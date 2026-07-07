# 飞书实时看板权限开通说明

- generated_at: 2026-07-07
- target: Unity HMI 实时任务跟踪看板
- app_id: `cli_aa96499f7ce29cbd`

## 当前阻塞

创建飞书 Base 看板失败，原因是当前飞书 CLI 应用尚未在开发者后台申请 Base 创建权限。

飞书返回：

| 字段 | 内容 |
| --- | --- |
| missing_scope | `base:app:create` |
| error | `app_scope_not_applied` |
| identity | `bot` |

这不是用户授权操作问题。用户只能授权应用已经申请过的 scope；应用后台未申请时，用户侧授权会失败。

## 需要开通的权限

第一步先开通最小权限：

- `base:app:create`

申请入口：

https://open.feishu.cn/page/scope-apply?clientID=cli_aa96499f7ce29cbd&scopes=base%3Aapp%3Acreate

后续创建表、同步记录、创建仪表盘和团队授权时，可能还需要继续按 CLI 返回补充以下权限：

- `base:table:read`
- `base:table:create`
- `base:table:update`
- `base:table:delete`
- `base:record:read`
- `base:record:create`
- `base:record:update`
- `base:dashboard:read`
- `base:dashboard:create`
- `base:dashboard:update`
- Drive/Base 协作者授权相关权限

## 开通后继续执行

后台权限开通并发布/生效后，回到本仓库运行：

```bash
python3 tools/generate-realtime-dashboard-state.py
python3 tools/sync-lark-dashboard.py --create
python3 tools/sync-lark-dashboard.py --sync
python3 tools/sync-lark-dashboard.py --grant-team
```

完成后把 `agents/realtime-tracking/lark-dashboard.json` 中的 `setup_status` 改为 `ready`，并激活 Codex 自动化 `Unity HMI 实时任务看板每日更新`。

## 当前自动化状态

每日自动化已创建但保持暂停，避免在权限未开通前每天失败。

## 降级方案

如果 Base 权限短期无法开通，可以先使用飞书群每日看板摘要：

```bash
python3 tools/generate-realtime-dashboard-state.py
python3 tools/send-lark-dashboard-digest.py --send
```

目标群：

- DM006. Realtime Task Management
- chat_id: `oc_824642a195aa4a6d1fd2861fd8c749da`
- 发送身份：bot

该方案不创建 Base 仪表盘，但能保证团队每天在群内看到项目热度、人员可见负载、风险队列和数据口径。启用前需要确认发送身份与消息内容。
