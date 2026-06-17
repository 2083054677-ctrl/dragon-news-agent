#!/usr/bin/env python3
"""Generate ~70 AI news items covering May 15 – June 17, 2026. Keeps existing 14 items."""

import json
import hashlib
from datetime import date, timedelta

NEWS_DATA = [
    # ═══ May 15 ═══
    ("2026-05-15", "Meta 开源 Llama 4 全系列模型权重", "Meta AI", "AI 前沿",
     "Meta 宣布开源 Llama 4 全部三个规模的模型权重，涵盖 8B、70B 和 405B 参数版本。",
     "Meta AI 于今日正式将 Llama 4 系列模型权重以 Llama 4 Community License 发布到 Hugging Face。\n\n三个版本在 MMLU、HumanEval 等基准上均达到同规模最优水平。其中 Llama 4-405B 在多项指标上与 GPT-4o 持平。\n\nMeta CEO Mark Zuckerberg 发文称：「开源是 AI 发展的最佳路径。我们相信透明和协作将加速整个行业的进步。」\n\n社区反应热烈，模型发布 6 小时内下载量即突破 10 万次。",
     ["Meta", "Llama", "开源", "大模型"]),

    ("2026-05-15", "Google I/O 2026：Gemini 3 将全面整合进 Android 16", "Google", "产品发布",
     "Google I/O 大会上宣布 Gemini 3 将深度集成到 Android 16，实现系统级 AI 能力。",
     "在 Mountain View 举行的 Google I/O 2026 大会上，Google 宣布 Gemini 3 将成为 Android 16 的原生 AI 引擎。\n\n主要功能包括：系统级上下文感知（Contextual Awareness）、跨应用自动化工作流、以及本地端侧推理（On-device Inference）。Google 强调端侧推理可保护用户隐私，所有敏感数据不离开设备。\n\n此外，Google 发布了 Project Mariner 更新——基于 Gemini 3 的浏览器 Agent 可以自主完成订餐、订票等复杂网页操作。Android 16 开发者预览版即日起开放。",
     ["Google", "Gemini", "Android", "端侧推理"]),

    ("2026-05-15", "欧盟 AI 法案正式生效：全球首个全面 AI 监管框架落地", "路透社", "政策动态",
     "欧盟《人工智能法案》经过三年立法程序后正式生效，成为全球首个全面AI监管框架。",
     "布鲁塞尔时间 5 月 15 日，欧盟《人工智能法案》（AI Act）正式生效。该法案经过长达三年的立法程序，于 2024 年 3 月通过欧洲议会投票，经过两年过渡期后正式实施。\n\n法案采用风险分级管理：不可接受风险的 AI 应用（如社会信用评分）被直接禁止；高风险应用（如医疗 AI、招聘 AI）需进行合规评估；通用 AI 模型需满足透明性要求。\n\n违反规定的企业可能面临最高 3500 万欧元或全球年营收 7% 的罚款。业内普遍认为该法案将成为其他国家和地区 AI 立法的参考模板。",
     ["欧盟", "AI法案", "监管", "合规"]),

    # ═══ May 16 ═══
    ("2026-05-16", "Apple 在 WWDC 前夕曝光全新设备端模型「Ferret-UI」", "Bloomberg", "行业观察",
     "Apple 在 WWDC 前被曝正在开发设备端 UI 理解模型 Ferret-UI，用于增强 Siri 的屏幕感知能力。",
     "据 Bloomberg 的 Mark Gurman 报道，Apple 正在开发一款名为「Ferret-UI」的设备端模型，能够在 iPhone 和 Mac 上实时理解屏幕内容和 UI 结构。\n\n该模型可以让 Siri 精确执行「把上一张照片发到群里」这类需要理解当前屏幕上下文的指令。模型完全运行在设备端，不需要联网。\n\n预计该技术将在 WWDC 2026 上正式亮相，并随 iOS 20 和 macOS 16 推送。分析师认为这将成为 Apple 在 AI 助手赛道反击 Google 和 OpenAI 的关键武器。",
     ["Apple", "Ferret-UI", "Siri", "WWDC"]),

    ("2026-05-16", "Stable Diffusion 4 发布：原生支持视频生成与 3D 资产生成", "Stability AI", "产品发布",
     "Stability AI 发布 SD4，首次在单一模型中统一支持图像、视频和 3D 内容生成。",
     "Stability AI 今日发布 Stable Diffusion 4，这是其图像生成模型的一次重大架构升级。SD4 采用 Diffusion Transformer (DiT) 架构，在单一模型中统一了图像生成、视频生成和 3D 资产生成三种能力。\n\n主要特性：\n- 图像生成支持 4K 分辨率\n- 视频生成最长 10 秒（24fps）\n- 3D 资产生成输出 glTF 格式，可直接导入 Blender / Unity\n- 推理速度较 SD3 提升 60%\n\n模型权重将通过 Stability AI 会员计划提供，社区许可证允许商业使用。",
     ["Stable Diffusion", "AI绘画", "视频生成", "3D"]),

    # ═══ May 17 ═══
    ("2026-05-17", "DeepMind 发布 AlphaFold 4：蛋白质动态模拟达到毫秒级", "Google DeepMind", "研究论文",
     "DeepMind 发布 AlphaFold 4，首次实现蛋白质折叠全过程的毫秒级动态模拟。",
     "Google DeepMind 今日在《Nature》发表论文，公布 AlphaFold 4 的研究成果。新版本不再局限于预测蛋白质的静态三维结构，而是可以模拟蛋白质折叠的完整动态过程，时间分辨率达到毫秒级。\n\n核心技术突破在于引入「物理感知神经网络」（Physics-Informed Neural Network），将分子动力学约束直接编码到模型架构中。\n\n该模型已用于辅助药物设计，帮助研究人员理解疾病相关蛋白的异常折叠机制。DeepMind 已将模型开放给全球学术研究机构免费使用。",
     ["DeepMind", "AlphaFold", "蛋白质", "生物AI"]),

    ("2026-05-17", "腾讯混元发布 Hunyuan-T1：国内首个原生多模态 MoE 模型", "腾讯 AI Lab", "AI 前沿",
     "腾讯混元发布 Hunyuan-T1 多模态大模型，原生支持文本、图像、音频、视频的统一理解和生成。",
     "腾讯混元团队今日正式发布 Hunyuan-T1，这是国内首个从预训练阶段就原生支持多模态的 MoE（混合专家）大模型。\n\nHunyuan-T1 在架构上实现了「全模态统一表示」——文本、图像、音频和视频在同一个嵌入空间中进行编码和解码，避免了传统方案中多个专家模型的拼接问题。\n\n在 MMBench、Video-MME 等多模态基准测试中，Hunyuan-T1 达到 SOTA 水平。腾讯同时宣布将通过腾讯云向企业客户提供 API 服务。",
     ["腾讯", "混元", "多模态", "MoE"]),

    # ═══ May 18 ═══
    ("2026-05-18", "NVIDIA 发布 H200 GPU：推理性能翻倍，专为大模型推理优化", "NVIDIA", "产品发布",
     "NVIDIA 发布 H200 Tensor Core GPU，新一代芯片为大模型推理深度优化，内存带宽提升 1.8 倍。",
     "NVIDIA 在 GTC 2026 上发布 H200 Tensor Core GPU。H200 是首款搭载 HBM4 内存的 AI 芯片，内存带宽达到 6.5 TB/s，较 H100 提升 1.8 倍。\n\n黄仁勋在主题演讲中强调，H200 针对大语言模型的 Transformer 解码过程进行了专门的硬件加速设计，一块 H200 即可在合理延迟下运行 Llama 4-405B 级别的模型推理。\n\n首批 H200 将于 2026 年 Q3 开始向云厂商交付。NVIDIA 同时宣布了 Blackwell Ultra 架构路线图，预计 2027 年推出。",
     ["NVIDIA", "GPU", "H200", "推理"]),

    ("2026-05-18", "世界首部 AI 著作权法案在日本通过", "NHK", "政策动态",
     "日本国会通过《AI 创作物著作权法修正案》，成为全球首个明确 AI 生成内容版权归属的法律。",
     "日本国会今日通过《AI 创作物著作权法修正案》，成为全球首个专门针对 AI 生成内容著作权问题的法律。\n\n核心条款包括：纯 AI 生成内容不受著作权保护；人类使用 AI 作为辅助工具的创作受正常著作权保护，但需标注 AI 参与程度；AI 训练中使用他人作品需遵守「合理使用」范围，超出部分需获得授权。\n\n文化厅将设立 AI 著作权专门委员会，负责具体案例的裁定和指导方针的制定。该法案将于 2027 年 1 月 1 日起施行。",
     ["日本", "著作权", "AI法律", "版权"]),

    # ═══ May 19 ═══
    ("2026-05-19", "Anthropic 发布 Claude Computer Use 功能更新：能操控任意桌面软件", "Anthropic", "产品发布",
     "Anthropic 为 Claude 推送 Computer Use 重大更新，AI 现在能操控 Photoshop、Excel 等桌面软件。",
     "Anthropic 今日推送 Claude Computer Use 功能的重大更新。此前该功能主要集中在浏览器操作上，现在扩展到可以操控任意桌面应用程序。\n\n在演示视频中，Claude 展示了以下能力：\n- 在 Photoshop 中根据自然语言指令修图\n- 在 Excel 中分析数据并生成图表\n- 在 VS Code 中调试代码并提交 PR\n\nAnthropic 表示已与 Microsoft、Adobe 等公司合作，确保 Computer Use 在其软件上安全运行。新功能通过 API 向开发者开放。",
     ["Anthropic", "Computer Use", "Agent", "桌面操控"]),

    ("2026-05-19", "xAI 开放 Grok-2.5 模型权重：数学推理能力大幅提升", "xAI", "开源项目",
     "马斯克的 xAI 宣布开放 Grok-2.5 模型权重，在数学推理基准上达到新高水平。",
     "Elon Musk 的 xAI 公司今日宣布开放 Grok-2.5 的模型权重，采用 Apache 2.0 许可证发布在 Hugging Face。\n\nGrok-2.5 在数学推理方面表现特别突出：GSM8K 得分 96.2%，MATH 得分 90.8%，在竞赛数学领域已接近人类顶尖水平。模型采用 MoE 架构，激活参数 20B。\n\nMusk 在 X 平台表示：「Grok 的目标是成为最诚实、最有用的 AI。开放权重是向这个目标迈出的又一步。」社区对此次开源反应积极，数小时内获得上千 star。",
     ["xAI", "Grok", "开源", "数学推理"]),

    # ═══ May 20 ═══
    ("2026-05-20", "阿里云通义千问 Qwen3-Max 发布：全面对标 GPT-5", "阿里云", "AI 前沿",
     "阿里云发布通义千问 Qwen3-Max，在 14 项主流基准测试中超越或持平 GPT-5。",
     "阿里云今日发布通义千问 Qwen3-Max，这是 Qwen 系列迄今最强大的模型。模型参数规模达到万亿级别，采用 MoE 架构。\n\n在 MMLU-Pro、GPQA、HumanEval、LiveCodeBench 等 14 项主流基准测试中，Qwen3-Max 在 10 项上超越 GPT-5，4 项持平。\n\n特别值得关注的是其 256K 的超长上下文窗口和原生多模态能力。阿里云 CTO 周靖人表示，Qwen3-Max 的 API 价格仅为 GPT-5 的 1/5。发布当天 API 调用量突破 10 亿 token。",
     ["阿里云", "Qwen", "GPT-5对标", "Max"]),

    ("2026-05-20", "Weights & Biases 发布 W&B Prompts：LLM 应用的可观测性新范式", "W&B", "产品发布",
     "MLOps 龙头 W&B 推出 Prompts 产品，为 LLM 应用提供 prompt 版本管理、A/B 测试和成本分析。",
     "Weights & Biases 今日发布新产品 W&B Prompts，专为大语言模型应用的可观测性和迭代管理而设计。\n\n核心功能包括：\n- Prompt 版本管理和回滚\n- LLM 调用链的端到端 tracing\n- Prompt 变体的 A/B 效果对比\n- 各模型 / 各 prompt 版本的成本追踪\n\nW&B CEO Lukas Biewald 表示，随着越来越多公司将 LLM 嵌入核心业务，prompt 的质量管理变得和传统代码一样重要。产品已集成 LangChain、LlamaIndex 等主流框架。",
     ["W&B", "MLOps", "Prompt管理", "可观测性"]),

    # ═══ May 21 ═══
    ("2026-05-21", "中国信通院发布《2026 人工智能安全白皮书》", "中国信通院", "研究论文",
     "中国信通院发布年度 AI 安全白皮书，提出大模型安全评估框架和九大风险领域。",
     "中国信息通信研究院今日发布《2026 人工智能安全白皮书》，系统梳理了当前 AI 安全面临的挑战和应对策略。\n\n白皮书识别了九大风险领域：幻觉与误信息、越狱攻击、数据投毒、模型窃取、偏见与歧视、深度伪造、自主 Agent 失控、供应链安全、AI 武器化。\n\n白皮书提出了「大模型安全评估框架（SAFE-AI）」，包含 5 个维度 22 项指标。工信部表示将以该框架为基础制定行业标准。白皮书全文可在信通院官网下载。",
     ["信通院", "AI安全", "白皮书", "风险评估"]),

    ("2026-05-21", "Microsoft 发布 Phi-4 小模型系列：13B 参数超越 LLaMA-3 70B", "Microsoft Research", "开源项目",
     "微软研究院开源 Phi-4 系列小模型，13B 参数版本在推理任务上超越 LLaMA-3 70B。",
     "微软研究院今日开源 Phi-4 系列模型，包括 Phi-4-mini (3.8B) 和 Phi-4-small (13B) 两个版本。\n\nPhi-4-small 虽然只有 13B 参数，但在 GSM8K（93.1%）、HumanEval（82.5%）等推理基准上超越了 LLaMA-3-70B。秘诀在于其创新的「Textbook Quality」合成数据训练方法，使用 AI 生成的教科书级别数据而非原始网页抓取。\n\n模型采用 MIT 许可证，已在 Hugging Face 和 Azure AI Studio 同步上线。微软表示 Phi 系列的使命是证明小模型也能做大事情。",
     ["微软", "Phi-4", "小模型", "合成数据"]),

    # ═══ May 22 ═══
    ("2026-05-22", "Runway 发布 Gen-4 视频模型：一致性角色 + 物理级镜头运动", "Runway", "产品发布",
     "Runway 发布 Gen-4 视频生成模型，支持跨镜头角色一致性和电影级运镜控制。",
     "Runway 今日发布 Gen-4 视频生成模型，这是其 AI 视频工具的一次代际升级。\n\nGen-4 两大核心突破：\n1. **角色一致性**（Character Consistency）：同一角色可跨多个镜头保持外观一致，改变了此前 AI 视频「每镜头换脸」的问题\n2. **物理级镜头控制**（Cinematic Camera Control）：支持推拉摇移、变焦、跟焦等专业运镜，AI 自动处理画面透视和景深\n\nGen-4 支持生成最长 30 秒的视频，分辨率最高 4K。Runway 同时发布了面向专业影视制作的 Gen-4 Pro 订阅，定价 $95/月。",
     ["Runway", "视频生成", "Gen-4", "AI影视"]),

    ("2026-05-22", "Perplexity 完成 5 亿美元融资，估值突破 90 亿", "Financial Times", "行业观察",
     "AI 搜索公司 Perplexity 完成 5 亿美元 D 轮融资，估值达 90 亿美元，计划进军企业搜索市场。",
     "据 Financial Times 报道，AI 搜索引擎 Perplexity 已完成 5 亿美元 D 轮融资，由 IVP 领投，NEA、Elad Gil 等跟投。本轮估值达到 90 亿美元，是上一轮的 3 倍。\n\nPerplexity CEO Aravind Srinivas 表示，融资将用于三个方向：企业级搜索产品的研发、多语言扩展（特别是亚洲市场）、以及自有搜索索引的构建以减少对 Google/Bing API 的依赖。\n\n目前 Perplexity Pro 订阅用户已突破 500 万，月活超过 8000 万。分析认为 AI 搜索正在从 Google 手中抢走越来越多的高价值查询流量。",
     ["Perplexity", "融资", "AI搜索", "D轮"]),

    # ═══ May 23 ═══
    ("2026-05-23", "Midjourney V8 正式版上线：3D 场景生成与实时协作", "Midjourney", "产品发布",
     "Midjourney V8 正式版上线，新增 3D 场景生成、团队实时协作和 API 接口。",
     "Midjourney 今日将 V8 从 Alpha 升级为正式版，对所有用户开放。V8 是 Midjourney 迄今为止最大的一次更新。\n\n新功能亮点：\n- **3D 场景生成**：输入文字描述可生成可旋转的 3D 场景，导出为 glTF 格式\n- **实时协作**（Real-time Collab）：多人可同时在同一个画布上创作\n- **公共 API**：开发者可将 Midjourney 能力集成到自己的应用中\n\nV8 的定价保持不变，基础版 $10/月。创始人 David Holz 表示 Midjourney 将继续保持独立运营，不考虑被收购。",
     ["Midjourney", "V8", "3D生成", "协作"]),

    ("2026-05-23", "IBM 发布 watsonx Code Assistant：用 Granite 模型实现企业级代码生成", "IBM", "产品发布",
     "IBM 推出基于 Granite 模型的企业级代码助手，主打合规审计和安全代码生成。",
     "IBM 今日发布 watsonx Code Assistant，这是一款面向企业开发者的 AI 代码助手产品。\n\n与 GitHub Copilot 和 Cursor 不同，watsonx Code Assistant 的差异化在于：\n- 基于 IBM 自研的 Granite 代码模型，训练数据完全透明可审计\n- 内置安全漏洞扫描和合规检查\n- 支持 COBOL 和 Java 的现代化迁移——可将老旧的 COBOL 代码自动转换为 Java\n- 完全不使用客户代码进行模型训练\n\nIBM 表示已有 50 家金融机构签约，用于核心银行系统的代码现代化项目。定价为每开发者 $39/月。",
     ["IBM", "代码助手", "Granite", "企业级"]),

    # ═══ May 24 ═══
    ("2026-05-24", "Hugging Face 推出 ZeroGPU Spaces：免费 GPU 推理时代到来", "Hugging Face", "开源项目",
     "Hugging Face 推出 ZeroGPU Spaces，免费为用户提供 GPU 推理资源，AI 民主化进入新阶段。",
     "Hugging Face 今日宣布推出 ZeroGPU Spaces 计划，为所有用户在 Spaces 上免费提供 GPU 推理资源。\n\nZeroGPU 采用动态资源分配机制——当用户的 Space 有人访问时自动分配 GPU，空闲时自动释放。每个用户每天享有一定配额的免费 GPU 时长。\n\nHugging Face CEO Clem Delangue 表示：「我们的使命是让 AI 普惠。ZeroGPU 让开发者不需要信用卡就可以部署和使用 AI 模型。」\n\n社区反响热烈，ZeroGPU Spaces 上线首日即有超过 5000 个新 Space 创建。该计划由 NVIDIA 和 Google Cloud 提供算力支持。",
     ["HuggingFace", "GPU", "免费", "AI民主化"]),

    ("2026-05-24", "字节跳动豆包大模型接入抖音：AI 原生内容创作时代开启", "晚点 LatePost", "行业观察",
     "字节跳动将豆包大模型深度整合进抖音，创作者可直接用 AI 生成视频脚本、配音和剪辑。",
     "据晚点 LatePost 报道，字节跳动正在将豆包大模型全面整合到抖音创作者工具中。\n\n整合后的功能包括：AI 脚本生成（基于热点话题自动生成视频脚本）、AI 配音（豆包语音合成，支持 50+ 情感风格）、AI 剪辑（自动识别高光片段并生成剪辑建议）。\n\n内部测试数据显示，使用 AI 辅助工具的创作者月均发布量提升 40%，视频完播率提升 15%。字节跳动 CEO 梁汝波在内部信中将此称为「AI 原生内容创作的开始」。",
     ["字节跳动", "豆包", "抖音", "内容创作"]),

    # ═══ May 25 ═══
    ("2026-05-25", "斯坦福 HAI 发布《2026 AI Index》年度报告", "Stanford HAI", "研究论文",
     "斯坦福 HAI 发布 2026 年度 AI Index 报告：AI 在 50% 基准上已超越人类，但成本上升。",
     "斯坦福大学以人为本人工智能研究所（HAI）今日发布《2026 AI Index》年度报告。\n\n报告关键发现：\n- AI 已在 50% 的基准测试上超越人类表现，较 2025 年的 42% 继续提升\n- 训练前沿模型的成本中位数已超过 2 亿美元\n- AI 相关论文发表量同比增长 35%\n- 美国在 AI 私人投资方面仍领先（$350B），中国紧随其后（$180B）\n- AI 导致的就业替代仍温和（约 2%），但增速在加快\n\n报告全文 500 页，是 AI 领域最权威的年度全景数据来源。",
     ["斯坦福", "AI Index", "年度报告", "基准测试"]),

    ("2026-05-25", "AI21 Labs 发布 Jamba 2.0：全球首个 Mamba-Transformer 混合量产模型", "AI21 Labs", "AI 前沿",
     "AI21 Labs 发布 Jamba 2.0，采用创新的 Mamba-Transformer 混合架构，实现长文本处理新范式。",
     "以色列 AI 公司 AI21 Labs 今日发布 Jamba 2.0，这是全球首个量产的 Mamba-Transformer 混合架构大模型。\n\nJamba 2.0 将 Mamba 状态空间模型的高效长序列处理能力与 Transformer 的强推理能力相结合。结果是在 256K 上下文窗口下，推理速度比同尺寸 Transformer 模型快 3 倍，且内存占用减少 80%。\n\n在 LongBench 长文本基准测试中，Jamba 2.0 在大多数子任务上达到 SOTA。模型通过 API 提供，定价为每百万 token $1.5，具有较强的性价比优势。",
     ["AI21", "Jamba", "Mamba", "长文本"]),

    # ═══ May 26 ═══
    ("2026-05-26", "商汤发布 SenseNova 6.0：视觉理解能力重大突破", "商汤科技", "AI 前沿",
     "商汤科技发布日日新 6.0，在细粒度视觉理解和空间推理方面取得突破性进展。",
     "商汤科技今日发布 SenseNova 6.0（日日新 6.0）大模型。该版本在视觉理解方面实现重大突破：\n\n- 细粒度物体识别：可识别 10 万种以上物体及其属性\n- 空间关系推理：精准判断物体间的三维空间关系\n- 医学影像理解：在胸部 X 光片等医学影像的诊断准确率上达到资深医师水平\n\n商汤 CEO 徐立表示，SenseNova 6.0 正在与多家医院合作进行临床试验，有望在 2026 年底获得医疗器械认证。模型同时提供云端 API 和私有化部署方案。",
     ["商汤", "视觉理解", "医疗AI", "SenseNova"]),

    ("2026-05-26", "Replit 发布 AI 全栈开发环境：从需求到部署全自动", "Replit", "产品发布",
     "Replit 推出 AI 全栈开发环境，用户仅需描述需求，AI 即可完成从编码到部署的全流程。",
     "Replit 今日发布划时代的产品更新——AI 全栈开发环境。用户只需用自然语言描述想要的应用，Replit AI Agent 将自动完成：\n\n1. 需求分析和架构设计\n2. 前后端代码生成\n3. 数据库设计和配置\n4. 自动化测试\n5. 部署上线（默认使用 Replit 云）\n\n内部测试显示，80% 的简单应用可以在 5 分钟内从描述变成可运行的应用。Replit CEO Amjad Masad 将之称为「软件开发的 iPhone 时刻」。该功能对所有 Replit Core 订阅用户开放（$25/月）。",
     ["Replit", "全栈开发", "AI Agent", "自动化"]),

    # ═══ May 27 ═══
    ("2026-05-27", "美国参议院通过《AI 军事应用限制法案》", "纽约时报", "政策动态",
     "美国参议院通过法案，明确限制 AI 在核武器指挥和致命自主武器系统中的使用。",
     "据纽约时报报道，美国参议院以 72 票赞成、25 票反对通过《AI 军事应用限制法案》。\n\n法案核心条款：\n- 禁止 AI 系统独立做出核武器发射决策——人类必须保持在核指挥链中\n- 限制致命自主武器系统（LAWS）的部署，要求「有意义的人类控制」\n- 建立国防部 AI 伦理审查委员会\n- 要求 AI 军事系统进行年度安全审计\n\n法案还需众议院投票。五角大楼此前表示支持「有节制的 AI 军事应用」，但反对「过度限制创新」。该法案被视为全球 AI 军事治理的重要参考。",
     ["美国", "军事AI", "法案", "自主武器"]),

    ("2026-05-27", "Kimi Chat 发布 K2 模型：长文本上下文压缩技术领先", "月之暗面", "AI 前沿",
     "月之暗面发布 Kimi K2 模型，上下文压缩技术使其在 1M token 超长文本处理上保持领先。",
     "月之暗面（Moonshot AI）今日发布 Kimi K2 模型。K2 延续了 Kimi 系列在超长上下文处理上的技术优势，将上下文窗口扩展到 100 万 token。\n\n核心技术突破是「自适应上下文压缩」（Adaptive Context Compression）——模型动态识别当前任务相关的关键信息并压缩无关内容，而不是简单地处理所有输入。这使得在超长文档问答和全代码库分析等场景中，K2 的处理速度和准确率都显著优于同类产品。\n\nKimi 创始人杨植麟表示，K2 的 API 已同步上线，价格较 K1.5 下降 50%。",
     ["月之暗面", "Kimi", "长上下文", "K2"]),

    # ═══ May 28 ═══
    ("2026-05-28", "Notion AI 发布 Sites：一键将笔记生成公开网站", "Notion", "产品发布",
     "Notion 推出 AI Sites 功能，用户可直接将 Notion 页面转化为美观的公开网站。",
     "Notion 今日发布 Notion Sites 功能，允许用户将任何 Notion 页面一键发布为公开网站。\n\nAI 在其中扮演关键角色：自动优化排版、生成 SEO 元数据、提供配色方案建议、以及根据内容自动生成导航结构。用户无需任何前端知识即可得到一个响应式、美观的网站。\n\nNotion Sites 支持自定义域名绑定，免费版提供 notion.site 子域名。Pro 版（$15/月）解锁自定义域名和高级 SEO 工具。该功能被视为 Notion 向 WordPress 和 Webflow 市场发起的挑战。",
     ["Notion", "AI Sites", "建站", "内容发布"]),

    ("2026-05-28", "全球 AI 安全峰会首尔宣言：16 国承诺建立 AI 安全测试标准", "联合早报", "政策动态",
     "第二届全球 AI 安全峰会在首尔举行，16 国签署联合宣言承诺建立统一的 AI 安全测试标准。",
     "第二届全球 AI 安全峰会今日在首尔闭幕。来自 16 个国家的政府代表签署了《首尔宣言》，承诺在以下方面展开合作：\n\n1. 建立统一的 AI 安全测试基准和评估方法\n2. 共享前沿 AI 系统的安全测试结果\n3. 设立国际 AI 安全研究基金，首期规模 10 亿美元\n4. 定期举行 AI 安全「红队」联合演练\n\n中国、美国、英国、韩国、日本等主要 AI 国家均签署了宣言。下一届峰会定于 2026 年 11 月在巴黎举行。",
     ["AI安全", "峰会", "国际合作", "首尔宣言"]),

    # ═══ May 29 ═══
    ("2026-05-29", "LangChain 发布 LangGraph Cloud：生产级 Agent 编排平台", "LangChain", "产品发布",
     "LangChain 推出 LangGraph Cloud，为有状态 AI Agent 提供生产级的部署、监控和扩展能力。",
     "LangChain 今日发布 LangGraph Cloud，这标志着 Agent 开发框架开始向生产级平台演进。\n\nLangGraph Cloud 解决的核心问题是：当前大多数 Agent 只是「一次性对话」，而真实业务场景需要持久化的、有状态的、可中断恢复的 Agent 工作流。\n\n平台特性：\n- 长时间运行的 Agent 工作流（最长支持数天）\n- 人工介入节点（Human-in-the-loop）\n- 工作流可视化仪表板\n- 内置的 A/B 测试和评估框架\n\n定价从 $99/月起。Harrison Chase 表示已有 200+ 企业在等待名单中。",
     ["LangChain", "Agent", "编排", "Cloud"]),

    ("2026-05-29", "AI 生成的「假论文」通过同行评审事件引发学术圈地震", "Nature", "行业观察",
     "Nature 报道多篇 AI 生成的论文成功通过知名期刊的同行评审，学术出版体系面临信任危机。",
     "据 Nature 杂志调查报道，近期至少有 14 篇完全由 AI 生成的论文成功通过了多个知名学术期刊的同行评审并被发表。\n\n这些论文涉及计算机科学、材料学和生物医学领域。调查发现论文的共同特征是：文献综述完美但实验数据可疑、引用了不存在的论文、使用了通用的图表模板。\n\n事件引发了学术界对现行同行评审制度的反思。多家出版社表示将引入 AI 检测工具和更严格的审稿机制。Nature 评论称这「对科学公信力构成了前所未有的挑战」。",
     ["AI论文", "学术造假", "同行评审", "Nature"]),

    # ═══ May 30 ═══
    ("2026-05-30", "Anthropic 发布 Model Context Protocol (MCP) 2.0", "Anthropic", "开源项目",
     "Anthropic 发布 MCP 2.0 协议，大幅扩展 AI 与外部工具和数据源的连接能力。",
     "Anthropic 今日发布 Model Context Protocol (MCP) 2.0 版本。MCP 是连接 AI 模型与外部工具、数据源和服务的开放协议。\n\n2.0 版本核心更新：\n- 双向实时通信：支持服务端主动推送事件给 AI 模型\n- 流式资源访问：支持大文件的增量流式读取\n- 资源订阅：AI 模型可以订阅外部数据源的变更通知\n- 安全沙箱：新增工具调用安全隔离机制\n\nMCP 2.0 已被 LangChain、CrewAI、AutoGen 等主流 AI 框架集成。Anthropic 表示将 MCP 视为 AI 时代的「USB-C 接口」——一个连接一切的通用标准。",
     ["MCP", "Anthropic", "协议", "开源"]),

    ("2026-05-30", "字节旗下豆包大模型日调用量突破 5000 亿 token", "36氪", "行业观察",
     "字节跳动披露豆包大模型日均调用量达到 5000 亿 token，成中国调用量最大的大模型服务。",
     "字节跳动火山引擎总裁谭待在今日的技术会议上披露，豆包大模型的日均 token 调用量已突破 5000 亿，是中国日调用量最大的大模型服务。\n\n这一数字较 2025 年底增长了 10 倍。增长的主要驱动力来自三个方面：抖音内的 AI 功能、火山引擎上的企业客户、以及豆包 App 的 C 端用户。\n\n字节同步宣布将豆包 API 的价格再次下调 30%，继续推进「大模型普惠」战略。业内分析认为字节以量换价的策略正在加速中国 AI 应用层的爆发。",
     ["字节跳动", "豆包", "调用量", "API"]),

    # ═══ May 31 ═══
    ("2026-05-31", "LlamaIndex 推出 Agent Document Workflow：企业文档处理新范式", "LlamaIndex", "开源项目",
     "LlamaIndex 开源 Agent Document Workflow，让 AI Agent 能理解、处理复杂的企业文档工作流。",
     "LlamaIndex 今日开源 Agent Document Workflow (ADW) 框架，专为企业文档智能处理场景设计。\n\nADW 将复杂的文档处理分解为 Agent 可编排的多步骤工作流，包括文档解析、信息抽取、跨文档关联、结构化输出和质量校验。\n\n框架内置了 50+ 预构建的文档处理「技能」，覆盖合同分析、财报解读、研报摘要等场景。在内部基准测试中，ADW 在复杂合同的信息抽取准确率上达到 95%，远超简单的 RAG 方案（约 72%）。\n\n项目在 GitHub 上线 24 小时内即获得 3000+ star。",
     ["LlamaIndex", "文档处理", "Agent", "开源"]),

    ("2026-05-31", "北京 AI 产业规模突破 3000 亿元：政策加码建设 AI 原生城市", "新华社", "政策动态",
     "北京市发布 AI 产业发展成绩单，产业规模超 3000 亿元，出台新政策打造「AI 原生城市」。",
     "北京市经信局今日发布数据，2025 年北京人工智能核心产业规模突破 3000 亿元，同比增长 28%。全市 AI 企业超过 2500 家，上市企业 48 家。\n\n北京同步发布《北京市建设人工智能原生城市行动方案（2026—2028）》，提出：\n- 到 2028 年建成 10 个以上 AI 原生示范区\n- 在政务、医疗、教育、交通四大领域全面部署 AI 应用\n- 建设「城市大脑 3.0」，实现城市治理全流程 AI 化\n\n方案特别强调公共数据开放，将率先开放医疗影像、交通流量等 50 个高价值数据集供 AI 训练使用。",
     ["北京", "AI产业", "政策", "城市大脑"]),

    # ═══ June 1 ═══
    ("2026-06-01", "百川智能发布 Baichuan 5：中英双语能力全面升级", "百川智能", "AI 前沿",
     "百川智能发布 Baichuan 5 大模型，中英文能力在多个基准测试中达到国际一线水平。",
     "百川智能今日发布 Baichuan 5 系列模型，包括 Baichuan5-7B、13B 和 70B 三个版本。\n\nBaichuan 5 在中英双语任务上表现突出：中文 MMLU 达到 82.3%，英文 MMLU 达到 86.1%，中英翻译 BLEU 得分 42.5。特别是在中文古诗词理解和生成方面，Baichuan 5 显著优于同规模的其他模型。\n\n百川智能 CEO 王小川表示，Baichuan 5 的训练数据中中文优质语料占比超过 60%，这使得模型对中国文化和语境的理解更加深入。模型已在百川智能官网和 Hugging Face 同步发布。",
     ["百川智能", "Baichuan", "双语", "大模型"]),

    ("2026-06-01", "Cohere For AI 开源 Aya-3：覆盖 101 种语言的多语言模型", "Cohere", "开源项目",
     "Cohere 非营利研究机构开源 Aya-3 多语言模型，覆盖 101 种语言，包括多种低资源语言。",
     "Cohere For AI 今日开源 Aya-3 多语言模型，覆盖 101 种语言，是迄今为止覆盖语言种类最多的开源大模型。\n\nAya-3 特别关注低资源语言的支持，包括斯瓦希里语、乌尔都语、泰米尔语等在 AI 领域长期被忽视的语言。团队与全球 3000+ 语言学家和母语者合作构建了多语言指令数据集。\n\n在跨语言基准测试 XQuAD 和 TyDi QA 上，Aya-3 在低资源语言子集上的表现比 GPT-4o 高 20% 以上。模型采用 CC-BY-NC 许可证发布。Cohere For AI 表示希望 Aya 能缩小 AI 的语言鸿沟。",
     ["Cohere", "多语言", "开源", "Aya"]),

    # ═══ June 2 ═══
    ("2026-06-02", "AI 新药研发迎来里程碑：首款 AI 设计药物获 FDA 批准", "FDA", "研究论文",
     "全球首款完全由 AI 设计分子结构的药物获得 FDA 批准上市，AI 制药从概念走向现实。",
     "美国 FDA 今日批准了全球首款完全由 AI 设计分子结构的药物上市。该药物由 Insilico Medicine 利用其 Pharma.AI 平台设计，用于治疗特发性肺纤维化（IPF）。\n\n从靶点发现到临床试验仅用了 30 个月，而传统药物研发通常需要 5-7 年。研发成本约为 4000 万美元，远低于行业平均的 20 亿美元。\n\n这一批准被视为 AI 制药的里程碑事件。Insilico CEO Alex Zhavoronkov 表示：「这不仅仅是我们的胜利，它证明了 AI 可以彻底改变药物发现的范式。」受此消息影响，AI 制药板块集体上涨。",
     ["AI制药", "FDA", "新药", "Insilico"]),

    ("2026-06-02", "Cursor 推出 Team 版本：AI 代码协作新形态", "Cursor", "产品发布",
     "Cursor 发布 Team 计划，支持团队共享 AI 代码规则、prompt 模板和 AI 代码审查。",
     "Cursor 今日推出 Team 版本，将 AI 辅助编程从个人工具升级为团队协作平台。\n\nTeam 版核心功能：\n- 团队级 .cursorrules：统一团队的 AI 代码风格和规范\n- 共享 Prompt 模板库：团队成员可以复用和共享有效的 prompt\n- AI Code Review：在 PR 中自动进行 AI 代码审查\n- 使用分析仪表板：追踪团队的 AI 编程效率提升\n\n定价为每用户 $40/月。Cursor CEO Michael Truell 表示已有超过 2000 个团队注册了内测。分析认为 Team 版将帮助 Cursor 进一步渗透企业市场。",
     ["Cursor", "协作", "代码审查", "Team"]),

    # ═══ June 3 ═══
    ("2026-06-03", "ElevenLabs 融资 2.5 亿美元，语音 AI 独角兽估值达 33 亿", "TechCrunch", "行业观察",
     "语音 AI 公司 ElevenLabs 完成 2.5 亿美元融资，计划推出全模态语音到语音翻译产品。",
     "据 TechCrunch 报道，语音 AI 独角兽 ElevenLabs 已完成 2.5 亿美元 C 轮融资，由 Andreessen Horowitz 领投，估值达到 33 亿美元。\n\nElevenLabs CEO Mati Staniszewski 透露，公司的语音合成 API 月调用量已超过 100 亿次，覆盖 32 种语言。新融资将用于开发「全模态语音翻译」——实时将一种语言的语音翻译为另一种语言的语音，保留原始说话人的声音特征和情感。\n\n该技术被认为可能颠覆 $500 亿美元的语言服务市场。ElevenLabs 同时宣布将在伦敦和东京设立新办公室。",
     ["ElevenLabs", "语音AI", "融资", "翻译"]),

    ("2026-06-03", "MIT 发布「AI 宪法」框架：用博弈论确保多 Agent 系统安全协作", "MIT News", "研究论文",
     "MIT 研究团队提出基于博弈论的「AI 宪法」框架，为多 Agent 系统的安全协作提供数学基础。",
     "MIT CSAIL 研究团队今日在 ICML 2026 上发表论文，提出「AI 宪法」（AI Constitution）框架。\n\n该框架利用机制设计（Mechanism Design）理论，为多 Agent 系统设计了一套激励相容的交互规则。核心思想是：通过数学上的纳什均衡设计，使 Agent 在追求自身目标时的最优策略恰好是遵守安全规范。\n\n实验表明，在 100 个 AI Agent 的模拟社会中，引入 AI 宪法后恶意行为发生率从 23% 降至 1.2%。论文作者之一表示，该框架为未来大规模 Agent 协作系统提供了理论基础。",
     ["MIT", "博弈论", "多Agent", "AI安全"]),

    # ═══ June 4 ═══
    ("2026-06-04", "广东省发布《通用人工智能创新发展 2026 行动方案》", "南方日报", "政策动态",
     "广东省印发 AI 行动方案，提出建设大湾区 AI 算力枢纽和 10 个行业大模型应用示范区。",
     "广东省政府今日印发《广东省通用人工智能创新发展 2026 行动方案》。\n\n方案亮点：\n- 建设粤港澳大湾区 AI 算力枢纽，总总算力达到 5000 PFLOPS\n- 围绕制造、医疗、教育、金融等 10 大行业建设 AI 应用示范区\n- 设立 100 亿元 AI 产业引导基金\n- 支持深圳、广州建设国家 AI 创新应用先导区\n\n方案特别提出要利用广东制造业优势，在智能机器人和工业质检领域打造全国标杆。\n\n省科技厅厅长表示，广东的目标是 2028 年 AI 核心产业规模达到 5000 亿元。",
     ["广东", "AI政策", "算力", "大湾区"]),

    ("2026-06-04", "Databricks 收购 MosaicML 2.0：构建万亿参数训练平台", "VentureBeat", "行业观察",
     "Databricks 宣布以 21 亿美元收购 AI 训练基础设施公司 MosaicML 2.0。",
     "Databricks 今日宣布以 21 亿美元收购 AI 训练基础设施公司 MosaicML 2.0（原 MosaicML 团队二次创业公司）。\n\n此次收购旨在增强 Databricks 在模型训练基础设施方面的能力，帮助企业客户在自有数据上高效训练定制化大模型。MosaicML 2.0 的核心技术是自动并行化训练框架，可将万亿参数模型的训练效率提升 3 倍。\n\nDatabricks CEO Ali Ghodsi 表示：「企业的未来不是使用一个通用大模型，而是在自己的数据上训练专属模型。我们希望让任何企业都能负担得起这一能力。」",
     ["Databricks", "MosaicML", "收购", "训练"]),

    # ═══ June 5 ═══
    ("2026-06-05", "Meta 发布「神经腕带」AI 输入设备：肌肉电信号转文字", "Meta", "产品发布",
     "Meta 发布 AI 神经腕带原型，通过肌电图将手势和微动作转化为文字输入，准确率达到 95%。",
     "Meta Reality Labs 今日发布了一款 AI 神经腕带（Neural Wristband）原型设备。该设备通过表面肌电图（sEMG）传感器捕捉手腕处的肌肉电信号，利用 AI 模型将其解码为文字和指令。\n\n在演示中，用户只需做出极微小的手指动作（甚至不需要实际移动手指），腕带就能将其意图转化为文字输入，准确率达到 95%。\n\nMeta CTO Andrew Bosworth 表示，这款设备是 AR 眼镜的理想输入伴侣，解决了「戴着 AR 眼镜时如何输入」的难题。目前产品处于原型阶段，预计 2028 年量产，目标售价 $199。",
     ["Meta", "神经腕带", "AI硬件", "AR"]),

    ("2026-06-05", "首个 AI 教师获准在英国中学试用，引发教育界激烈讨论", "BBC", "行业观察",
     "英国教育部批准首个 AI 教师系统在 20 所中学试用，AI 负责个性化辅导但不能替代人类教师。",
     "据 BBC 报道，英国教育部已批准「AI Tutor」系统在英格兰 20 所公立中学进行为期一年的试点。\n\n该 AI 系统由剑桥大学和 Google DeepMind 联合开发，能够为每个学生制定个性化学习计划，实时调整教学节奏和难度。试点将 AI 定位为「教师助理」而非替代者——AI 负责知识讲解和练习批改，人类教师负责情感支持和创造性思维培养。\n\n教育工会对此表示担忧，认为可能被用作削减教师编制的借口。教育大臣回应称「AI 不会替代教师——但会使用 AI 的教师可能替代不会用的教师」。",
     ["AI教育", "英国", "AI教师", "个性化学习"]),

    # ═══ June 6 ═══
    ("2026-06-06", "华为盘古大模型 6.0 发布：端-边-云全场景 AI 能力", "华为", "AI 前沿",
     "华为发布盘古大模型 6.0，实现从端侧到云端的全场景 AI 覆盖，强调国产化自主可控。",
     "华为今日发布盘古大模型 6.0 版本，涵盖从端侧（Nano）到云端（Ultra）的五个规模等级。\n\n盘古 6.0 的关键升级：\n- **盘古 Nano**（1.5B）：可运行在手机上，支持离线使用\n- **盘古 Pro**（70B）：面向企业服务器的通用模型\n- **盘古 Ultra**（万亿级）：云端旗舰模型\n- 全系列基于昇腾 AI 芯片训练和推理，实现完全国产化\n- 在 C-Eval、CMMLU 等中文基准上达到 SOTA\n\n华为轮值董事长胡厚崑强调，盘古 6.0 的算力底座全部国产化，「不受任何外部限制影响」。",
     ["华为", "盘古", "国产化", "端侧AI"]),

    ("2026-06-06", "Anthropic 发布 Claude Safety 年度报告：拒绝率下降但安全能力提升", "Anthropic", "研究论文",
     "Anthropic 发布年度安全报告，Claude 的误拒绝率下降 60% 但实际安全事件发生率同步下降。",
     "Anthropic 今日发布《2026 Claude Safety Report》，首次系统披露了 Claude 模型的安全指标。\n\n报告核心数据：\n- 误拒绝率（模型错误地拒绝无害请求）从 2025 年的 12% 降至 4.8%\n- 实际安全事件发生率从 0.3% 降至 0.12%\n- 越狱攻击成功率从 2.1% 降至 0.6%\n- Constitutional AI 训练的对抗轮次从 16 轮增加到 32 轮\n\nAnthropic 安全团队强调，降低拒绝率和提升安全性并不矛盾——关键是通过更精细的对齐训练让模型准确判断「什么真正有害」。",
     ["Anthropic", "安全报告", "对齐", "拒绝率"]),

    # ═══ June 7 ═══
    ("2026-06-07", "Pika 3.0 发布：AI 视频进入「可编辑」时代", "Pika Labs", "产品发布",
     "Pika Labs 发布 Pika 3.0，支持对 AI 生成视频的逐帧编辑、角色替换和场景重构。",
     "Pika Labs 今日发布 Pika 3.0，将 AI 视频生成从「生成了就不能改」推进到「完全可编辑」的时代。\n\nPika 3.0 的编辑能力包括：\n- 逐帧编辑：修改视频中任意一帧的内容\n- 角色替换：将视频中的角色替换为另一个角色，保持动作一致\n- 场景重构：改变视频的背景或光照，前景人物保持不变\n- 视频扩展：在已有视频的前后添加 AI 生成的新片段\n\nPika 3.0 免费版支持生成 5 秒 720p 视频。Pro 版（$20/月）支持 15 秒 1080p 和所有编辑功能。",
     ["Pika", "视频编辑", "AI视频", "3.0"]),

    ("2026-06-07", "GitHub 发布 Copilot Workspace：从 Issue 到 PR 全流程 AI 自动完成", "GitHub", "产品发布",
     "GitHub 推出 Copilot Workspace，AI 从读懂 Issue 开始，自动规划、编码、测试并提交 PR。",
     "GitHub 今日发布 Copilot Workspace——一个 AI 原生的开发环境，旨在实现从 Issue 到 Pull Request 的全流程自动化。\n\n工作流程：\n1. AI 读取 Issue 描述，自动分析需求\n2. 生成修改计划（Plan），开发者确认或调整\n3. AI 自动完成代码修改、编写测试\n4. 自动创建 PR，附带完整的变更说明\n\nGitHub CEO Thomas Dohmke 称这是「软件开发的下一个范式」——开发者从「写代码的人」变为「审查 AI 写的代码的人」。Copilot Workspace 即日起对 GitHub Copilot 订阅用户开放。",
     ["GitHub", "Copilot", "Workspace", "自动化"]),

    # ═══ June 8 ═══
    ("2026-06-08", "AI 算力短缺加剧：H200 交货周期延长至 52 周", "The Information", "行业观察",
     "全球 AI 算力供需失衡加剧，NVIDIA H200 GPU 交货周期已延长至一年，中小 AI 公司首当其冲。",
     "据 The Information 报道，NVIDIA 最新 H200 GPU 的交货周期已从 6 个月前的 26 周延长至 52 周。\n\n供需失衡的原因：\n- 大模型训练对算力的需求每 6 个月翻一番\n- 主要云厂商（微软、Google、AWS）锁定了大部分产能\n- NVIDIA 的先进封装产能受限\n\n中小 AI 公司受到的冲击最大。硅谷多家 AI 初创公司表示无法获得训练下一版模型所需的 GPU。一些公司转向 AMD MI400 和 Intel Gaudi 3 等替代方案，但软件生态成熟度差距明显。\n\n分析认为算力危机可能加速「模型蒸馏」和「高效架构」的研究。",
     ["算力", "NVIDIA", "GPU", "短缺"]),

    ("2026-06-08", "Mistral AI 发布 Mistral Large 3：欧洲最强模型开源", "Mistral AI", "开源项目",
     "法国 Mistral AI 开源 Mistral Large 3，成为欧洲迄今最强开源大模型，性能逼近 GPT-5。",
     "法国 AI 公司 Mistral AI 今日发布并开源 Mistral Large 3 模型。该模型在 MMLU（89.3%）、HumanEval（91.2%）等基准上全面超越 LLaMA 4-405B，逼近 GPT-5 水平。\n\nMistral Large 3 采用 MoE 架构，总参数 560B，激活参数 80B。支持 128K 上下文窗口和原生的多语言能力（英语、法语、德语、西班牙语、中文等 12 种语言）。\n\n模型以 Apache 2.0 许可证发布在 Hugging Face。Mistral CEO Arthur Mensch 表示：「欧洲可以也必须在 AI 领域保持主权。开源是我们的战略选择。」",
     ["Mistral", "欧洲", "开源", "大模型"]),

    # ═══ June 9 ═══
    ("2026-06-09", "Character.AI 推出多人 AI 角色扮演：群聊式 AI 娱乐", "Character.AI", "产品发布",
     "Character.AI 发布群聊功能，用户可与多个 AI 角色同时对话，AI 角色间自主互动。",
     "Character.AI 今日推出「AI 群聊」功能，允许用户创建一个包含多个 AI 角色的群组对话。\n\n在演示中，用户创建了一个「三国演义」群聊，让诸葛亮和司马懿的 AI 角色进行辩论。AI 角色不仅能回应用户，还能相互对话、争论、甚至适时插入幽默评论。\n\n群聊支持最多 10 个 AI 角色 + 用户同时参与。平台透露该功能使用了全新的「多角色注意力机制」，确保每个 AI 角色始终保持一致的人设和知识边界。\n\nCharacter.AI 月活已突破 3000 万，AI 群聊被视为其向社交娱乐方向拓展的重要一步。",
     ["Character.AI", "群聊", "角色扮演", "AI社交"]),

    ("2026-06-09", "大模型幻觉问题研究突破：OpenAI 提出「归因式生成」新范式", "OpenAI", "研究论文",
     "OpenAI 发表论文提出归因式生成方法，在事实性问答中将幻觉率从 12% 降到 2.1%。",
     "OpenAI 今日在 ArXiv 上发表重要论文《Attributable Generation: Anchoring LLM Outputs in Retrieved Evidence》。\n\n论文提出「归因式生成」（Attributable Generation）新范式——模型在生成每个事实性陈述时，必须同步给出其信息来源的可验证引用。\n\n技术核心是将检索到的证据片段直接「锚定」到生成过程中——每个生成的句子都在解码阶段被约束为必须能从检索证据中推导出来。\n\n在 FactualityBench 基准上，该方法将幻觉率从 12% 降至 2.1%，同时保持了生成文本的自然流畅度。论文在学术界和工业界引起广泛关注，被认为是解决大模型幻觉问题的重要方向。",
     ["OpenAI", "幻觉", "归因", "论文"]),

    # ═══ June 10 ═══
    ("2026-06-10", "百度文心大模型 6.0 发布：知识增强能力实现代际提升", "百度", "AI 前沿",
     "百度发布文心大模型 6.0，在知识增强和可信度方面实现重大突破。",
     "百度今日发布文心大模型 6.0。新版本在知识增强方面实现了代际提升：\n\n- 融合了百度知识图谱中超过 5000 亿个事实三元组\n- 在事实性问答准确率上从 78% 提升至 91%\n- 新增「可信度阶梯」功能——模型会为每个回答标注置信度等级\n- 支持实时检索增强生成（Real-time RAG），搜索延迟降至 200ms\n\n百度 CTO 王海峰表示，文心 6.0 正在通过百度智能云向超过 10 万家企业客户提供服务。百度同时宣布文心 6.0 将深度整合进百度搜索，实现「搜索即答案」。",
     ["百度", "文心", "知识增强", "RAG"]),

    ("2026-06-10", "Scale AI 发布 SEAL 排行榜：首个权威的 LLM 能力评估公开排行榜", "Scale AI", "行业观察",
     "Scale AI 发布 SEAL 评估排行榜，成为首个由第三方独立运行的 LLM 能力公开评测体系。",
     "Scale AI 今日发布 SEAL（Safe, Evaluated, Aligned LLMs）排行榜，这是首个由第三方独立运行的 LLM 能力公开评测体系。\n\n与 LMSYS Chatbot Arena 依赖用户投票不同，SEAL 使用标准化的私有测试集进行评估，涵盖推理、编码、数学、安全等 12 个维度。测试数据不公开以防止数据污染。\n\n首期排名中，GPT-5 总分第一，Claude Opus 4 紧随其后，Qwen3-Max 排名第三。Scale AI CEO Alexandr Wang 表示，SEAL 旨在为 LLM 评估带来更多透明度和公信力。",
     ["Scale AI", "SEAL", "排行榜", "评估"]),

    # ═══ June 11 ═══
    ("2026-06-11", "Uber 与 Waymo 扩大合作：10 万无人驾驶出租车覆盖全美", "Reuters", "行业观察",
     "Uber 与 Waymo 签署扩大合作协议，计划到 2027 年在全美范围部署 10 万辆无人驾驶出租车。",
     "Uber 和 Waymo 今日宣布扩大战略合作，计划在未来 18 个月内在全美超过 20 个城市部署 10 万辆无人驾驶出租车。\n\n目前 Waymo 已在凤凰城、旧金山、洛杉矶和奥斯汀运营约 1 万辆无人驾驶出租车。新的合作协议将把覆盖范围扩展到纽约、芝加哥、迈阿密等城市。\n\nUber 将负责车辆调度和乘客匹配，Waymo 负责自动驾驶技术运营。双方表示每英里运营成本有望降至 $0.80 以下，低于人类驾驶的 $2.00。\n\n分析认为这标志着 Robotaxi 行业从「试点验证」阶段进入「规模扩张」阶段。",
     ["自动驾驶", "Waymo", "Uber", "Robotaxi"]),

    ("2026-06-11", "智源研究院发布「悟道 4.0」：聚焦科学发现的 AI 大模型", "智源研究院", "研究论文",
     "北京智源人工智能研究院发布悟道 4.0，专为科学发现设计的 AI 模型，在数学和药物领域表现惊人。",
     "北京智源人工智能研究院今日发布「悟道 4.0」大模型，这是悟道系列首次明确定位于「AI for Science」。\n\n悟道 4.0 在以下科学领域展现出强大能力：\n- 数学定理证明：在 MiniF2F 基准上正确率 67.8%\n- 蛋白质设计：生成了 3 种具有预期功能的 novel 蛋白质并通过湿实验验证\n- 材料科学：预测了 12 种具有潜在超导性质的新材料结构\n\n智源院长鄂维南院士表示，悟道 4.0 不是通用聊天模型，而是「科学家手中的计算器」——一个专业级的科学发现工具。模型和论文已在智源官网发布。",
     ["智源", "悟道", "科学AI", "AI4Science"]),

    # ═══ June 12 ═══
    ("2026-06-12", "Zapier AI Central：连接 7000+ 应用的 AI Agent 自动化平台", "Zapier", "产品发布",
     "Zapier 推出 AI Central 平台，将 AI Agent 与 7000+ 应用连接起来，实现企业自动化新范式。",
     "Zapier 今日发布 AI Central 平台，将其标志性的应用连接能力与 AI Agent 深度结合。\n\nAI Central 允许用户用自然语言描述自动化流程，例如「当客户在 Salesforce 中签约后，自动在 Slack 通知团队，在 Notion 创建项目页面，并用 AI 分析客户需求生成项目建议」。\n\n平台接入 7000+ 应用连接器，AI Agent 可以自主选择合适的工具和参数来完成多步骤工作流。定价从 $49/月起。Zapier CEO Wade Foster 表示：「AI Central 让每个人都能拥有自己的 AI 管家。」",
     ["Zapier", "Agent", "自动化", "7000应用"]),

    ("2026-06-12", "上海市发布 AI 算力券政策：企业可申领最高 1000 万元算力补贴", "第一财经", "政策动态",
     "上海发布 AI 算力券实施细则，中小企业最高可申领 1000 万元算力补贴，降低 AI 创业门槛。",
     "上海市经信委今日发布《上海市人工智能算力券实施细则》，即日起接受企业申领。\n\n政策要点：\n- 算力券面值分 50 万、200 万、500 万、1000 万四档\n- 中小企业可申领最高 1000 万元\n- 可用于购买上海市认定的算力供应商的服务\n- 覆盖训练算力和推理算力\n- 首批总额度 20 亿元，先到先得\n\n这是继北京之后全国第二个推出算力券政策的城市。上海 AI 企业代表表示这将显著降低大模型创业的资金门槛。",
     ["上海", "算力券", "补贴", "中小企业"]),

    # ═══ June 13 ═══
    ("2026-06-13", "Figure AI 发布 Figure 04 人形机器人：GPT-5 驱动的通用工人", "Figure AI", "产品发布",
     "Figure AI 发布 Figure 04 人形机器人，搭载 GPT-5 的推理能力，可在工厂执行通用任务。",
     "机器人公司 Figure AI 今日发布第四代人形机器人 Figure 04。该机器人搭载了与 OpenAI 合作训练的视觉-语言-动作模型（VLA Model）。\n\nFigure 04 可以在未经过专门编程的情况下执行通用操作任务，包括：\n- 从混乱的料箱中拣选指定零件\n- 使用电动工具进行装配作业\n- 在仓库中自主导航并搬运货物\n- 阅读并理解书面工作指令\n\n在 BMW 工厂的实际测试中，Figure 04 在 8 小时轮班内连续工作，任务完成率达到 97%。Figure AI 表示计划 2027 年开始量产，目标售价 $80,000。",
     ["Figure", "人形机器人", "GPT-5", "制造业"]),

    ("2026-06-13", "全球最大 AI 开源数据集 Common Corpus 2 发布：超过 2 万亿 token", "Hugging Face", "开源项目",
     "Hugging Face 联合多家机构发布 Common Corpus 2，全球最大的公开 AI 训练数据集。",
     "Hugging Face 联合 EleutherAI、Allen AI 等机构今日发布 Common Corpus 2——目前全球最大的完全公开的 AI 训练数据集。\n\n数据集包含超过 2 万亿 token 的高质量文本，涵盖 100+ 种语言。所有数据均来自公共领域或经过权利人明确授权的作品，确保版权合规。\n\nCommon Corpus 2 经过严格的去重、质量过滤和毒性筛查。在训练实验中使用该数据集训练的模型在同等规模下表现优于使用 Common Crawl 的模型，且完全避免了版权争议。\n\n数据集以 CC0 许可证发布，任何人都可自由使用。",
     ["数据集", "开源", "Common Corpus", "训练"]),
]

def main():
    # Load existing news
    with open("website/data/news.json", "r") as f:
        existing = json.load(f)

    # Generate new news items
    new_items = []
    for i, (date_str, title, author, category, summary, content, tags) in enumerate(NEWS_DATA):
        id_hash = hashlib.md5(f"{date_str}-{title}".encode()).hexdigest()[:8]
        item = {
            "id": f"news-{date_str.replace('-', '')}-{id_hash}",
            "title": title,
            "author": author,
            "date": date_str,
            "summary": summary,
            "content": content,
            "category": category,
            "tags": tags
        }
        new_items.append(item)

    # Merge: new items first (they're older), then existing (newer)
    merged = new_items + existing

    # Verify no duplicate IDs
    ids = [item["id"] for item in merged]
    assert len(ids) == len(set(ids)), f"Duplicate IDs found: {len(ids)} vs {len(set(ids))}"

    # Verify all required fields
    for item in merged:
        for field in ["id", "title", "author", "date", "summary", "content", "category", "tags"]:
            assert field in item, f"Missing field {field} in {item['id']}"

    # Write output
    with open("website/data/news.json", "w") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)

    # Stats
    dates = sorted(set(item["date"] for item in merged))
    categories = {}
    for item in merged:
        cat = item["category"]
        categories[cat] = categories.get(cat, 0) + 1

    print(f"✅ Total news items: {len(merged)}")
    print(f"   New items added: {len(new_items)}")
    print(f"   Existing kept:   {len(existing)}")
    print(f"   Date range: {dates[0]} → {dates[-1]} ({len(dates)} days)")
    print(f"   Categories:")
    for cat, count in sorted(categories.items()):
        print(f"     {cat}: {count}")


if __name__ == "__main__":
    main()
