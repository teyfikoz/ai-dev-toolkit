# PraisonAI Integration Guide

## Installation

```bash
pip install praisonaiagents   # lightweight
pip install praisonai         # full framework with UI
```

## Core Concepts

| Concept | Description |
|---------|-------------|
| `Agent` | Autonomous worker with a role, goal, and backstory |
| `Task` | What an agent does — has description + expected_output |
| `Tools` | What agents can use: web search, file I/O, code execution, DB |
| `Memory` | `short_term` (session), `long_term` (RAG), `entity` (knowledge graph) |
| `Process` | `sequential` → one after another; `hierarchical` → manager delegates |

## Minimal Example

```python
from praisonaiagents import Agent, Task, PraisonAIAgents

analyst = Agent(
    role="Market Analyst",
    goal="Research competitor pricing",
    backstory="Expert in B2B market analysis",
    tools=["web_search"]
)

writer = Agent(
    role="Report Writer",
    goal="Produce executive summary",
    memory=True  # persists between tasks
)

pipeline = PraisonAIAgents(
    agents=[analyst, writer],
    tasks=[
        Task(description="Research top 5 competitors for {product}", agent=analyst,
             expected_output="Pricing table with features"),
        Task(description="Write executive summary of findings",       agent=writer,
             expected_output="500-word summary with recommendations"),
    ],
    process="sequential"
)

result = pipeline.start(inputs={"product": "B2B inventory software"})
print(result)
```

## Tools Reference

```python
# Built-in tools
tools = [
    "web_search",        # DuckDuckGo / Google
    "web_scrape",        # Fetch and parse URLs
    "file_read",         # Read local files
    "file_write",        # Write files
    "code_interpreter",  # Execute Python
    "sql_query",         # Query databases
    "wikipedia",         # Wikipedia API
]

# Custom tool
from praisonaiagents import tool

@tool
def get_stock_price(symbol: str) -> dict:
    """Get current stock price for a symbol."""
    # ... your implementation
    return {"symbol": symbol, "price": 150.0}

agent = Agent(role="...", tools=[get_stock_price])
```

## Memory Configuration

```python
from praisonaiagents import Agent
from praisonaiagents.memory import Memory

# Short-term: lives for the session
agent = Agent(role="...", memory=True)

# Long-term: persists to disk (RAG)
agent = Agent(
    role="...",
    memory=Memory(
        provider="rag",
        config={"path": "./agent_memory.db"}
    )
)

# Entity memory: knowledge graph
agent = Agent(
    role="...",
    memory=Memory(provider="entity")
)
```

## Integrations

### Slack
```python
from praisonaiagents.integrations import SlackIntegration

slack = SlackIntegration(token="xoxb-your-token", channel="#ai-reports")
pipeline = PraisonAIAgents(agents=[...], tasks=[...], callback=slack.send)
```

### Discord
```python
from praisonaiagents.integrations import DiscordIntegration
discord = DiscordIntegration(webhook_url="https://discord.com/api/webhooks/...")
```

## Visual Workflow UI

```bash
praisonai --ui
# → http://localhost:8080
# Drag-and-drop workflow builder
# Connect agents visually
# Export as Python code
```

## Real Project Patterns

### B2BLife Intelligence Pipeline

```python
from praisonaiagents import Agent, Task, PraisonAIAgents

scraper = Agent(
    role="Web Intelligence Analyst",
    goal="Find company websites and analyse web presence",
    tools=["web_search", "web_scrape"]
)

gap_analyst = Agent(
    role="Website Gap Analyst",
    goal="Identify what's missing from each company's web presence",
    backstory="Expert in digital marketing and web conversion"
)

report_writer = Agent(
    role="Sales Report Writer",
    goal="Create actionable outreach reports",
    memory=True
)

pipeline = PraisonAIAgents(
    agents=[scraper, gap_analyst, report_writer],
    tasks=[
        Task(description="Search for {company_name} website and extract content",
             agent=scraper),
        Task(description="Identify missing pages, SEO issues, conversion gaps",
             agent=gap_analyst),
        Task(description="Write 1-page outreach report with specific recommendations",
             agent=report_writer, expected_output="PDF-ready report"),
    ]
)
```

### RoboCheckIn Incident Analysis

```python
incident_analyst = Agent(
    role="Incident Analyst",
    goal="Analyse monitoring incidents and provide actionable summaries",
    backstory="SRE with 10 years of incident response experience",
    llm="meta-llama/Llama-3.1-8B-Instruct",  # via HuggingFace router
    self_reflection=True  # validates own output
)

task = Task(
    description="""
    Incident data: {incident_json}

    Provide:
    1. Root cause (one sentence)
    2. Business impact (severity + affected users)
    3. Immediate mitigation steps (ordered list)
    4. Prevention recommendations
    """,
    agent=incident_analyst,
    expected_output="Structured incident report"
)
```

## Migration from CrewAI

```python
# CrewAI (before)
from crewai import Agent, Task, Crew

agent = Agent(role="Analyst", goal="...", backstory="...")
task = Task(description="...", agent=agent)
crew = Crew(agents=[agent], tasks=[task])
result = crew.kickoff()

# PraisonAI (after) — almost identical
from praisonaiagents import Agent, Task, PraisonAIAgents

agent = Agent(role="Analyst", goal="...", backstory="...")
task = Task(description="...", agent=agent)
pipeline = PraisonAIAgents(agents=[agent], tasks=[task])
result = pipeline.start()
```

## Performance Tips

```python
# Async for parallel execution
import asyncio

async def run_pipeline():
    pipeline = PraisonAIAgents(
        agents=[...], tasks=[...],
        process="hierarchical",  # manager agent coordinates
        async_execution=True
    )
    return await pipeline.astart()

asyncio.run(run_pipeline())
```
