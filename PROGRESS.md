# 项目进度记录

## 项目名称
基于大模型 Agent（龙虾）的网站自动化发布与更新系统

## 当前状态：80% 完成

---

## 已完成

### 1. 核心工具链 ✅
- `agent/tools/tools.py` — 4 个工具函数（read_news、add_news、git_publish、git_status）+ 文本清洗防注入
- `agent/tools/mcp_server.py` — MCP 协议 stdio 服务端，供 OpenClaw 调用
- 路径已修复，测试全部通过

### 2. Agent 配置 ✅
- `agent/config/system-prompt.md` — 完整的 System Prompt（含红线约束、防注入声明）
- `agent/config/workflow.json` — 工作流 JSON 编排（5步流程）
- `agent/config/agent-config.json` — Agent 平台配置（TokenDance API）
- `agent/config/skill.json` — OpenClaw skill 注册文件

### 3. 网站 UI ✅
- `website/index.html` — 已重构为 AI HOT 风格（左侧导航 + 时间线信息流 + 右侧面板）
- 支持分类筛选、展开全文、今日热点榜、响应式布局
- 本地预览：`cd website && python3 -m http.server 8080`

### 4. 测试 ✅
- `tests/test_tools.py` — 7 项测试全部通过（读取、清洗、添加、去重、验证、Git、注入防御）
- `tests/sample-news.txt` — 测试新闻稿

### 5. 演示脚本 ✅
- `demo.py` — 端到端演示，模拟 Agent 全流程（可直接 `python3 demo.py` 运行）

### 6. RSS 采集器 ✅
- `fetch_news.py` — 支持 5 个源（HN AI、HN LLM、机器之心、InfoQ、36氪）
- HN 源验证通过，中文源依赖 RSSHub 可能超时

### 7. 文档 ✅
- `README.md` — 完整说明文档
- `PRESENTATION.md` — 演讲稿（约10分钟，含 Q&A）

### 8. Git 历史 ✅
```
0da82f8 feat: 重构 UI 为 AI HOT 风格 + 添加 RSS 采集器
b900e17 feat: 添加端到端演示脚本
9b1be51 publish: Anthropic 发布 Claude 4 系列模型
b3e3452 feat: 完成全部工程文件
f25010a init: 龙虾新闻 Agent 自动化发布系统
```

---

## 未完成

### 1. 新闻数据量不足 ❌
- 当前 `website/data/news.json` 只有 14 条新闻（6月14-17日）
- **需要补充**：扩充到约 30 天的数据（5月中旬到6月中旬），每天 2-3 条，总计约 60-80 条
- 新闻内容目前是基于真实公司/事件虚构的（HN 的几条标题是真的）
- 分类要均匀覆盖：AI 前沿、政策动态、产品发布、行业观察、研究论文、开源项目

### 2. 未推送到 GitHub ❌
- 本地 Git 仓库已建好，但没有 remote
- 需要创建 GitHub 仓库并 push

### 3. OpenClaw 实际对接未测试 ❌
- 配置文件都写好了，但没有实际在 OpenClaw 中运行过
- 需要在 OpenClaw 中导入 skill 并测试完整对话流程

---

## 关键文件路径

```
/Users/luoluo/Desktop/dragon-news-agent/
├── website/index.html          # 网站主页
├── website/data/news.json      # 新闻数据（唯一修改点）
├── agent/tools/tools.py        # 核心工具
├── agent/tools/mcp_server.py   # MCP 服务
├── agent/config/system-prompt.md  # System Prompt
├── agent/config/workflow.json  # 工作流
├── demo.py                     # 演示脚本
├── fetch_news.py               # RSS 采集器
├── tests/test_tools.py         # 测试
├── README.md                   # 说明文档
└── PRESENTATION.md             # 演讲稿
```

## 环境信息
- Python 3.12（pyenv）
- OpenClaw 已配置，API: TokenDance (DeepSeek V4 Flash)
- 本地服务器已在 8080 端口运行（可能需要重启）
- Git 仓库已初始化，无 remote

## 下一步建议
1. 先补充 news.json 到一个月的量（这是上次卡住的地方）
2. 创建 GitHub 仓库并 push
3. 在 OpenClaw 里实际跑一次完整流程
