# Claude Code Agent Teams — Complete Setup Guide

Run Backend + Frontend + Testing + Review agents simultaneously. One feature, 4 agents, 2 hours instead of a full day.

---

## The 3 Levels

Before building a team, understand what's available:

| Level | Name | How It Works | Best For |
|-------|------|-------------|----------|
| 1 | Subagents | Run inside your current session, report back | Repeatable tasks: review, test, docs |
| 2 | Agent View | Full-screen dashboard, sessions survive terminal close | 3-10 independent tasks |
| 3 | Agent Teams | Lead agent coordinates teammates, shared task list | Multi-file features with dependencies |

Most people never get past Level 1. This guide goes to Level 3.

---

## Step 1 — Enable Agent Teams

```bash
# Add to ~/.zshrc (Mac) or ~/.bashrc (Linux)
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
export CLAUDE_CODE_SUBAGENT_MODEL="claude-sonnet-4-5-20250929"
export CLAUDE_CODE_DEFAULT_EFFORT=high
export CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1
```

`CLAUDE_CODE_SUBAGENT_MODEL` routes teammates to Sonnet automatically — 1/5 the cost of Opus for focused execution tasks. The lead agent runs on whatever model you're using.

---

## Step 2 — Write a Team Prompt

The key difference from regular prompting: describe the full project and let the lead agent decompose it.

```
I need to build a user authentication system.

Spawn separate agents to handle:
1. Backend: Create Express.js routes for login, signup, and token refresh
2. Frontend: Build React login and signup forms with validation
3. Testing: Write integration tests for all auth endpoints
4. Review: Review all code produced by the other agents for security issues

Each agent works in its own context window.
Flag dependencies before starting dependent tasks.
Coordinate through the shared task list.
```

The lead agent breaks this down, assigns roles, and spawns teammates. Each teammate works independently with clean, focused context.

---

## Step 3 — Manage with Agent View

Once the team is running, switch to the dashboard:

```bash
claude agents
```

```
┌─────────────────────────────────────────────┐
│ Agent View                                  │
├──────────┬──────────┬───────────┬───────────┤
│ Backend  │ Frontend │ Testing   │ Review    │
│ ██████░░ │ ████░░░░ │ ░░░░░░░░░ │ waiting   │
│ 72%      │ 48%      │ queued    │ for deps  │
└──────────┴──────────┴───────────┴───────────┘
```

From here:
- **Dispatch** new tasks to the team
- **Peek** at any agent's progress without interrupting
- **Attach** to an agent when it needs input
- Close your laptop — sessions survive terminal closure

---

## Step 4 — Decision Framework

Not every task needs a team. Wrong orchestration wastes tokens.

| Situation | Use |
|-----------|-----|
| Single file fix | Regular Claude Code session |
| 3+ independent tasks, no dependencies | Agent View — dispatch all, check results |
| Repeatable workflow (review/test/docs) | Subagents with consistent prompts |
| Multi-file feature with dependencies | Agent Teams |
| Overnight backlog drain | Headless mode + `--max-budget-usd` cap |

---

## Step 5 — Guardrails

Multiple parallel agents = multiple things can go wrong simultaneously. Lock it down in `~/.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Glob",
      "Grep",
      "Edit",
      "Write(src/**)",
      "Write(tests/**)",
      "Bash(npm test *)",
      "Bash(npx tsc *)",
      "Bash(git add *)",
      "Bash(git commit *)"
    ],
    "deny": [
      "Read(**/.env*)",
      "Read(**/.ssh/**)",
      "Bash(rm -rf *)",
      "Bash(sudo *)",
      "Bash(git push *)",
      "Bash(npm publish *)"
    ],
    "defaultMode": "acceptEdits"
  }
}
```

Always set a budget cap for team sessions:

```bash
# 5 agents at $3 each = $15 cap for the entire team
claude -p "build the auth system" --max-budget-usd 15.00
```

---

## Copy-Paste Ready Setup

```bash
# 1. Add to ~/.zshrc
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
export CLAUDE_CODE_SUBAGENT_MODEL="claude-sonnet-4-5-20250929"
export CLAUDE_CODE_DEFAULT_EFFORT=high
export CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1

# 2. Reload
source ~/.zshrc

# 3. Start a team session with budget cap
claude -p "$(cat team-prompt.txt)" --max-budget-usd 15.00

# 4. Monitor
claude agents
```

**Team prompt template (`team-prompt.txt`):**

```
I need to [describe the full feature].

Spawn separate agents:
1. [Role 1]: [specific task with files/modules]
2. [Role 2]: [specific task with files/modules]
3. [Role 3]: [specific task with files/modules]
4. Review: Review all code for [bugs/security/style]

Each agent works in its own context.
Coordinate through the shared task list.
Flag dependencies before starting dependent tasks.
```

---

## Before & After

**Before (solo sequential):**
- Write → review → test → commit → docs
- One task at a time
- Context bloats as you switch between tasks
- A 4-part feature takes a full day

**After (agent team):**
- Backend + frontend + tests + review running simultaneously
- Each agent has clean, focused context
- Same feature done in ~2 hours
- You review and merge the results

Same Claude Code subscription. Same tool. The difference is one environment variable and a team prompt.

---

## Related

- [guides/praisonai-integration-guide.md](praisonai-integration-guide.md) — external multi-agent framework
- [github.com/Stanshy/AgentHub](https://github.com/Stanshy/AgentHub) — alternative multi-agent runner
- [github.com/humanlayer/12-factor-agents](https://github.com/humanlayer/12-factor-agents) — architecture principles for production agents
