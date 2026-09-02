# LLM Infrastructure & Local AI

| # | Repo | Stars | Ne İşe Yarar? | GitHub |
|---|------|-------|--------------|--------|
| 1 | **llmfit** | 600 | Donanıma göre uygun local LLM modellerini gösteriyor | [link](https://github.com/AlexsJones/llmfit) |
| 2 | **ollama** | 130,000 | Açık kaynak modelleri yerel çalıştırma | [link](https://github.com/ollama/ollama) |
| 3 | **freellmapi** | 320 | Duzinelerce ucretsiz LLM katmanini tek API de birlestiren router; otomatik yonlendirme + fallback | [link](https://github.com/tashfeenahmed/freellmapi) |
| 4 | **llama3** | 77,000 | Meta'nın Llama 3 model ailesi — 8B/70B/405B ağırlıkları, fine-tune rehberleri, inference örnekleri | [link](https://github.com/meta-llama/llama3) |
| 5 | **metaseq** | 13,000 | Meta'nın büyük ölçekli dil modeli araştırma çerçevesi; OPT modeli dahil | [link](https://github.com/facebookresearch/metaseq) |
| 6 | **bert** | 38,000 | Google'ın BERT modeli — NLP'de devrim yaratan orijinal pre-training kodu ve ağırlıklar | [link](https://github.com/google-research/bert) |
| 7 | **google-research** | 35,000 | Google Research'ün yüzlerce araştırma projesini barındıran ana repo: BERT, T5, ViT, Imagen ve daha fazlası | [link](https://github.com/google-research/google-research) |
| 8 | **automl** | 6,200 | Google AutoML araçları — NAS (Neural Architecture Search), verimli model tasarımı | [link](https://github.com/google/automl) |
| 9 | **starter-applets (Gemini)** | 1,100 | Google Gemini API ile sıfırdan uygulama örnekleri — multimodal, chat, function calling | [link](https://github.com/google-gemini/starter-applets) |
| 10 | **lupine** | 2,005 | GPU over IP köprüsü — uzak GPU'yu yerel CUDA cihazı gibi kullanma; multi-GPU workload dağıtımı | [link](https://github.com/iot-lab/lupine) |
| 11 | **gemini-web2api** | 823 | Gemini web arayüzünü OpenAI uyumlu API'ye dönüştürür — tek Python dosyası, sıfır bağımlılık, streaming + tool calling + 20K token bağlam; ayda $20-50 API maliyeti sıfıra inebilir | [link](https://github.com/Sophomoresty/gemini-web2api) |
| 12 | **pipeshub-ai** | 4,500 | Aciklanabilir kurumsal arama + bilgi grafigi (knowledge graph). Belge, sohbet, kod ve is verilerini semantik olarak indeksler; seffaf AI arama sonuclari. Self-hosted, SOC2 uyumlu | [link](https://github.com/pipeshub-ai/pipeshub-ai) |
| 13 | **free-coding-models** | 3,400 | 170+ ücretsiz kodlama modelini benchmark eder ve yükler. Model performans karşılaştırması, otomatik kurulum ve kod görevleri için en iyi model seçimi. | [link](https://github.com/vava-nessa/free-coding-models) |
| 14 | **ai-engineering-toolkit** | 5,800 | LLM mühendisliği için 100+ kütüphane seçkisi. Vektör veritabanları, embedding, RAG, fine-tuning, evaluation, deployment ve observability araçları kategorize edilmiş. | [link](https://github.com/Sumanth077/ai-engineering-toolkit) |
| 15 | **LLMRouter** | — | Her sorgu için en uygun LLM'i dinamik olarak seçer. Maliyet, hız ve kalite dengesini otomatik optimize eder. Groq→HuggingFace→local gibi kendi routing mantığını özelleştirmeye alternatif; kendi arayüzünle lokal + bulut LLM'leri tek noktadan yönet. | [link](https://github.com/ulab-uiuc/LLMRouter) |
| 16 | **headroom** | — | Claude Code, Codex, Cursor, Aider, Copilot icin token sikiştirma proxy. Tool ciktilari, loglar, RAG verisi, dosyalar, konusma gecmisini modele gondermeden once optimize eder. Bazi senaryolarda %90+ token tasarrufu. Claude Code destegi, MCP entegrasyonu, cross-agent memory, reversible compression, proxy modu. Yeni model degil — mevcut modelleri daha verimli kullanma. | [link](https://github.com/headroomlabs-ai/headroom) |
| 17 | **mlx-audio** | 980 | Apple MLX framework tabanlı TTS (metin-ses), STT (konuşma-metin) ve STS (konuşma-konuşma) kütüphanesi. Apple Silicon üzerinde verimli ses analizi. | [link](https://github.com/Blaizzy/mlx-audio) |
| 18 | **Orpheus-TTS** | 5200 | Llama-3b omurgası üzerine kurulu SOTA açık kaynak TTS sistemi. İnsan benzeri konuşma kalitesi, çok dilli destek, gerçek zamanlı streaming. Apache-2.0 lisanslı. | [link](https://github.com/canopyai/Orpheus-TTS) |
| 19 | **awesome-ai-voice** | 1800 | Açık kaynak TTS, ses klonlama ve müzik üretim modellerinin kapsamlı listesi. Orpheus, Kokoro, Chatterbox ve daha fazlası için tek referans noktası. | [link](https://github.com/wildminder/awesome-ai-voice) |
| 20 | **gentle-ai** | 4011 | Go ile yazilmis hafif AI asistan | [link](https://github.com/Gentleman-Programming/gentle-ai) |
| 21 | **FastGPT** | 28481 | LLM tabanlı bilgi tabanı platformu — iş akışı, Q&A, dataset yönetimi | [link](https://github.com/labring/FastGPT) |
| 22 | **llm_wiki** | 11779 | Belgelerini birbirine bağlı kişisel bilgi tabanına dönüştüren masaüstü aracı | [link](https://github.com/nashsu/llm_wiki) |
| 23 | **OpenKB** | 2079 | Hafif açık kaynak LLM bilgi tabanı — minimal MVP için ideal | [link](https://github.com/VectifyAI/OpenKB) |
| 24 | **ramalama** | 2961 | RamaLama is an open-source developer tool that simplifies the local serving of AI models from any source and facilitates their use for inference in production, all through the familiar language of containers. | [link](https://github.com/containers/ramalama) |
| 25 | **OmniRoute** | 20088 | MIT lisanslı, yerel/self-hosted birleşik AI gateway ve model yönlendiricisi. OpenAI uyumlu tek endpoint üzerinden çok sayıda sağlayıcı/modeli birleştirir; otomatik fallback, yönlendirme stratejileri, kota ve maliyet görünürlüğü, bağlam sıkıştırma, MCP/A2A ve kullanım analitiği sunar. v3.8.49 paketi Node.js 22.22.2+ gerektirir. | [link](https://github.com/diegosouzapw/OmniRoute) |
| 26 | **Qwen3** | 27426 | Alibaba Qwen3 LLM serisi — Dense + MoE (0.6B–235B), thinking/non-thinking mod, Ollama destekli, Qwen3-2507 güncel sürüm | [link](https://github.com/QwenLM/Qwen3) |
| 27 | **tensorflow** | 196592 | An Open Source Machine Learning Framework for Everyone | [link](https://github.com/tensorflow/tensorflow) |
| 28 | **AutoGPT** | 185741 | AutoGPT is the vision of accessible AI for everyone, to use and to build on. Our mission is to provide the tools, so tha | [link](https://github.com/Significant-Gravitas/AutoGPT) |
| 29 | **prompts.chat** | 166486 | f.k.a. Awesome ChatGPT Prompts. Share, discover, and collect prompts from the community. Free and open source — self-hos | [link](https://github.com/f/prompts.chat) |
| 30 | **transformers** | 163121 | 🤗 Transformers: the model-definition framework for state-of-the-art machine learning models in text, vision, audio, and | [link](https://github.com/huggingface/transformers) |
| 31 | **firecrawl** | 157819 | The API to search, scrape, and interact with the web at scale. 🔥 | [link](https://github.com/firecrawl/firecrawl) |
| 32 | **open-webui** | 147224 | User-friendly AI Interface (Supports Ollama, OpenAI API, ...) | [link](https://github.com/open-webui/open-webui) |
| 33 | **awesome-llm-apps** | 128717 | 100+ AI Agents, Agent Skills and RAG Apps - Free and Open Source. | [link](https://github.com/Shubhamsaboo/awesome-llm-apps) |
| 34 | **pytorch** | 102055 | Tensors and Dynamic neural networks in Python with strong GPU acceleration | [link](https://github.com/pytorch/pytorch) |
| 35 | **LLMs-from-scratch** | 100106 | Implement a ChatGPT-like LLM in PyTorch from scratch, step by step | [link](https://github.com/rasbt/LLMs-from-scratch) |
| 36 | **graphify** | 98302 | Turn any codebase, with its docs, SQL schemas, configs, and PDFs, into a queryable knowledge graph. A /graphify skill fo | [link](https://github.com/Graphify-Labs/graphify) |
| 37 | **caveman** | 94302 | 🪨 why use many token when few token do trick — Claude Code skill that cuts 65% of tokens by talking like caveman | [link](https://github.com/JuliusBrussee/caveman) |
| 38 | **ML-For-Beginners** | 88727 | 12 weeks, 26 lessons, 52 quizzes, classic Machine Learning for all | [link](https://github.com/microsoft/ML-For-Beginners) |
| 39 | **vllm** | 87582 | A high-throughput and memory-efficient inference and serving engine for LLMs | [link](https://github.com/vllm-project/vllm) |
| 40 | **cs-video-courses** | 82818 | List of Computer Science courses with video lectures. | [link](https://github.com/Developer-Y/cs-video-courses) |
| 41 | **llm-course** | 81306 | Course to get into Large Language Models (LLMs) with roadmaps and Colab notebooks. | [link](https://github.com/mlabonne/llm-course) |
| 42 | **netdata** | 79902 | The fastest path to AI-powered full stack observability, even for lean teams. | [link](https://github.com/netdata/netdata) |
| 43 | **d2l-zh** | 79285 | 《动手学深度学习》：面向中文读者、能运行、可讨论。中英文版被70多个国家的500多所大学用于教学。 | [link](https://github.com/d2l-ai/d2l-zh) |
| 44 | **deer-flow** | 78155 | An open-source long-horizon SuperAgent harness that researches, codes, and creates. With the help of sandboxes, memories | [link](https://github.com/bytedance/deer-flow) |
| 45 | **tesseract** | 75627 | Tesseract Open Source OCR Engine (main repository) | [link](https://github.com/tesseract-ocr/tesseract) |
| 46 | **rtk** | 73831 | CLI proxy that reduces LLM token consumption by 60-90% on common dev commands. Single Rust binary, zero dependencies | [link](https://github.com/rtk-ai/rtk) |
| 47 | **LlamaFactory** | 73608 | Unified Efficient Fine-Tuning of 100+ LLMs & VLMs (ACL 2024) | [link](https://github.com/hiyouga/LlamaFactory) |
| 48 | **awesome-scalability** | 72813 | The Patterns of Scalable, Reliable, and Performant Large-Scale Systems | [link](https://github.com/binhnguyennus/awesome-scalability) |
| 49 | **learn-claude-code** | 72642 | Bash is all you need -  A nano claude code–like 「agent harness」, built from 0 to 1 | [link](https://github.com/shareAI-lab/learn-claude-code) |
| 50 | **OpenBB** | 71164 | Open Data Platform for analysts, quants and AI agents. | [link](https://github.com/OpenBB-finance/OpenBB) |
| 51 | **MetaGPT** | 69580 | 🌟 The Multi-Agent Framework: First AI Software Company, Towards Natural Language Programming | [link](https://github.com/FoundationAgents/MetaGPT) |
| 52 | **hello-agents** | 69428 | 📚 《从零开始构建智能体》——从零开始的智能体原理与实践教程 | [link](https://github.com/datawhalechina/hello-agents) |
| 53 | **unsloth** | 69068 | Unsloth is a local UI for training and running Gemma 4, Qwen3.6, DeepSeek, Kimi, GLM and other models. | [link](https://github.com/unslothai/unsloth) |
| 54 | **annotated_deep_learning_paper_implementations** | 67240 | 🧑‍🏫 60+ Implementations/tutorials of deep learning papers with side-by-side notes 📝; including transformers (original, x | [link](https://github.com/labmlai/annotated_deep_learning_paper_implementations) |
| 55 | **scikit-learn** | 66816 | scikit-learn: machine learning in Python | [link](https://github.com/scikit-learn/scikit-learn) |
| 56 | **keras** | 64187 | Deep Learning for humans | [link](https://github.com/keras-team/keras) |
| 57 | **anything-llm** | 64067 | Stop renting your intelligence. Own it with AnythingLLM. Everything you need for a powerful local-first agent experience | [link](https://github.com/Mintplex-Labs/anything-llm) |
| 58 | **mem0** | 62031 | Universal memory layer for AI Agents | [link](https://github.com/mem0ai/mem0) |
| 59 | **system_prompts_leaks** | 61309 | Extracted system prompts from Anthropic - Claude Fable 5, Opus 5, Claude Design, Claude Code. OpenAI - ChatGPT GPT-5.6-S | [link](https://github.com/asgeirtj/system_prompts_leaks) |
| 60 | **TrendRadar** | 61003 | ⭐AI-driven public opinion & trend monitor with multi-platform aggregation, RSS, and smart alerts.🎯 告别信息过载，你的 AI 舆情监控助手与热 | [link](https://github.com/sansan0/TrendRadar) |
| 61 | **ultralytics** | 60018 | Ultralytics YOLO26, YOLO11, YOLOv8 — object detection, instance segmentation, semantic segmentation, image classificatio | [link](https://github.com/ultralytics/ultralytics) |
| 62 | **context7** | 59965 | Context7 Platform -- Up-to-date code documentation for LLMs and AI code editors | [link](https://github.com/upstash/context7) |
| 63 | **daily_stock_analysis** | 59503 | LLM 驱动的多市场股票智能分析系统：多源行情、实时新闻、决策看板与自动推送，支持零成本定时运行。  LLM-powered multi-market stock analysis system with multi-source mark | [link](https://github.com/ZhuLinsen/daily_stock_analysis) |
| 64 | **llm-app** | 58946 | Ready-to-run cloud templates for RAG, AI pipelines, and enterprise search with live data. 🐳Docker-friendly.⚡Always in sy | [link](https://github.com/pathwaycom/llm-app) |
| 65 | **face_recognition** | 56626 | The world's simplest facial recognition api for Python and the command line | [link](https://github.com/ageitgey/face_recognition) |
| 66 | **faceswap** | 56162 | Deepfakes Software For All | [link](https://github.com/deepfakes/faceswap) |
| 67 | **AI-For-Beginners** | 53188 | 12 Weeks, 24 Lessons, AI for All! | [link](https://github.com/microsoft/AI-For-Beginners) |
| 68 | **100-Days-Of-ML-Code** | 51584 | 100 Days of ML Coding | [link](https://github.com/Avik-Jain/100-Days-Of-ML-Code) |
| 69 | **awesome-claude-code** | 51250 | A hand-picked collection of the finest of resources for the most awesome of agents, Claude Code, the undisputed champion | [link](https://github.com/hesreallyhim/awesome-claude-code) |
| 70 | **cherry-studio** | 49122 | AI productivity studio with smart chat, autonomous agents, and 300+ assistants. Unified access to frontier LLMs | [link](https://github.com/CherryHQ/cherry-studio) |
| 71 | **julia** | 48946 | The Julia Programming Language | [link](https://github.com/JuliaLang/julia) |
| 72 | **Made-With-ML** | 48920 | Learn how to develop, deploy and iterate on production-grade ML applications. | [link](https://github.com/GokuMohandas/Made-With-ML) |
| 73 | **qlib** | 46801 | Qlib is an AI-oriented Quant investment platform that aims to use AI tech to empower Quant Research, from exploring idea | [link](https://github.com/microsoft/qlib) |
| 74 | **nanobot** | 46381 | Ultra-lightweight, open-source, self-hosted personal AI agent framework in Python with WebUI, tools, memory, MCP, multi- | [link](https://github.com/HKUDS/nanobot) |
| 75 | **airflow** | 46301 | Apache Airflow - A platform to programmatically author, schedule, and monitor workflows | [link](https://github.com/apache/airflow) |
| 76 | **streamlit** | 45409 | Streamlit — A faster way to build and share data apps. | [link](https://github.com/streamlit/streamlit) |
| 77 | **ai-engineering-from-scratch** | 44861 | Learn it. Build it. Ship it for others. | [link](https://github.com/rohitg00/ai-engineering-from-scratch) |
| 78 | **new-api** | 43782 | A unified AI model hub for aggregation & distribution. It supports cross-converting various LLMs into OpenAI-compatible, | [link](https://github.com/QuantumNous/new-api) |
| 79 | **TensorFlow-Examples** | 43738 | TensorFlow Tutorial and Examples for Beginners (support TF v1 & v2) | [link](https://github.com/aymericdamien/TensorFlow-Examples) |
| 80 | **gpt-researcher** | 28718 | An autonomous agent that conducts deep research on any data using any LLM providers | [link](https://github.com/assafelovic/gpt-researcher) |
| 81 | **Vibe-Trading** | 28532 | "Vibe-Trading: Your Personal Trading Agent" | [link](https://github.com/HKUDS/Vibe-Trading) |
| 82 | **DeepSeek-Reasonix** | 28006 | DeepSeek-native AI coding agent for your terminal. Engineered around prefix-cache stability — leave it running. | [link](https://github.com/esengine/DeepSeek-Reasonix) |
| 83 | **ai-agent-book** | 26116 | 《深入理解 AI Agent：设计原理与工程实践》（李博杰 著）开源主仓库：全书正文、编译版 PDF 与按章配套代码 | [link](https://github.com/bojieli/ai-agent-book) |
| 84 | **MaxKB** | 22310 | 🔥 MaxKB is an open-source platform for building enterprise-grade agents.  强大易用的开源企业级智能体平台。 | [link](https://github.com/1Panel-dev/MaxKB) |
| 85 | **oh-my-pi** | 20573 | ⌥  AI Coding agent for the terminal — hash-anchored edits, optimized tool harness, LSP, Python, browser, subagents, and | [link](https://github.com/can1357/oh-my-pi) |
| 86 | **FunASR** | 19546 | Open-source speech recognition toolkit for training, inference, streaming ASR, VAD, punctuation, speaker diarization pip | [link](https://github.com/modelscope/FunASR) |
| 87 | **browser-harness** | 16336 | Browser Harness / Self-healing harness that enables LLMs to complete any task. | [link](https://github.com/browser-use/browser-harness) |
| 88 | **ai-berkshire** | 14700 | AI 时代的伯克希尔：基于 Claude Code / Codex 的价值投资研究框架。巴菲特·芒格·段永平·李录四大师方法论 + 多Agent并行研究。/ AI-era Berkshire: a value investing resea | [link](https://github.com/xbtlin/ai-berkshire) |
| 89 | **Auto-claude-code-research-in-sleep** | 14006 | ARIS ⚔️ (Auto-Research-In-Sleep) — Lightweight Markdown-only skills for autonomous ML research: cross-model review loops | [link](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) |
| 90 | **cc-haha** | 13742 | Local-first cross-platform desktop workspace for Claude Code / agents: multi-agent, Git worktrees, code diffs, skill mar | [link](https://github.com/NanmiCoder/cc-haha) |
| 91 | **fastapi_mcp** | 11966 | Expose your FastAPI endpoints as Model Context Protocol (MCP) tools, with Auth! | [link](https://github.com/tadata-org/fastapi_mcp) |
| 92 | **Kimi-K3** | 7486 | Moonshot AI'nin yeni nesil frontier modeli Kimi-K3 — çok modlu, uzun bağlam destekli güçlü LLM | [link](https://github.com/MoonshotAI/Kimi-K3) |
| 93 | **airllm** | 26663 | 4GB GPU ile 70B LLM inference — extreme bellek sıkıştırma, tamamen lokal | [link](https://github.com/lyogavin/airllm) |
| 94 | **pocketbase** | ? | Tek dosyali açik kaynak backend — gerçek zamanli veritabani, auth, dosya depolama ve REST/JS SDK | [link](https://github.com/pocketbase/pocketbase) |
| 95 | **Infisical** | ? | Açik kaynak secret yönetim platformu — .env, API key, sertifika ve yapilari merkezi olarak yönet | [link](https://github.com/Infisical/infisical) |
| 96 | **kimi-cli** | 11188 | Kimi Code CLI — yeni nesil ajan tabanlı kodlama ve görev yürütme aracı | [link](https://github.com/MoonshotAI/kimi-cli) |
| 97 | **omlx** | 19,328 | Apple Silicon MLX tabanlı LLM inference server. Continuous batching + SSD cache + macOS menu bar yönetim. OpenAI API uyumlu. | [link](https://github.com/jundot/omlx) |

## run-llama/llama_index ⭐51,745
**URL:** https://github.com/run-llama/llama_index
**Tags:** agents, data, framework, rag, fine-tuning
Dokuman agent + RAG framework. OCR + indexleme platformu.
**Portföy:** B2BLife şirket intelligence için belge indexleme, TSA StrategyLab için RAG
| 27 | **qdrant** | 34,063 | Yüksek performanslı vektör veritabanı — RAG, embedding arama, semantik benzerlik. B2BLife/TechSyncAnalytica için şirket bilgi tabanı ve döküman arama altyapısı. Yerel çalışır, REST+gRPC API | [link](https://github.com/qdrant/qdrant) |

- [salesforce/OmniXAI](https://github.com/salesforce/OmniXAI) ⭐970 — Açıklanabilir AI (XAI) kütüphanesi — model yorumlama ve şeffaflık
- [Tencent/TencentPretrain](https://github.com/Tencent/TencentPretrain) ⭐1091 — PyTorch tabanlı LLM ön eğitim çerçevesi ve model zoo
- [Tencent/tencent-ml-images](https://github.com/Tencent/tencent-ml-images) ⭐3063 — Büyük çok etiketli görsel veritabanı ve ResNet-101 modeli
- [bojieli/ai-agent-book](https://github.com/bojieli/ai-agent-book) ⭐40672 — AI Agent tasarım ilkeleri ve mühendislik pratiği kitabı (açık kaynak)

## shiyu-coder/Kronos ⭐37,729
**Lang:** Python | Finansal piyasalar için temel dil modeli.
Fiyat, hacim ve volatilite verilerini doğal dil olarak modelleyen transformer mimarisi.
**Repo:** https://github.com/shiyu-coder/Kronos
**Not:** StockPulse için finansal zaman serisi tahmin referansı

## FlashML-org/FreeToken
Ücretsiz LLM token/erişim yönetimi — açık kaynak token optimizasyon aracı.
- **Stars:** 2,483 | **Language:** Python
- **GitHub:** https://github.com/FlashML-org/FreeToken
- **Kullanım:** Groq/Ollama token verimliliği, Synapse embedding maliyet azaltma

## microsoft/kernel-memory
Microsoft LLM bellek çözümü — RAG, semantic search, indeksleme, kullanıcı/takım/uygulama hafızası.
- **Stars:** 2,233 | **Language:** C#
- **Tags:** rag, llm, memory, semantic-search, indexing
- **GitHub:** https://github.com/microsoft/kernel-memory
- **Kullanım:** Synapse Knowledge Layer için alternatif RAG mimarisi referansı

## JustVugg/colibri
Saf C ile MoE modellerini disk'ten expert streaming ile çalıştır. Sıfır bağımlılık, minimal kaynak.
- **Stars:** 25,890 | **Language:** C
- **GitHub:** https://github.com/JustVugg/colibri
- **Kullanım:** Synaptiq Studio offline/yerel model desteği için ultra-hafif inference

## zilliztech/deep-searcher
Open Source Deep Research — özel veriler üzerinde arama ve akıl yürütme. Agentic RAG mimarisi, Milvus/Zilliz vektör DB entegrasyonu. Claude, DeepSeek, Grok, Qwen3, Llama4 desteği. Pipedream/Perplexity alternatifi.
- **Stars:** 8,168 | **Language:** Python
- **Tags:** agentic-rag, deep-research, vector-database, milvus, reasoning-models
- **GitHub:** https://github.com/zilliztech/deep-searcher
- **Kullanım:** Synaptiq Synapse brain için deep research referansı — private data üzerinde RAG + reasoning

## ombharatiya/ai-system-design-guide
Üretim ortamı AI sistemleri ve değerlendirmeleri oluşturan mühendisler için kapsamlı AI sistem tasarım rehberi. RAG, agentic workflow, evals, interview soruları. Claude, Gemini, DeepSeek, Grok desteği.
- **Stars:** 2,857 | **Language:** Markdown
- **Tags:** ai, system-design-interview, rag, evals, agentic-ai, llm, machine-learning
- **GitHub:** https://github.com/ombharatiya/ai-system-design-guide
- **Kullanım:** YouTube 'AI ile SaaS Kurma' serisi için içerik kaynağı; TSA agent mimarisi tasarım referansı

### microduck_rl
- **Repo:** https://github.com/pollen-robotics/microduck_rl
- **Stars:** ?
- **Açıklama:** Reinforcement Learning for robotics — robotik sistemlerde pekiştirmeli öğrenme uygulaması. Sim-to-real transfer.

### minimind (jingyaogong)
- **Repo:** https://github.com/jingyaogong/minimind
- **Stars:** 56,020
- **Açıklama:** Sıfırdan 64M parametreli LLM eğitimi — sadece 2 saatte küçük dil modeli oluşturma. LLM mimarisi anlama ve eğitim amaçlı referans proje.

### DeepTutor (HKUDS)
- **Repo:** https://github.com/HKUDS/DeepTutor
- **Stars:** 38,432
- **Açıklama:** Araştırma tabanlı kişiselleştirilmiş AI öğretmen — derin öğrenme asistanı, etkileşimli ders modu. Synaptiq'in Fabric agent sistemi ile entegre edilebilir veri eğitimi modülü için ilham kaynağı.

### system-design-101 (ByteByteGoHq)
- **Repo:** https://github.com/ByteByteGoHq/system-design-101
- **Stars:** 87,973
- **Açıklama:** Görseller ve rehberlerle sistem tasarımı — 87K yıldız, API, veritabanı, cache, CDN, mesajlaşma sistemleri anlatılıyor. YouTube teknik eğitim serisi + TSA içerik üretimi için temel referans.
