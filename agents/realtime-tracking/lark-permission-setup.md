# 飞书实时看板权限开通说明

- generated_at: 2026-07-07
- target: Unity HMI 实时任务跟踪看板
- app_id: `cli_aa96499f7ce29cbd`

## 当前状态

飞书 Base 看板已创建并完成数据同步，当前状态为 `ready_daily_sync`。

- Base：`https://yousandi.feishu.cn/base/QIFybHOSUaU7HUsQ1h8c2eV5nY8`
- Dashboard ID：`blkxBQFl6g0CY98j`
- 授权群：DM006. Realtime Task Management（`oc_824642a195aa4a6d1fd2861fd8c749da`），view 权限
- 日更：Codex automation `unity-hmi` 已激活，Asia/Shanghai 每天 09:00

## 需要开通的权限

授权原则：

- 不申请任何单独 `delete` 类权限。
- 创建 Base 时保留平台默认表，再新增项目状态、人员负载、数据源健康、风险队列和每日变化表。
- 不使用会删除默认表的 `+base-create --table-name --fields` 路径。

已经通过：

- `base:app:create`
- `base:table:read`
- `base:table:create`
- `base:table:update`
- `base:field:read`
- `base:field:create`
- `base:field:update`
- `base:view:write_only`
- `base:record:read`
- `base:record:create`
- `base:record:update`
- `base:dashboard:read`
- `base:dashboard:create`
- `base:dashboard:update`
- `docs:permission.member:create`

## 开通后继续执行

日常手动刷新可运行：

```bash
python3 tools/generate-realtime-dashboard-state.py
python3 tools/calibrate-realtime-dashboard-from-weekly-report.py
python3 tools/sync-lark-dashboard.py --sync
python3 tools/sync-lark-dashboard.py --dedupe
```

首次创建或结构补齐时才运行：

```bash
python3 tools/sync-lark-dashboard.py --create
python3 tools/sync-lark-dashboard.py --grant-team
```

## 降级方案

如果 Base 同步临时失败，可以先使用飞书群每日看板摘要：

```bash
python3 tools/generate-realtime-dashboard-state.py
python3 tools/calibrate-realtime-dashboard-from-weekly-report.py
python3 tools/send-lark-dashboard-digest.py --send
```

目标群：

- DM006. Realtime Task Management
- chat_id: `oc_824642a195aa4a6d1fd2861fd8c749da`
- 发送身份：bot

该方案不创建 Base 仪表盘，但能保证团队每天在群内看到项目热度、人员可见负载、风险队列和数据口径。启用前需要确认发送身份与消息内容。
