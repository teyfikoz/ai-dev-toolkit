# Skills & Tools for Insight Agent and GlobalKariyerim

## Insight Agent

Insight Agent is a USB-based local AI research and intelligence tool.
The skills ecosystem dramatically extends what it can do.

### Recommended Skills Stack

**1. academic-research-skills (Imbad0202)**
```
Primary use: Research pipeline automation
- Feed URLs/PDFs → structured insight extraction
- Citation tracking across sources
- Blog/report draft generation from research
```

**2. agency-agents roles:**
- `Market Research Analyst` — structured competitive research
- `Financial Analyst` — financial data interpretation
- `Data Scientist` — statistical analysis framing
- `Investigative Journalist` — OSINT-style investigation

**3. PraisonAI multi-agent pipeline:**
```python
from praisonaiagents import Agent, Task, PraisonAIAgents

collector = Agent(
    role="Intelligence Collector",
    goal="Gather data from multiple sources on {topic}",
    tools=["web_search", "web_scrape", "wikipedia"],
    backstory="Expert OSINT analyst"
)

analyser = Agent(
    role="Pattern Analyst",
    goal="Find patterns and anomalies in collected data",
    memory=True  # retains context across research sessions
)

reporter = Agent(
    role="Intelligence Report Writer",
    goal="Produce structured intelligence brief",
    backstory="Former intelligence analyst, now consultant"
)

pipeline = PraisonAIAgents(
    agents=[collector, analyser, reporter],
    tasks=[
        Task(description="Collect all available data on {topic} from web, news, and Wikipedia",
             agent=collector),
        Task(description="Identify key patterns, trends, and anomalies",
             agent=analyser),
        Task(description="Write executive intelligence brief with confidence levels",
             agent=reporter,
             expected_output="Structured brief: Summary | Key Findings | Risk Factors | Recommendations"),
    ]
)
```

**4. Shadowbroker (geospatial layer)**
```python
# Enrich research with geospatial data
# - Where are subjects/companies located?
# - GPS jamming zones affecting logistics
# - Real-time satellite passes over regions of interest
```

**5. agentmemory (persistent research)**
```python
from praisonaiagents.memory import Memory

# Insight Agent remembers previous research sessions
agent = Agent(
    role="Research Analyst",
    memory=Memory(provider="rag", config={"path": "./insight_memory.db"})
)
# Follow-up questions remember prior context automatically
```

### New Features to Add to Insight Agent

| Feature | Tool | Implementation |
|---------|------|----------------|
| Multi-source aggregation | PraisonAI | 3-agent pipeline (collect → analyse → report) |
| Persistent memory | agentmemory | SQLite-backed RAG across USB sessions |
| Geospatial enrichment | Shadowbroker | API bridge to local Shadowbroker instance |
| Web scraping | Firecrawl CLI | `firecrawl scrape {url}` → Markdown → agent context |
| Expert analysis roles | agency-agents | Drop-in role prompts per research domain |
| Visual report | react-bits | Animated insight cards in web dashboard |

### Zero-Cost Inference for Insight Agent

```python
# Use FreeLLMAPI for non-critical analysis (free tier)
# Use local Ollama for sensitive/offline research
# Use Claude only for final report synthesis

from praisonaiagents import Agent

# Tiered LLM routing
research_agent = Agent(role="...", llm="auto")  # FreeLLMAPI routes to best free model
synthesis_agent = Agent(role="...", llm="claude-3-5-sonnet-20241022")  # only for final output
```

---

## GlobalKariyerim

GlobalKariyerim is a local career + visa assistant (FastAPI + Next.js + SQLite, Ollama-based).

### Current Stack
- Ollama local models: qwen2.5, deepseek-r1:8b, mistral, llama3.2
- JobSpy: LinkedIn + Indeed + Glassdoor scraping
- Consulting module: sessions → invoice → report.md

### Recommended Skills Stack

**1. agency-agents roles:**
- `HR Business Partner` — career strategy, CV optimisation
- `Legal Counsel` — visa/work permit advice framing
- `Career Coach` — personalised job search strategy
- `Financial Analyst` — salary negotiation, offer comparison
- `Cultural Advisor` (custom) — country-specific work culture

**2. academic-research-skills:**
```
- Research country-specific visa requirements
- Track immigration policy changes (RSS → agent)
- Generate structured country comparison reports
```

**3. PraisonAI pipeline for GlobalKariyerim:**

```python
# Job Application Package Generator
cv_analyst = Agent(
    role="CV Specialist",
    goal="Analyse CV and identify gaps for target role",
    backstory="Senior HR consultant with 15 years experience"
)

cover_letter_writer = Agent(
    role="Cover Letter Writer",
    goal="Write compelling, personalised cover letters",
    llm="qwen2.5"  # local Ollama model
)

visa_researcher = Agent(
    role="Immigration Researcher",
    goal="Find visa/work permit requirements for {country}",
    tools=["web_search"]
)

pipeline = PraisonAIAgents(
    agents=[cv_analyst, cover_letter_writer, visa_researcher],
    tasks=[
        Task(description="Analyse CV for {job_title} position at {company}",
             agent=cv_analyst),
        Task(description="Write tailored cover letter addressing identified gaps",
             agent=cover_letter_writer),
        Task(description="Research {work_visa_type} requirements for {country}",
             agent=visa_researcher),
    ]
)
```

**4. JobSpy + PraisonAI sponsor job finder:**
```python
sponsor_finder = Agent(
    role="Sponsor Job Researcher",
    goal="Find companies that sponsor work visas in {country}",
    tools=["web_search", "web_scrape"]
)

# Enrich JobSpy results with sponsorship likelihood scoring
```

### New Features for GlobalKariyerim

| Feature | Tool | Benefit |
|---------|------|---------|
| Multi-agent CV pipeline | PraisonAI | Better CV analysis + targeted cover letters |
| Sponsor probability scoring | agency-agents + web_search | Filter jobs by visa sponsor likelihood |
| Country research report | academic-research-skills | Automated immigration research |
| Salary comparison | agency-agents Financial Analyst | Offer evaluation, negotiation prep |
| Consulting session memory | agentmemory | Advisor remembers all previous sessions |
| Automated follow-up reminders | PraisonAI scheduled task | Application tracking + status nudges |

### Consulting Module Enhancement

```python
# consulting.py — enhanced with PraisonAI
consulting_pipeline = PraisonAIAgents(
    agents=[
        Agent(role="Career Strategist", goal="Build personalised career roadmap"),
        Agent(role="Immigration Specialist", goal="Map visa pathways to career goals"),
        Agent(role="Action Planner", goal="Create 30/60/90 day action plan"),
    ],
    tasks=[...],
    process="sequential"
)

# Output: structured Markdown report → auto-invoice → email delivery
# ₺1500/session → monthly potential: 10 sessions = ₺15,000
```

### Revenue Enhancement via Skills

1. **"AI Advisory Package"** — 5 expert agents (CV, legal, market research, salary, culture) → ₺2500/package
2. **Country Intelligence Report** — automated research via academic-research-skills → ₺500/report (sell as PDF)
3. **Sponsor Company Database** — PraisonAI scraper + sponsor scoring → monthly subscription ₺199/month
