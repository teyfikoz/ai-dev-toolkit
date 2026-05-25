# Claude Code Skills — Complete Setup Guide

## What Are Skills?

Skills are reusable, shareable instructions that extend Claude Code's capabilities. Think of them as "roles" or "modes" you can activate per task.

## The "Find Skills" Trick

A Japanese developer discovered this workflow:

> Create one skill whose only job is to scan the Anthropic ecosystem and surface the best existing skill for whatever you're working on.

**How it works:**
1. You describe your task
2. The "find-skills" skill searches skills.sh + GitHub
3. Returns: "Use X skill for this" + install command

## Directory Structure

```
~/.claude/
├── skills/
│   ├── frontend-design/     ← anthropics/skills
│   ├── agency-agents/       ← 140+ expert roles
│   ├── pm-skills/           ← 106 skills, 15 professions
│   └── academic-research/   ← research pipeline
├── commands/                ← SuperClaude slash commands
├── agents/                  ← SuperClaude agent personas
└── MEMORY.md                ← persistent context
```

## Installation Script

```bash
#!/bin/bash
# install-claude-skills.sh — run once to set up everything

mkdir -p ~/.claude/skills ~/.claude/commands ~/.claude/agents

# 1. anthropics/skills (frontend-design)
npx skills add anthropics/skills 2>/dev/null || \
  git clone https://github.com/anthropics/skills /tmp/anthropics-skills && \
  cp -r /tmp/anthropics-skills/skills/* ~/.claude/skills/

# 2. agency-agents (140+ roles)
git clone --depth=1 https://github.com/msitarzewski/agency-agents \
  ~/.claude/skills/agency-agents

# 3. PM skills (106 skills)
git clone --depth=1 https://github.com/mohitagw15856/pm-claude-skills \
  ~/.claude/skills/pm-skills

# 4. SuperClaude Framework
git clone --depth=1 https://github.com/SuperClaude-Org/SuperClaude_Framework \
  /tmp/sc && cp -r /tmp/sc/.claude/* ~/.claude/

# 5. Real engineer skills
npx skills add mattpocock/skills 2>/dev/null || true

echo "Done. Restart Claude Code to pick up new skills."
```

## Using Skills

### In Claude Code
```
/skill frontend-design
→ Claude now generates production-quality UI instead of generic layouts

/skill ceo
→ Claude adopts CEO strategic thinking role

/skill financial-analyst
→ Quantitative finance analysis mode

/skill security-auditor
→ Code security review mode (from SuperClaude)
```

### Creating a Custom Skill

```bash
mkdir -p ~/.claude/skills/my-skill
cat > ~/.claude/skills/my-skill/prompt.md << 'EOF'
# My Custom Skill

When activated, you are a [ROLE].

Your approach:
1. [Step 1]
2. [Step 2]

Always:
- [Constraint 1]
- [Constraint 2]

Output format: [Format]
EOF
```

## SuperClaude Commands Reference

After installing SuperClaude_Framework:

```
/sc:architect   → System design and architecture decisions
/sc:security    → Security audit and vulnerability scan
/sc:test        → Generate comprehensive test suite
/sc:refactor    → Code quality and refactoring
/sc:api         → API design and OpenAPI spec
/sc:deploy      → Deployment strategy and CI/CD
/sc:perf        → Performance profiling and optimization
/sc:docs        → Documentation generation
```

## Agency-Agents Role Reference

Full list: `~/.claude/skills/agency-agents/roles/`

**Business:**
- CEO, CFO, CMO, CTO, COO
- M&A Analyst, Financial Analyst, Portfolio Manager
- Business Developer, Trust & Risk Assessor

**Technical:**
- Senior Developer, DevOps Engineer, Security Auditor
- Data Scientist, ML Engineer, Solution Architect

**Creative/Marketing:**
- Brand Strategist, Content Director, UX Designer
- Customer Insights Analyst, Growth Hacker

**Specialist:**
- Legal Counsel, Compliance Officer
- Aviation Consultant, Revenue Manager
- Macro Economist, Portfolio Manager

**Usage:**
```
Tell Claude: "You are an M&A Analyst from agency-agents..."
Then paste the full role prompt from ~/.claude/skills/agency-agents/roles/ma-analyst.md
```

## skills.sh Integration

Browse: https://www.skills.sh/

Monthly trending skills:
- `frontend-design` — 136K+ installs
- `agency-agents` — 810K+ installs
- `academic-research` — research pipeline
- `pm-skills` — product management suite

## Troubleshooting

**Skills not loading:**
```bash
# Check skills directory
ls ~/.claude/skills/

# Restart Claude Code
pkill -f "claude" && claude
```

**Conflict between skills:**
- Only activate one "role" skill at a time
- SuperClaude commands are always available regardless of active skill
