# AI Dev Toolkit — Curated GitHub Repos & Claude Code Skills

> **140+ hand-picked repositories and skills** for AI-powered software development.
> Organised, analysed, and battle-tested across real production projects.

[![Stars](https://img.shields.io/github/stars/teyfikoz/ai-dev-toolkit?style=flat-square)](https://github.com/teyfikoz/ai-dev-toolkit)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![Last Updated](https://img.shields.io/badge/updated-May%202026-blue?style=flat-square)]()

---

## Why This Repo?

There are thousands of AI tools on GitHub. This repo cuts through the noise:

- Every entry has been **actually used** (or tested) in a real project
- Each tool has a **practical use case** — not just "it exists"
- Organised into clear categories so you find what you need in seconds
- Includes **Claude Code skills** you can install and run today

---

## Quick Navigation

| Category | Count | What's Inside |
|----------|-------|---------------|
| [Claude Code Skills](#-claude-code-skills) | 12 | Ready-to-install skills for Claude Code |
| [Multi-Agent Frameworks](#-multi-agent-frameworks) | 8 | PraisonAI, CrewAI, AgentHub, Citadel... |
| [Browser & Web Automation](#-browser--web-automation) | 6 | Alumnium, Firecrawl, Playwright-based... |
| [LLM Infrastructure](#-llm-infrastructure) | 7 | Free LLM gateways, local models, routing |
| [Content & Media Generation](#-content--media-generation) | 9 | Voice, video, image, slides automation |
| [Data & Analytics](#-data--analytics) | 6 | Finance, trading indicators, geospatial |
| [Security & OSINT](#-security--osint) | 7 | OSINT frameworks, secret scanning, CTFs |
| [UI & Frontend Components](#-ui--frontend-components) | 5 | Animated React components, design systems |
| [Backend & Infrastructure](#-backend--infrastructure) | 10 | Kubernetes, monitoring, messaging |
| [Mobile Development](#-mobile-development) | 4 | Capacitor, NativeScript, store publishing |
| [Developer Productivity](#-developer-productivity) | 8 | Code graphs, context tools, scaffolding |
| [WhatsApp & Messaging](#-whatsapp--messaging) | 3 | Self-hosted WhatsApp API, n8n workflows |
| [AI Roles & Prompts](#-ai-roles--prompts) | 5 | 140+ expert agent roles, system prompts |

---

## Claude Code Skills

Install with: `npx skills add <owner/repo>` or copy to `~/.claude/skills/`

### Essential — Install These First

| Skill Repo | Stars | What It Does | Install |
|-----------|-------|-------------|---------|
| [anthropics/skills](https://github.com/anthropics/skills) | 136K+ | **Frontend Design** — stops Claude from generating generic AI layouts. Forces production-quality UI | `npx skills add anthropics/skills` |
| [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) | 810K+ | **140+ expert AI roles** — CEO, lawyer, financial analyst, M&A specialist, UX designer | Copy prompts to `.claude/skills/` |
| [SuperClaude-Org/SuperClaude_Framework](https://github.com/SuperClaude-Org/SuperClaude_Framework) | — | **30 slash commands + 20 agent personas** — `/sc:security`, `/sc:architect`, `/sc:test`, `/sc:refactor` | Clone to `.claude/` |
| [mohitagw15856/pm-claude-skills](https://github.com/mohitagw15856/pm-claude-skills) | — | **106 skills across 15 professions** — PM, Finance, Legal, Marketing, HR | Clone skills to `.claude/skills/` |
| [mattpocock/skills](https://github.com/mattpocock/skills) | — | **Real engineers' production skills** — TypeScript, React, testing patterns | `npx skills add mattpocock/skills` |
| [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) | — | **Research pipeline** — PDF analysis, blog drafting, citation tracking | Clone to `.claude/skills/` |
| [wesammustafa/Claude-Code-Everything-You-Need-to-Know](https://github.com/wesammustafa/Claude-Code-Everything-You-Need-to-Know) | — | **Complete Claude Code reference** — hooks, MCPs, agents, memory | Read as reference |

### Skills Installation

```bash
# Create skills directory
mkdir -p ~/.claude/skills

# Install anthropics frontend-design skill
npx skills add anthropics/skills

# Install agency-agents (140+ roles)
git clone https://github.com/msitarzewski/agency-agents ~/.claude/skills/agency-agents

# Install SuperClaude (30 commands + 20 agents)
git clone https://github.com/SuperClaude-Org/SuperClaude_Framework /tmp/sc
cp -r /tmp/sc/.claude/* ~/.claude/

# Install PM skills (106 across 15 professions)
git clone https://github.com/mohitagw15856/pm-claude-skills ~/.claude/skills/pm-skills
```

### skills.sh — The "Find Skills" Trick

A Japanese developer discovered this workflow that nobody was talking about:

```
# Instead of searching manually, create ONE skill that scans
# the Anthropic ecosystem and finds the optimal workflow for your task.
```

Browse all community skills at **[skills.sh](https://www.skills.sh/)** — updated monthly.

**Using skills in a session:**
```
/skill frontend-design    → production-quality UI generation
/skill m-and-a-analyst    → M&A analysis role (from agency-agents)
/skill research-pipeline  → academic research workflow
```

---

## Multi-Agent Frameworks

### PraisonAI ⭐ Recommended

**Repo:** [MervinPraison/PraisonAI](https://github.com/MervinPraison/PraisonAI)

The most complete multi-agent framework for production use. Supports 100+ LLMs, has drag-and-drop workflow UI, built-in memory, and self-reflection (agents evaluate their own output).

```bash
pip install praisonaiagents
praisonai --ui   # http://localhost:8080
```

```python
from praisonaiagents import Agent, Task, PraisonAIAgents

research = Agent(role="Research Analyst", goal="Gather market data", tools=["web_search"])
writer   = Agent(role="Report Writer",    goal="Synthesise findings", memory=True)

pipeline = PraisonAIAgents(
    agents=[research, writer],
    tasks=[Task(description="Research {topic}", agent=research),
           Task(description="Write report",     agent=writer)],
    process="sequential"  # or "hierarchical"
)
result = pipeline.start()
```

**Why PraisonAI over CrewAI:**

| Feature | CrewAI | PraisonAI |
|---------|--------|-----------|
| LLM support | 20+ | 100+ |
| Visual workflow UI | No | Yes |
| Self-reflection | Manual | Automatic |
| Slack/Discord/Telegram | No | Built-in |
| Long-term memory | Manual | Built-in |
| Async execution | Limited | Full |

---

### AgentHub

**Repo:** [Stanshy/AgentHub](https://github.com/Stanshy/AgentHub)

Run multiple Claude Code instances as a **virtual dev team**. Backend agent + Frontend agent + Test agent all working on the same project simultaneously.

```bash
git clone https://github.com/Stanshy/AgentHub
# Configure agents in agentHub.config.json
agenthub start --project ./myproject
```

---

### Citadel

**Repo:** [SethGammon/Citadel](https://github.com/SethGammon/Citadel)

**Persistent campaigns** that survive Claude Code session ends. Define a long goal ("deploy app, pass all tests, integrate Paddle") and Citadel keeps track across sessions.

---

### Other Agent Frameworks

| Repo | What It Does | Best For |
|------|-------------|----------|
| [humanlayer/12-factor-agents](https://github.com/humanlayer/12-factor-agents) | 12 production principles for agent architecture | Architecture reference |
| [rohitg00/agentmemory](https://github.com/rohitg00/agentmemory) | Persistent agent memory (short/long term + entity) | Stateful agents |
| [tinyhumansai/openhuman](https://github.com/tinyhumansai/openhuman) | Personal AI assistant with local LLMs | Ollama-based assistants |

---

## Browser & Web Automation

### Alumnium

**Repo:** [alumnium-hq/alumnium](https://github.com/alumnium-hq/alumnium)

AI-native browser automation — use natural language instead of CSS selectors.

```python
from alumnium import Agent
agent = Agent(driver)  # Selenium driver
agent.do("find all products with price under $50 and extract their SKUs")
results = agent.get("list all product names and prices as JSON")
```

---

### Firecrawl CLI

**Repo:** [firecrawl/cli](https://github.com/firecrawl/cli)

Converts any URL to clean Markdown — perfect for feeding web content to AI agents.

```bash
npx firecrawl scrape https://competitor.com --format markdown
npx firecrawl crawl https://docs.site.com --limit 50 --format markdown
```

---

### CloakBrowser

**Repo:** [CloakHQ/CloakBrowser](https://github.com/CloakHQ/CloakBrowser)

Scraping with bot-bypass. Gets through Cloudflare, reCAPTCHA, and other protections.

---

### Google Maps Scraper

**Repo:** [zohaibbashir/Google-Maps-Scrapper](https://github.com/zohaibbashir/Google-Maps-Scrapper)

Extract business listings, reviews, hours, and contact info from Google Maps.

```python
# Find businesses without websites → lead generation
from google_maps_scraper import scrape
leads = scrape("restaurant istanbul beyoglu", limit=200)
no_website = [b for b in leads if not b.get("website")]
```

---

## LLM Infrastructure

### FreeLLMAPI

**Repo:** [tashfeenahmed/freellmapi](https://github.com/tashfeenahmed/freellmapi)

Gateway that **aggregates dozens of free LLM tiers** into one API. Automatic routing, rate-limit management, and fallback when one provider hits limits. No card required.

```python
import openai
client = openai.OpenAI(base_url="https://freellmapi.com/v1", api_key="free")
response = client.chat.completions.create(
    model="auto",  # Routes to best available free model
    messages=[{"role": "user", "content": "Analyse this market report..."}]
)
```

---

### CodeGraph

**Repo:** [colbymchenry/codegraph](https://github.com/colbymchenry/codegraph)

Builds a semantic knowledge graph of your codebase. Claude Code queries the graph instead of scanning files — **92% fewer tool calls, 71% faster exploration**.

```bash
npm install -g codegraph
cd /your/project && codegraph init
# Claude Code now navigates via graph queries
```

---

### Other LLM Tools

| Repo | What It Does |
|------|-------------|
| [ollama/ollama](https://github.com/ollama/ollama) | Run LLMs locally (Llama3, Mistral, Qwen...) |
| [oven-sh/bun](https://github.com/oven-sh/bun) | 3x faster JS runtime — replace Node.js in new projects |

---

## Content & Media Generation

### OmniVoice Studio

**Repo:** [debpalash/OmniVoice-Studio](https://github.com/debpalash/OmniVoice-Studio)

**646 languages**, fully offline voice cloning and video dubbing. Replaces ElevenLabs at zero cost.

- 3-second voice clone
- YouTube URL → transcript → translate → dub → MP4 export
- Real-time speech-to-text
- Batch processing (50+ videos)

```bash
git clone https://github.com/debpalash/OmniVoice-Studio
cd OmniVoice-Studio && pip install -r requirements.txt
python app.py  # http://localhost:7860
```

---

### Higgsfield CLI

**Repo:** [higgsfield-ai/cli](https://github.com/higgsfield-ai/cli)

30+ AI image/video generation models from your terminal.

```bash
brew install higgsfield
higgsfield generate create flux --prompt "product photo, white background" --wait
higgsfield generate create wan --prompt "product demo video" --wait
```

---

### LongCat-Video

**Repo:** [meituan-longcat/LongCat-Video](https://github.com/meituan-longcat/LongCat-Video)

13.6B parameter model for **long-form video generation** (minutes, not seconds). Requires multi-GPU — runs on Hetzner CCX53+.

---

### YouTube Automation Agent

**Repo:** [darkzOGx/youtube-automation-agent](https://github.com/darkzOGx/youtube-automation-agent)

Full pipeline: script → voiceover → thumbnail → upload to YouTube.

---

### Supertonic (TTS)

**Repo:** [supertone-inc/supertonic](https://github.com/supertone-inc/supertonic)

High-quality offline text-to-speech. Best for YouTube narration without API costs.

---

### React Bits

**Repo:** [DavidHDev/react-bits](https://github.com/DavidHDev/react-bits)

**110+ production-ready animated React components**. Copy-paste into any project.

```bash
# Use with anthropics/skills frontend-design for production UI
npx @react-bits/cli add --all
```

---

## Data & Analytics

### Technical Analysis (Python)

**Repo:** [bukosabino/ta](https://github.com/bukosabino/ta)

130+ technical indicators for Python. Wraps Pandas.

```python
import ta
df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()
df['macd'] = ta.trend.MACD(df['close']).macd()
```

---

### Indicator (Go)

**Repo:** [cinar/indicator](https://github.com/cinar/indicator)

80+ indicators in Go — for high-performance backtesting.

---

### Shadowbroker

**Repo:** [BigBodyCobain/Shadowbroker](https://github.com/BigBodyCobain/Shadowbroker)

60+ public data sources in one geospatial intelligence panel. Private jets, military aircraft, ships, satellites, earthquakes, GPS jamming zones. Fully local.

---

## Security & OSINT

### Awesome Cyber Skills

**Repo:** [joe-shenouda/awesome-cyber-skills](https://github.com/joe-shenouda/awesome-cyber-skills)

Curated list of hands-on security practice platforms — CTFs, wargames, vulnerable VMs.

---

### System Prompts Collection

**Repo:** [asgeirtj/system_prompts_leaks](https://github.com/asgeirtj/system_prompts_leaks)

Collection of leaked/published system prompts from major AI products. Useful as benchmarks for your own agent prompts.

---

### RoboCheckIn Secret Scanner Patterns

> Built-in to RoboCheckIn v2.3 — 27 credential patterns (AWS keys, JWT secrets, Stripe keys, etc.)

```python
# 27 patterns for detecting accidentally committed secrets
PATTERNS = {
    "aws_access_key": r'AKIA[0-9A-Z]{16}',
    "stripe_secret":  r'sk_(live|test)_[0-9a-zA-Z]{24,}',
    "jwt_secret":     r'(?i)jwt[_-]?secret[_-]?[=:]\s*["\']?[a-zA-Z0-9+/]{32,}',
    # ... 24 more
}
```

---

## UI & Frontend Components

| Repo | Stars | What It Does |
|------|-------|-------------|
| [DavidHDev/react-bits](https://github.com/DavidHDev/react-bits) | — | 110+ animated React components |
| [anthropics/skills](https://github.com/anthropics/skills) | 136K+ | Frontend Design skill — production-quality UI |
| [shadcn/ui](https://github.com/shadcn-ui/ui) | 80K+ | Accessible component library (Radix + Tailwind) |
| [lucide-icons/lucide](https://github.com/lucide-icons/lucide) | 12K+ | 1400+ consistent icons |

---

## Backend & Infrastructure

| Repo | What It Does | When to Use |
|------|-------------|-------------|
| [cilium/cilium](https://github.com/cilium/cilium) | eBPF-based K8s networking & security | When moving to Kubernetes |
| [rmyndharis/OpenWA](https://github.com/rmyndharis/OpenWA) | Self-hosted WhatsApp API (multi-session, REST, n8n) | WhatsApp notifications/automation |
| [oven-sh/bun](https://github.com/oven-sh/bun) | Fast JS runtime | All new Node.js projects |

---

## Developer Productivity

| Repo | What It Does |
|------|-------------|
| [colbymchenry/codegraph](https://github.com/colbymchenry/codegraph) | Semantic code graph — 92% fewer Claude tool calls |
| [SuperClaude-Org/SuperClaude_Framework](https://github.com/SuperClaude-Org/SuperClaude_Framework) | 30 slash commands for Claude Code |
| [AgentHub (Stanshy)](https://github.com/Stanshy/AgentHub) | Multi-agent parallel dev team |
| [Citadel (SethGammon)](https://github.com/SethGammon/Citadel) | Persistent cross-session campaigns |
| [humanlayer/12-factor-agents](https://github.com/humanlayer/12-factor-agents) | 12 principles for production agents |

---

## WhatsApp & Messaging

### OpenWA

**Repo:** [rmyndharis/OpenWA](https://github.com/rmyndharis/OpenWA)

Self-hosted, multi-session WhatsApp gateway. REST API + Swagger + Docker.

```bash
docker compose up -d
# POST /api/sendText → send WhatsApp message
# GET  /api/sessions → manage multiple accounts
```

**Use cases:**
- Order/appointment notifications for SMBs
- Incident alerts from monitoring systems
- Report delivery to clients

**Revenue model:** Set up for local businesses → ₺500-1000/month/business

---

## AI Roles & Prompts

### Agency Agents (140+ Roles)

**Repo:** [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents)

The largest collection of expert AI agent roles. Drop any prompt into Claude Code as a system context:

```
# Available roles include:
CEO | CFO | CTO | CMO | Legal Counsel | M&A Analyst
Financial Analyst | Portfolio Manager | Macro Economist
Brand Strategist | Customer Insights Analyst | UX Designer
DevOps Engineer | Security Auditor | Data Scientist
Aviation Consultant | Revenue Manager | Trust & Risk Assessor
... and 120+ more
```

---

## Complete Repository Index

> Full analysis of all 140+ repositories with integration notes.

See [`categories/`](categories/) for detailed breakdowns:

- [`categories/claude-code-ecosystem.md`](categories/claude-code-ecosystem.md) — All Claude Code tools
- [`categories/multi-agent.md`](categories/multi-agent.md) — Agent frameworks compared
- [`categories/content-automation.md`](categories/content-automation.md) — Media generation pipeline
- [`categories/data-finance.md`](categories/data-finance.md) — Finance and trading tools
- [`categories/security.md`](categories/security.md) — Security and OSINT tools
- [`categories/saas-stack.md`](categories/saas-stack.md) — SaaS boilerplate and billing

---

## Usage Guide

### For Solo Developers / Indie Hackers

**Start here:**
1. Install `SuperClaude_Framework` → 30 instant commands
2. Install `frontend-design` skill → professional UI immediately
3. Set up `CodeGraph` on any large project → faster navigation
4. Bookmark `FreeLLMAPI` → prototype without API costs

### For SaaS Projects

**Recommended stack:**
```
PraisonAI          → Agent pipeline backbone
OpenWA             → WhatsApp notifications
FreeLLMAPI         → Development/testing LLM
OmniVoice Studio   → Voiceover/content
react-bits         → UI components
CodeGraph          → Dev efficiency
```

### For Content Creators

```
Higgsfield CLI     → AI images/videos in terminal
OmniVoice Studio   → Voice cloning + dubbing
LongCat-Video      → Long-form video (GPU server)
YouTube Automation → End-to-end video pipeline
Supertonic         → High-quality TTS
```

---

## Contributing

Found a tool that belongs here? Open a PR:
1. Add it to the appropriate `categories/*.md` file
2. Include: what it does, install command, one practical use case
3. Rate it: `HIGH` / `MEDIUM` / `LOW` usefulness

---

## License

MIT — use freely. Star if useful ⭐

---

*Maintained by [@teyfikoz](https://github.com/teyfikoz) | Last updated: May 2026*
