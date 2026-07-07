#!/usr/bin/env ruby
# frozen_string_literal: true

require "json"
require "yaml"
require "csv"
require "fileutils"
require "time"

ROOT = File.expand_path("..", __dir__)
SRC = File.join(ROOT, "tmp", "2026-source-index")
OUT = File.join(ROOT, "agents", "analysis")
FileUtils.mkdir_p(OUT)

def load_json(path, fallback = [])
  JSON.parse(File.read(path))
rescue Errno::ENOENT
  fallback
end

def clean(text)
  text.to_s.gsub(/<[^>]+>/, "").gsub(/&amp;/, "&").gsub(/\s+/, " ").strip
end

def normalize_name(name)
  s = clean(name)
  s = s.sub(/\(.+\)\z/, "")
  s = s.sub(/（.+）\z/, "")
  s.strip
end

PROJECTS = [
  {
    id: "hongqi-8397",
    name: "红旗8397",
    patterns: [/红旗\s*8397/i, /红旗.*(语音|角色|SR|车控|投影|千人千面|VPA|设计)/i, /8397内部例会/i, /一汽红旗/i]
  },
  {
    id: "dongfeng-8397",
    name: "东风8397",
    patterns: [/东风\s*8397/i, /东风xUnity.*8397/i, /东风\+Unity/i, /东风.*POC/i]
  },
  {
    id: "dongfeng-4sr",
    name: "东风4SR / 8295 4SR",
    patterns: [/东风.*4SR/i, /东风.*8295/i, /4SR项目/i, /8397\s*&\s*4SR/i]
  },
  {
    id: "benteng-e541",
    name: "奔腾E541 / 奔腾实验室",
    patterns: [/E541/i, /奔腾/i]
  },
  {
    id: "auto-show-demo",
    name: "2026车展DEMO",
    patterns: [/车展/i, /Demo01/i, /HMI Demo/i, /2026.*Demo/i]
  },
  {
    id: "aios-ai-workflow",
    name: "AIOS / AI Workflow / AI Worker",
    patterns: [/AIOS/i, /AI workflow/i, /AI桌面/i, /AI Worker/i, /fufu/i, /智能机器人/i, /AI Agent/i, /AI 工具/i]
  },
  {
    id: "lixiang-game",
    name: "理想游戏上车",
    patterns: [/理想游戏/i, /饥饿鲨/i, /车载游戏/i, /虚拟控制器/i, /虚拟手柄/i]
  },
  {
    id: "benz-hmi",
    name: "奔驰HMI",
    patterns: [/奔驰HMI/i, /奔驰/i]
  },
  {
    id: "gac-audio",
    name: "广汽音频可视化",
    patterns: [/广汽.*音频/i, /广汽本田音乐可视化/i]
  },
  {
    id: "jetour-light",
    name: "捷途灯语",
    patterns: [/捷途.*灯语/i]
  },
  {
    id: "design-system-platform",
    name: "设计系统 / 动效平台化",
    patterns: [/设计系统/i, /动效平台化/i, /UI kit/i, /3DEngine Library/i, /DS00/i]
  },
  {
    id: "research-figma",
    name: "Figma / 创意研究画板",
    patterns: [/figma/i, /赛博朋克/i, /GVDP/i]
  }
].freeze

def project_matches(text)
  PROJECTS.select { |p| p[:patterns].any? { |re| text =~ re } }
end

roster = YAML.load_file(File.join(ROOT, "agents", "team-roster.yml"))
assignments = YAML.load_file(File.join(ROOT, "agents", "project-assignments.yml"))
open_id_to_name = {}
name_to_agent = {}
([roster["lead_agent"]] + roster["subagents"]).each do |person|
  name = person["name"]
  open_id_to_name[person.dig("feishu", "open_id")] = name if person.dig("feishu", "open_id")
  name_to_agent[name] = person["id"]
end

excluded_names = ["李达", "张婕"]
active_names = name_to_agent.keys - ["杨帆"] - excluded_names

project_stats = {}
PROJECTS.each do |p|
  project_stats[p[:id]] = {
    "project_id" => p[:id],
    "project_name" => p[:name],
    "evidence" => {"drive_docs" => 0, "meetings" => 0, "chat_messages" => 0, "figma_links" => 0, "self_declared" => 0},
    "people" => Hash.new { |h, k| h[k] = {"score" => 0.0, "drive_edit_docs" => 0, "drive_owner_docs" => 0, "chat_messages" => 0, "meeting_organizer" => 0, "self_declared" => 0, "domain_leader" => 0, "domain_partner" => 0} },
    "sample_evidence" => []
  }
end

people_scores = Hash.new { |h, k| h[k] = {"total_score" => 0.0, "projects" => Hash.new(0.0), "evidence_counts" => Hash.new(0)} }

def add_evidence(project_stats, people_scores, project_id, source, title, url: nil, person: nil, score: 0.0, count_key: nil)
  p = project_stats[project_id]
  return unless p

  p["evidence"][source] += 1
  if p["sample_evidence"].length < 8
    p["sample_evidence"] << {"source" => source, "title" => title, "url" => url}.compact
  end
  return unless person && !person.empty?

  p["people"][person]["score"] += score
  p["people"][person][count_key] += 1 if count_key
  people_scores[person]["total_score"] += score
  people_scores[person]["projects"][project_id] += score
  people_scores[person]["evidence_counts"][count_key] += 1 if count_key
end

drive_batches = load_json(File.join(SRC, "drive_searches_2026.json"))
seen_drive = {}
drive_batches.each do |batch|
  (batch["results"] || []).each do |r|
    meta = r["result_meta"] || {}
    title = clean(r["title_highlighted"])
    url = meta["url"]
    key = [title, url]
    next if seen_drive[key]
    seen_drive[key] = true
    text = [batch["query"], title, clean(r["summary_highlighted"]), url].join(" ")
    matches = project_matches(text)
    matches.each do |proj|
      editor = normalize_name(meta["edit_user_name"])
      owner = normalize_name(meta["owner_name"])
      add_evidence(project_stats, people_scores, proj[:id], "drive_docs", title, url: url)
      add_evidence(project_stats, people_scores, proj[:id], "drive_docs", title, url: url, person: editor, score: 3.0, count_key: "drive_edit_docs") if active_names.include?(editor)
      if active_names.include?(owner) && owner != editor
        add_evidence(project_stats, people_scores, proj[:id], "drive_docs", title, url: url, person: owner, score: 1.5, count_key: "drive_owner_docs")
      end
    end
  end
end

messages = load_json(File.join(SRC, "im_messages_2026.json"))
messages.each do |m|
  text = clean(m["content"])
  matches = project_matches(text)
  next if matches.empty?
  sender = open_id_to_name[m.dig("sender", "id")]
  matches.each do |proj|
    add_evidence(project_stats, people_scores, proj[:id], "chat_messages", "#{m["create_time"]} #{text[0, 80]}", url: m["message_app_link"])
    if sender && active_names.include?(sender)
      add_evidence(project_stats, people_scores, proj[:id], "chat_messages", text[0, 80], url: m["message_app_link"], person: sender, score: 1.0, count_key: "chat_messages")
    end
  end
end

meetings = load_json(File.join(SRC, "vc_meetings_2026.json"))
meetings.each do |m|
  text = clean(m["display_info"])
  matches = project_matches(text)
  next if matches.empty?
  organizer = text[/组织者：([^|]+?)\s*\|/, 1]
  organizer = normalize_name(organizer)
  matches.each do |proj|
    add_evidence(project_stats, people_scores, proj[:id], "meetings", text.lines.first&.strip || text, url: m.dig("meta_data", "app_link"))
    if active_names.include?(organizer)
      add_evidence(project_stats, people_scores, proj[:id], "meetings", text.lines.first&.strip || text, url: m.dig("meta_data", "app_link"), person: organizer, score: 2.0, count_key: "meeting_organizer")
    end
  end
end

figma_links = load_json(File.join(SRC, "figma_links_2026.json"))
figma_links.each do |url|
  next if url.include?("/blog/")
  project_matches(url).each do |proj|
    add_evidence(project_stats, people_scores, proj[:id], "figma_links", url, url: url)
  end
end

(assignments["members"] || []).each do |m|
  name = m["name"]
  next unless active_names.include?(name)
  projects = m["historical_project_assignments"] || []
  projects.each do |project_name|
    matches = project_matches(project_name)
    matches.each do |proj|
      add_evidence(project_stats, people_scores, proj[:id], "self_declared", project_name, person: name, score: 2.0, count_key: "self_declared")
    end
  end
  leader_count = m.dig("load_indicators", "domain_leader_count").to_i
  partner_count = m.dig("load_indicators", "domain_partner_count").to_i
  people_scores[name]["evidence_counts"]["domain_leader_roles"] += leader_count
  people_scores[name]["evidence_counts"]["domain_partner_roles"] += partner_count
end

project_rows = project_stats.values.map do |p|
  p["evidence"]["total"] = p["evidence"].values_at("drive_docs", "meetings", "chat_messages", "figma_links").sum
  p["people"] = p["people"].sort_by { |_name, v| -v["score"] }.to_h
  p
end.sort_by { |p| -p["evidence"]["total"] }

people_rows = active_names.map do |name|
  score = people_scores[name]
  top_projects = score["projects"].sort_by { |_k, v| -v }.first(5).map do |project_id, value|
    {"project_id" => project_id, "project_name" => PROJECTS.find { |p| p[:id] == project_id }[:name], "score" => value.round(1)}
  end
  declared = (assignments["members"] || []).find { |m| m["name"] == name }
  declared_project_count = declared&.dig("load_indicators", "historical_project_count").to_i
  evidence_project_count = score["projects"].keys.length
  {
    "name" => name,
    "agent_id" => name_to_agent[name],
    "evidence_score" => score["total_score"].round(1),
    "evidence_project_count" => evidence_project_count,
    "self_declared_project_count" => declared_project_count,
    "load_delta_project_count" => evidence_project_count - declared_project_count,
    "domain_leader_count" => declared&.dig("load_indicators", "domain_leader_count").to_i,
    "domain_partner_count" => declared&.dig("load_indicators", "domain_partner_count").to_i,
    "evidence_counts" => score["evidence_counts"],
    "top_projects" => top_projects
  }
end.sort_by { |r| [-r["evidence_score"], -r["evidence_project_count"], r["name"]] }

output = {
  "version" => 1,
  "generated_at" => Time.now.iso8601,
  "period" => {"start" => "2026-01-01", "end" => "2026-07-06", "timezone" => "Asia/Shanghai"},
  "sources" => {
    "im_messages" => {"path" => "tmp/2026-source-index/im_messages_2026.json", "count" => messages.length},
    "drive_search_results" => {"path" => "tmp/2026-source-index/drive_searches_2026.json", "unique_results" => seen_drive.length},
    "vc_meetings" => {"path" => "tmp/2026-source-index/vc_meetings_2026.json", "count" => meetings.length},
    "figma_links" => {"path" => "tmp/2026-source-index/figma_links_2026.json", "count" => figma_links.length}
  },
  "scoring_model" => {
    "drive_edit_doc" => 3.0,
    "drive_owner_doc_when_not_editor" => 1.5,
    "meeting_organizer" => 2.0,
    "chat_project_message" => 1.0,
    "self_declared_project" => 2.0,
    "notes" => [
      "Scores quantify visible evidence, not final performance.",
      "Drive search is limited to resources visible to the authenticated user.",
      "Meeting contribution is currently based on organizer/title evidence; participant-level detail requires meeting detail expansion.",
      "Sheet/Base workhour and task records are not included until sheets:spreadsheet:read and base:table:read are authorized."
    ]
  },
  "projects" => project_rows,
  "people" => people_rows,
  "excluded_from_current_analysis" => ["李达", "张婕"]
}

File.write(File.join(OUT, "workload-evidence-2026.json"), JSON.pretty_generate(output))
CSV.open(File.join(OUT, "people-contribution-2026.csv"), "w") do |csv|
  csv << ["name", "agent_id", "evidence_score", "evidence_project_count", "self_declared_project_count", "load_delta_project_count", "domain_leader_count", "domain_partner_count", "top_projects"]
  people_rows.each do |r|
    csv << [r["name"], r["agent_id"], r["evidence_score"], r["evidence_project_count"], r["self_declared_project_count"], r["load_delta_project_count"], r["domain_leader_count"], r["domain_partner_count"], r["top_projects"].map { |p| "#{p["project_name"]}:#{p["score"]}" }.join("; ")]
  end
end
CSV.open(File.join(OUT, "project-evidence-2026.csv"), "w") do |csv|
  csv << ["project_id", "project_name", "total_evidence", "drive_docs", "meetings", "chat_messages", "figma_links", "top_people"]
  project_rows.each do |p|
    csv << [p["project_id"], p["project_name"], p["evidence"]["total"], p["evidence"]["drive_docs"], p["evidence"]["meetings"], p["evidence"]["chat_messages"], p["evidence"]["figma_links"], p["people"].first(5).map { |name, v| "#{name}:#{v["score"].round(1)}" }.join("; ")]
  end
end

puts JSON.pretty_generate({
  output: "agents/analysis/workload-evidence-2026.json",
  people: people_rows.length,
  projects: project_rows.length,
  top_people: people_rows.first(5).map { |r| [r["name"], r["evidence_score"]] },
  top_projects: project_rows.first(5).map { |p| [p["project_name"], p["evidence"]["total"]] }
})
