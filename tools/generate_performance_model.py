#!/usr/bin/env python3
from pathlib import Path
import csv
import json
import re
import subprocess

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_DATE = "2026-07-08"
MODEL_VERSION = "0.2"
LOCAL_XLSX_ROOT = Path("/Users/frankyang/my_work/My_Team/2025 Mid-year review/xlsx")
OUT_XLSX = ROOT / "agents/performance/2026H1-performance-weight-model.xlsx"
OUT_YML = ROOT / "agents/performance/performance-score-model-v0.2.yml"
OUT_MD = ROOT / "agents/performance/2026H1-performance-model-summary.md"
OUT_CSV = ROOT / "agents/performance/2026H1-performance-score-snapshot.csv"


SUBITEM_ROWS = list(range(16, 32))
SUBITEM_DIMENSIONS = {
    16: "UI/UE设计产出与质量",
    17: "UI/UE设计产出与质量",
    18: "UI/UE设计产出与质量",
    19: "UI/UE设计产出与质量",
    20: "项目进度与执行力",
    21: "项目进度与执行力",
    22: "项目进度与执行力",
    23: "设计能力与沉淀、AI工具利用",
    24: "设计能力与沉淀、AI工具利用",
    25: "设计能力与沉淀、AI工具利用",
    26: "设计能力与沉淀、AI工具利用",
    27: "团队协作与沟通",
    28: "团队协作与沟通",
    29: "团队协作与沟通",
    30: "工作规范与责任心",
    31: "工作规范与责任心",
}

DEFAULT_WEIGHTS = {
    "local_form": 0.25,
    "evidence": 0.35,
    "role": 0.15,
    "mainline": 0.20,
    "confidence": 0.05,
    "evidence_benchmark": 100,
    "project_benchmark": 6,
    "leader_point": 10,
    "partner_point": 3,
    "owner_bonus": 18,
    "blank_form_penalty": 0,
}

QUALITATIVE_SCORES = {
    "critical_overload_risk": 92,
    "strategic_overload_risk": 92,
    "high_overload_risk": 88,
    "high_load": 84,
    "broad_partner_load": 78,
    "balanced_specialist_load": 80,
    "medium_high_load": 76,
    "super_collaboration_support_capacity": 68,
    "onboarding_capacity": 55,
    "super_collaboration_unassigned_capacity": 50,
}


def as_float(value, default=0.0):
    if value is None or value == "":
        return default
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(str(value).strip().replace("%", ""))
    except ValueError:
        return default


def band_from_score(score):
    score = as_float(score)
    if score >= 90:
        return "A"
    if score >= 85:
        return "B+"
    if score >= 75:
        return "B"
    if score >= 60:
        return "C"
    return "D"


def score_employee(row):
    if row["analysis_status"] == "excluded_transition":
        return {
            "local_or_rule_score": "EXCLUDED",
            "evidence_norm_score": "EXCLUDED",
            "role_score": "EXCLUDED",
            "mainline_score": "EXCLUDED",
            "confidence_score": "EXCLUDED",
            "model_estimated_score": "EXCLUDED",
            "model_band": "排除",
            "suggested_action": "不进入本轮主分析",
        }

    evidence = as_float(row["evidence_score"])
    projects = as_float(row["evidence_project_count"])
    leader = as_float(row["domain_leader_count"])
    partner = as_float(row["domain_partner_count"])
    local_filled = row["local_form_status"] == "filled"
    load_baseline = QUALITATIVE_SCORES.get(row["qualitative_load"], 60)
    local_or_rule = as_float(row["local_final_score"]) if local_filled else load_baseline
    evidence_norm = min(100, evidence / DEFAULT_WEIGHTS["evidence_benchmark"] * 100)
    owner_bonus = DEFAULT_WEIGHTS["owner_bonus"] if row["organization_role"] == "owner" else 0
    role_score = min(100, leader * DEFAULT_WEIGHTS["leader_point"] + partner * DEFAULT_WEIGHTS["partner_point"] + owner_bonus)
    project_score = min(100, projects / DEFAULT_WEIGHTS["project_benchmark"] * 100)
    mainline = round(evidence_norm * 0.45 + role_score * 0.25 + project_score * 0.20 + load_baseline * 0.10, 1)
    confidence = min(100, (35 if local_filled else 0) + (35 if evidence > 0 else 0) + (15 if projects > 0 else 0) + (15 if leader + partner > 0 else 0))
    estimated = round(
        local_or_rule * DEFAULT_WEIGHTS["local_form"]
        + evidence_norm * DEFAULT_WEIGHTS["evidence"]
        + role_score * DEFAULT_WEIGHTS["role"]
        + mainline * DEFAULT_WEIGHTS["mainline"]
        + confidence * DEFAULT_WEIGHTS["confidence"]
        - DEFAULT_WEIGHTS["blank_form_penalty"] * (0 if local_filled else 1),
        1,
    )
    action = "补齐本地评价表与证据索引" if not local_filled else ("补证并复核置信度" if confidence < 70 else "可进入管理者校准")
    return {
        "local_or_rule_score": local_or_rule,
        "evidence_norm_score": round(evidence_norm, 1),
        "role_score": round(role_score, 1),
        "mainline_score": mainline,
        "confidence_score": round(confidence, 1),
        "model_estimated_score": estimated,
        "model_band": band_from_score(estimated),
        "suggested_action": action,
    }


def load_yaml_with_ruby(path):
    out = subprocess.check_output(
        ["ruby", "-ryaml", "-rjson", "-e", "puts JSON.generate(YAML.load_file(ARGV[0]))", str(path)],
        text=True,
    )
    return json.loads(out)


def read_local_forms():
    rows = []
    for path in sorted(LOCAL_XLSX_ROOT.glob("*/*.xlsx")):
        if path.name.startswith("~$"):
            continue
        wb = load_workbook(path, data_only=True, read_only=True)
        ws = wb["设计团队评分表"] if "设计团队评分表" in wb.sheetnames else wb[wb.sheetnames[-1]]
        person = ws["D3"].value or path.parent.name
        item_scores = []
        item_max = []
        for r in SUBITEM_ROWS:
            item_scores.append(ws.cell(r, 5).value)
            item_max.append(as_float(ws.cell(r, 4).value))
        filled = sum(1 for v in item_scores if isinstance(v, (int, float)) and v > 0)
        base = as_float(ws["B48"].value)
        bonus = as_float(ws["B49"].value)
        deduct = as_float(ws["B50"].value)
        final = as_float(ws["B51"].value)
        band = ws["B52"].value or ""
        status = "filled" if filled >= 12 and final > 0 else "template_blank"
        rows.append({
            "name": person,
            "folder": path.parent.name,
            "local_file": str(path),
            "local_form_status": status,
            "filled_items": filled,
            "local_base_score": base,
            "local_bonus": bonus,
            "local_deduct": deduct,
            "local_final_score": final,
            "local_band": band,
        })
    return rows


def read_people_evidence():
    data = {}
    path = ROOT / "agents/analysis/people-contribution-2026.csv"
    with path.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            data[row["name"]] = row
    return data


def read_assignments():
    path = ROOT / "agents/project-assignments.yml"
    doc = load_yaml_with_ruby(path)
    data = {}
    for m in doc.get("members", []):
        data[m["name"]] = m
    excluded = {m.get("name"): m for m in doc.get("analysis_policy", {}).get("excluded_from_workload_analysis", [])}
    return data, excluded


def build_employee_rows():
    local = {row["name"]: row for row in read_local_forms()}
    evidence = read_people_evidence()
    assignments, excluded = read_assignments()
    names = sorted(set(local) | set(evidence) | set(assignments))
    rows = []
    for name in names:
        l = local.get(name, {})
        e = evidence.get(name, {})
        a = assignments.get(name, {})
        load = a.get("load_indicators", {}) if isinstance(a, dict) else {}
        role = a.get("organization_role", "") if isinstance(a, dict) else ""
        team = a.get("organization_team", "") if isinstance(a, dict) else ""
        status = "excluded_transition" if name in excluded or role == "transition" else "active"
        local_status = l.get("local_form_status", "missing")
        rows.append({
            "name": name,
            "agent_id": e.get("agent_id") or a.get("agent_id", ""),
            "analysis_status": status,
            "organization_team": team,
            "organization_role": role,
            "qualitative_load": load.get("qualitative_load", ""),
            "historical_project_count": load.get("historical_project_count", 0),
            "domain_leader_count": e.get("domain_leader_count", load.get("domain_leader_count", 0)),
            "domain_partner_count": e.get("domain_partner_count", load.get("domain_partner_count", 0)),
            "evidence_score": e.get("evidence_score", 0),
            "evidence_project_count": e.get("evidence_project_count", 0),
            "self_declared_project_count": e.get("self_declared_project_count", len(a.get("historical_project_assignments", [])) if isinstance(a, dict) else 0),
            "load_delta_project_count": e.get("load_delta_project_count", 0),
            "top_projects": e.get("top_projects", ""),
            "local_file": l.get("local_file", ""),
            "local_form_status": local_status,
            "filled_items": l.get("filled_items", 0),
            "local_base_score": l.get("local_base_score", 0),
            "local_bonus": l.get("local_bonus", 0),
            "local_deduct": l.get("local_deduct", 0),
            "local_final_score": l.get("local_final_score", 0),
            "local_band": l.get("local_band", ""),
        })
    return rows


def setup_sheet(ws, title=None):
    ws.freeze_panes = "A2"
    ws.sheet_view.showGridLines = False
    if title:
        ws["A1"] = title


def style_table(ws, header_row=1):
    header_fill = PatternFill("solid", fgColor="1F2937")
    header_font = Font(color="FFFFFF", bold=True)
    thin = Side(style="thin", color="D1D5DB")
    for cell in ws[header_row]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = Border(bottom=thin)
    for row in ws.iter_rows(min_row=header_row + 1):
        for cell in row:
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            cell.border = Border(bottom=Side(style="hair", color="E5E7EB"))


def autosize(ws, max_width=48):
    for col in range(1, ws.max_column + 1):
        letter = get_column_letter(col)
        width = 10
        for cell in ws[letter]:
            value = cell.value
            if value is None:
                continue
            width = max(width, min(max_width, len(str(value)) + 2))
        ws.column_dimensions[letter].width = width


def add_weights(wb):
    ws = wb.create_sheet("01_权重设置")
    ws.append(["参数ID", "参数名称", "当前值", "单位/类型", "建议范围", "说明"])
    rows = [
        ("w_local_form", "本地评价表权重", 0.25, "ratio", "0-0.50", "本地 Excel 已填写时参与；空模板时自动再分配给其他证据。"),
        ("w_evidence", "云端/项目证据权重", 0.35, "ratio", "0.20-0.50", "来自飞书、云盘、会议、Figma metadata 与现有贡献分。"),
        ("w_role", "组织/领域角色权重", 0.15, "ratio", "0.05-0.25", "体现 owner、domain leader、partner 等角色责任。"),
        ("w_mainline", "主线贡献权重", 0.20, "ratio", "0.10-0.30", "体现 AI提效、领域驱动、超级合作等主线职责贡献。"),
        ("w_confidence", "证据置信度权重", 0.05, "ratio", "0.00-0.15", "证据来源覆盖、是否原始数据可复核。"),
        ("evidence_benchmark", "证据分基准", 100, "score", "80-150", "用于把 evidence_score 归一到 0-100，可随团队整体数据接入调整。"),
        ("project_benchmark", "项目覆盖基准", 6, "count", "3-8", "项目覆盖数达到该值视为满档。"),
        ("leader_point", "每个领域 leader 角色分", 10, "points", "6-12", "角色组件使用。"),
        ("partner_point", "每个领域 partner 角色分", 3, "points", "1-5", "角色组件使用。"),
        ("owner_bonus", "组织 owner 加分", 18, "points", "10-25", "AI提效/超级合作 owner 的角色责任加成。"),
        ("active_confidence_floor", "活跃成员置信度底线", 45, "score", "30-60", "有云端证据但本地表未填时的置信度底线。"),
        ("blank_form_penalty", "空本地表惩罚", 0, "points", "0-10", "默认不惩罚，因为当前本地表大多是模板态。"),
        ("bonus_cap", "加分项建议上限", 5, "points", "3-8", "用于后续人工评价表复核。"),
    ]
    for r in rows:
        ws.append(r)
    ws.append(["weight_sum", "权重合计", '=SUM(C2:C6)', "ratio", "应为 1.00", "如果不等于 1，模型仍按有效权重归一，但建议保持 1。"])
    style_table(ws)
    for row in ws.iter_rows(min_row=2, max_col=3):
        if row[0].value != "weight_sum":
            row[2].font = Font(color="0000FF")
            row[2].fill = PatternFill("solid", fgColor="FFF7CC")
    ws["C15"].font = Font(color="008000")
    ws["C15"].fill = PatternFill("solid", fgColor="E8F5E9")
    autosize(ws)
    return ws


def add_rules(wb):
    ws = wb.create_sheet("02_主线打分规则")
    ws.append(["规则ID", "模块", "分值/权重", "A档条件", "B档条件", "C/D风险", "数据来源"])
    rows = [
        ("mainline_output", "主线产出", "35%", "有关键项目主责或平台级交付，交付物可追溯", "多项目稳定交付，主责边界清楚", "只有零散支援或证据不足", "Figma/云盘/本地源文件/最终交付"),
        ("mainline_role", "主线角色责任", "20%", "owner 或核心 domain leader，能做关键判断", "重要 partner 或二级 owner", "角色缺失或职责未定义", "organization-teams / domain-formation"),
        ("mainline_impact", "主线影响力", "20%", "跨团队复用、提效、方法论或机制沉淀", "项目内复用或局部提效", "只做单点执行，无复用记录", "复盘文档/工具使用记录/会议结论"),
        ("mainline_execution", "主线推进闭环", "15%", "按期闭环，风险预警清楚，阻塞少", "基本按期，问题有上报", "延期或返工多且缺少闭环", "Jira/Gantt/飞书会议/反馈记录"),
        ("mainline_confidence", "证据置信度", "10%", "至少三类高/中置信来源交叉验证", "两类来源可验证", "仅自述或路径不可访问", "raw export / evidence index"),
    ]
    for r in rows:
        ws.append(r)
    ws.append([])
    ws.append(["档位", "分数区间", "必要条件"])
    bands = [
        ("A", "90-100", "至少一条关键项目主责或平台级贡献；证据覆盖 3 类以上来源；无重大质量/协作风险；有团队或跨团队影响。"),
        ("B+", "85-89", "多项目稳定交付，证据充分，有明确领域优势，但平台级影响或量化效果仍需补证。"),
        ("B", "75-84", "完成本职和主要项目，协作与质量稳定，创新和影响力有限。"),
        ("C", "60-74", "有交付但证据不足、延期/返工偏多，或主要为被动执行。"),
        ("D", "<60", "核心任务未达成、重大质量/协作风险，或证据无法支撑基本交付。"),
    ]
    for b in bands:
        ws.append(b)
    style_table(ws)
    autosize(ws)
    return ws


def add_lookups(wb):
    ws = wb.create_sheet("03_映射表")
    ws.append(["类型", "键", "值", "说明"])
    rows = [
        ("qualitative_load", "critical_overload_risk", 92, "关键过载，通常代表高责任/高复杂度。"),
        ("qualitative_load", "strategic_overload_risk", 92, "战略高负载。"),
        ("qualitative_load", "high_overload_risk", 88, "高过载。"),
        ("qualitative_load", "high_load", 84, "高覆盖。"),
        ("qualitative_load", "broad_partner_load", 78, "广覆盖协作者。"),
        ("qualitative_load", "balanced_specialist_load", 80, "聚焦专家。"),
        ("qualitative_load", "medium_high_load", 76, "中高负载。"),
        ("qualitative_load", "super_collaboration_support_capacity", 68, "超级合作支援池。"),
        ("qualitative_load", "onboarding_capacity", 55, "新人/onboarding。"),
        ("qualitative_load", "super_collaboration_unassigned_capacity", 50, "未分配容量。"),
        ("organization_role", "owner", 100, "组织主责。"),
        ("organization_role", "domain_driven_member", 78, "领域驱动成员。"),
        ("organization_role", "super_collaboration_member", 70, "超级合作成员。"),
        ("organization_role", "transition", 0, "过渡/排除。"),
        ("local_form_status", "filled", 100, "本地评价表已填写。"),
        ("local_form_status", "template_blank", 45, "本地表存在但为空模板。"),
        ("local_form_status", "missing", 30, "未发现本地表。"),
    ]
    for r in rows:
        ws.append(r)
    style_table(ws)
    autosize(ws)
    return ws


def add_employee_input(wb, rows):
    ws = wb.create_sheet("04_员工输入")
    headers = [
        "姓名", "agent_id", "分析状态", "组织团队", "组织角色", "负载标签",
        "历史项目数", "领域Leader数", "领域Partner数", "可见证据分",
        "可见项目数", "手填项目数", "项目差值", "Top项目",
        "本地文件", "本地表状态", "已填子项数", "本地基础分", "本地加分",
        "本地扣分", "本地最终分", "本地档位"
    ]
    ws.append(headers)
    for r in rows:
        ws.append([
            r["name"], r["agent_id"], r["analysis_status"], r["organization_team"], r["organization_role"], r["qualitative_load"],
            as_float(r["historical_project_count"]), as_float(r["domain_leader_count"]), as_float(r["domain_partner_count"]),
            as_float(r["evidence_score"]), as_float(r["evidence_project_count"]), as_float(r["self_declared_project_count"]),
            as_float(r["load_delta_project_count"]), r["top_projects"], r["local_file"], r["local_form_status"], r["filled_items"],
            as_float(r["local_base_score"]), as_float(r["local_bonus"]), as_float(r["local_deduct"]), as_float(r["local_final_score"]), r["local_band"],
        ])
    style_table(ws)
    autosize(ws, 70)
    return ws


def add_model_scores(wb, n_rows):
    ws = wb.create_sheet("05_模型算分")
    headers = [
        "姓名", "分析状态", "组织团队", "本地表状态",
        "本地表分", "证据归一分", "角色责任分", "主线贡献分", "证据置信分",
        "本地有效权重", "证据有效权重", "角色有效权重", "主线有效权重", "置信有效权重",
        "模型预估分", "模型档位", "建议动作", "说明"
    ]
    ws.append(headers)
    for i in range(2, n_rows + 2):
        input_row = i
        row = ws.max_row + 1
        ws.cell(row, 1, f"='04_员工输入'!A{input_row}")
        ws.cell(row, 2, f"='04_员工输入'!C{input_row}")
        ws.cell(row, 3, f"='04_员工输入'!D{input_row}")
        ws.cell(row, 4, f"='04_员工输入'!P{input_row}")
        ws.cell(row, 5, f'=IF(D{row}="filled",\'04_员工输入\'!U{input_row},IFERROR(SUMIFS(\'03_映射表\'!$C:$C,\'03_映射表\'!$A:$A,"qualitative_load",\'03_映射表\'!$B:$B,\'04_员工输入\'!F{input_row}),60))')
        ws.cell(row, 6, f'=MIN(100,\'04_员工输入\'!J{input_row}/VLOOKUP("evidence_benchmark",\'01_权重设置\'!$A:$C,3,FALSE)*100)')
        ws.cell(row, 7, f'=MIN(100,\'04_员工输入\'!H{input_row}*VLOOKUP("leader_point",\'01_权重设置\'!$A:$C,3,FALSE)+\'04_员工输入\'!I{input_row}*VLOOKUP("partner_point",\'01_权重设置\'!$A:$C,3,FALSE)+IF(\'04_员工输入\'!E{input_row}="owner",VLOOKUP("owner_bonus",\'01_权重设置\'!$A:$C,3,FALSE),0))')
        ws.cell(row, 8, f'=ROUND((F{row}*0.45+G{row}*0.25+MIN(100,\'04_员工输入\'!K{input_row}/VLOOKUP("project_benchmark",\'01_权重设置\'!$A:$C,3,FALSE)*100)*0.20+IFERROR(SUMIFS(\'03_映射表\'!$C:$C,\'03_映射表\'!$A:$A,"qualitative_load",\'03_映射表\'!$B:$B,\'04_员工输入\'!F{input_row}),60)*0.10),1)')
        ws.cell(row, 9, f'=MIN(100,IF(D{row}="filled",35,0)+IF(\'04_员工输入\'!J{input_row}>0,35,0)+IF(\'04_员工输入\'!K{input_row}>0,15,0)+IF(\'04_员工输入\'!H{input_row}+\'04_员工输入\'!I{input_row}>0,15,0))')
        ws.cell(row, 10, f'=VLOOKUP("w_local_form",\'01_权重设置\'!$A:$C,3,FALSE)')
        ws.cell(row, 11, f'=VLOOKUP("w_evidence",\'01_权重设置\'!$A:$C,3,FALSE)')
        ws.cell(row, 12, f'=VLOOKUP("w_role",\'01_权重设置\'!$A:$C,3,FALSE)')
        ws.cell(row, 13, f'=VLOOKUP("w_mainline",\'01_权重设置\'!$A:$C,3,FALSE)')
        ws.cell(row, 14, f'=VLOOKUP("w_confidence",\'01_权重设置\'!$A:$C,3,FALSE)')
        ws.cell(row, 15, f'=IF(B{row}="excluded_transition","EXCLUDED",ROUND(E{row}*J{row}+F{row}*K{row}+G{row}*L{row}+H{row}*M{row}+I{row}*N{row}-VLOOKUP("blank_form_penalty",\'01_权重设置\'!$A:$C,3,FALSE)*(D{row}<>"filled"),1))')
        ws.cell(row, 16, f'=IF(O{row}="EXCLUDED","排除",IF(O{row}>=90,"A",IF(O{row}>=85,"B+",IF(O{row}>=75,"B",IF(O{row}>=60,"C","D")))))')
        ws.cell(row, 17, f'=IF(B{row}="excluded_transition","不进入本轮主分析",IF(D{row}<>"filled","补齐本地评价表与证据索引",IF(I{row}<70,"补证并复核置信度","可进入管理者校准")))') 
        ws.cell(row, 18, f'=IF(D{row}<>"filled","当前本地员工表为空模板，本地表分使用现有规则基线；填写后自动替换为人工评价分。","本地评价表已参与模型加权。")')
    style_table(ws)
    for row in ws.iter_rows(min_row=2):
        for cell in row[9:14]:
            cell.number_format = "0.0%"
        if row[14].value != "EXCLUDED":
            row[14].number_format = "0.0"
    autosize(ws, 58)
    return ws


def add_snapshot(wb, rows):
    ws = wb.create_sheet("06_当前评分快照")
    headers = [
        "姓名", "分析状态", "组织团队", "本地表状态", "规则/本地分", "证据归一分",
        "角色责任分", "主线贡献分", "证据置信分", "模型建议分", "建议档位", "建议动作"
    ]
    ws.append(headers)
    snapshot_rows = []
    for row in rows:
        score = score_employee(row)
        values = [
            row["name"], row["analysis_status"], row["organization_team"], row["local_form_status"],
            score["local_or_rule_score"], score["evidence_norm_score"], score["role_score"],
            score["mainline_score"], score["confidence_score"], score["model_estimated_score"],
            score["model_band"], score["suggested_action"],
        ]
        ws.append(values)
        snapshot_rows.append(dict(zip(headers, values)))
    style_table(ws)
    autosize(ws)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(snapshot_rows)
    return ws


def add_summary(wb, n_rows):
    ws = wb.create_sheet("00_总览")
    rows = [
        ["项目", "2026H1 设计团队定量分析模型"],
        ["模型版本", MODEL_VERSION],
        ["生成日期", RUNTIME_DATE],
        ["本地评价表目录", str(LOCAL_XLSX_ROOT)],
        ["说明", "蓝色/黄色单元格为可调参数；模型分会根据权重和后续证据接入动态重算。"],
        ["重要提醒", "当前本地员工评价表均为空模板，模型预估分不是最终绩效分，需要管理者校准。"],
    ]
    for r in rows:
        ws.append(r)
    ws.append([])
    ws.append(["姓名", "分析状态", "组织团队", "本地表状态", "模型预估分", "模型档位", "建议动作"])
    start = ws.max_row
    for i in range(2, n_rows + 2):
        row = ws.max_row + 1
        ws.cell(row, 1, f"='05_模型算分'!A{i}")
        ws.cell(row, 2, f"='05_模型算分'!B{i}")
        ws.cell(row, 3, f"='05_模型算分'!C{i}")
        ws.cell(row, 4, f"='05_模型算分'!D{i}")
        ws.cell(row, 5, f"='05_模型算分'!O{i}")
        ws.cell(row, 6, f"='05_模型算分'!P{i}")
        ws.cell(row, 7, f"='05_模型算分'!Q{i}")
    for cell in ws[1]:
        cell.font = Font(bold=True)
    style_table(ws, header_row=start)
    autosize(ws, 60)
    return ws


def add_version_log(wb):
    ws = wb.create_sheet("99_版本记录")
    ws.append(["版本", "日期", "作者", "变更内容", "兼容性"])
    rows = [
        ("0.1", "2026-07-07", "Codex", "建立小范围绩效评分 YAML 草案，完成李颖样本审计。", "文档模型"),
        ("0.2", RUNTIME_DATE, "Codex", "生成可调权重 Excel 模型，接入本地员工评价表模板、云端证据和组织角色。", "可重算模型"),
    ]
    for r in rows:
        ws.append(r)
    style_table(ws)
    autosize(ws)
    return ws


def write_model_yml():
    OUT_YML.parent.mkdir(parents=True, exist_ok=True)
    text = f"""version: {MODEL_VERSION}
created_at: {RUNTIME_DATE}
timezone: Asia/Shanghai
outputs:
  workbook: {OUT_XLSX.relative_to(ROOT)}
  summary: {OUT_MD.relative_to(ROOT)}
  snapshot_csv: {OUT_CSV.relative_to(ROOT)}
local_employee_forms: "{LOCAL_XLSX_ROOT}"
model_policy:
  local_blank_forms_are_not_zero_performance: true
  zhang_jie_excluded_from_primary_analysis: true
  score_is_model_estimate_until_manager_calibration: true
  weights_are_adjustable_in_workbook: true
default_weights:
  local_form: 0.25
  evidence: 0.35
  role: 0.15
  mainline: 0.20
  confidence: 0.05
dynamic_recalculation:
  change_weight_sheet: "01_权重设置"
  employee_input_sheet: "04_员工输入"
  model_score_sheet: "05_模型算分"
  summary_sheet: "00_总览"
score_bands:
  A: ">=90"
  B_plus: "85-89"
  B: "75-84"
  C: "60-74"
  D: "<60"
"""
    OUT_YML.write_text(text, encoding="utf-8")


def write_summary(rows):
    blank_count = sum(1 for r in rows if r["local_form_status"] == "template_blank")
    active_count = sum(1 for r in rows if r["analysis_status"] == "active")
    excluded = [r["name"] for r in rows if r["analysis_status"] != "active"]
    text = f"""# 2026H1 定量绩效模型生成说明

- generated_at: {RUNTIME_DATE}
- model_version: {MODEL_VERSION}
- workbook: `agents/performance/2026H1-performance-weight-model.xlsx`
- local_employee_forms: `{LOCAL_XLSX_ROOT}`

## 生成结果

已生成一份可调权重 Excel 模型。权重位于 `01_权重设置`，员工输入位于 `04_员工输入`，模型预估分位于 `05_模型算分`，总览位于 `00_总览`。

## 当前数据状态

- 本地员工评价表数量：{len(rows)}
- active 分析成员：{active_count}
- 空模板评价表：{blank_count}
- 排除/过渡成员：{", ".join(excluded) if excluded else "无"}

当前 `/Users/frankyang/my_work/My_Team/2025 Mid-year review/xlsx` 中的员工评价表均处于模板态，子项分为空，基础分/最终分为 0。因此模型不会把这些空表当作真实绩效 0 分，而是把本地表状态标记为 `template_blank`，并用现有项目/角色/负载规则生成临时基线分。后续本地表填写后，该基线会自动替换为人工评价分。

## 使用方式

1. 打开 `agents/performance/2026H1-performance-weight-model.xlsx`。
2. 在 `01_权重设置` 调整蓝色/黄色参数。
3. 后续接入 Jira、本地文件索引、Figma raw export、飞书会议 raw JSON 后，更新 `04_员工输入` 或扩展证据输入。
4. 查看 `05_模型算分` 和 `00_总览` 的动态结果。
5. 查看 `06_当前评分快照` 或 `agents/performance/2026H1-performance-score-snapshot.csv` 获取当前默认权重下的静态建议分。

## 主线规则

主线评分不直接等同于文件数量或会议数量，而是由主线产出、角色责任、影响力、推进闭环、证据置信度组成。详见 workbook 的 `02_主线打分规则`。

## 版本管理

- `performance-score-model-v0.1.yml`：小范围绩效评分草案与李颖样本审计。
- `performance-score-model-v0.2.yml`：当前可调权重模型配置。
- workbook `99_版本记录`：记录 Excel 模型版本变更。
"""
    OUT_MD.write_text(text, encoding="utf-8")


def main():
    rows = build_employee_rows()
    OUT_XLSX.parent.mkdir(parents=True, exist_ok=True)
    wb = Workbook()
    wb.calculation.calcMode = "auto"
    wb.calculation.fullCalcOnLoad = True
    wb.calculation.forceFullCalc = True
    wb.remove(wb.active)
    add_weights(wb)
    add_rules(wb)
    add_lookups(wb)
    add_employee_input(wb, rows)
    add_model_scores(wb, len(rows))
    add_snapshot(wb, rows)
    add_summary(wb, len(rows))
    add_version_log(wb)
    wb._sheets = [wb["00_总览"], wb["01_权重设置"], wb["02_主线打分规则"], wb["03_映射表"], wb["04_员工输入"], wb["05_模型算分"], wb["06_当前评分快照"], wb["99_版本记录"]]
    for ws in wb.worksheets:
        ws.sheet_properties.pageSetUpPr.fitToPage = True
    wb.save(OUT_XLSX)
    write_model_yml()
    write_summary(rows)
    print(json.dumps({
        "workbook": str(OUT_XLSX),
        "summary": str(OUT_MD),
        "model_config": str(OUT_YML),
        "snapshot_csv": str(OUT_CSV),
        "employees": len(rows),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
