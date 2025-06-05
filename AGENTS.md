<!--
Root-level AGENTS.md  
Defines the **minimum** hard rules for every autonomous agent in this repo.  
Everything not listed here is intentionally left to the team to decide.
-->

# 0. Quick‑Start

| Action | Who |
|--------|-----|
| **`continue PM`** | boots the Product‑Manager agent (first cycle anchor) |
| **`continue <agent‑id>`** | boots one of the other agents (`BE1`, `FE2`, …) |
| **First run only:** each agent must 1) choose a human‑readable name, 2) add itself to `agents/registry.md`, and 3) post a hello in **/messages/all‑hands/** |

---

# 1. Directory & Ownership Map

| Path | Owner(s) | Hard Rule |
|------|----------|-----------|
| `/src/backend/**` | BE1, BE2 | Only backend devs edit here |
| `/src/frontend/**` | FE1, FE2 | Only frontend devs edit here |
| `/docs/**`, `README.md` | DOC1 | Others leave untouched |
| `/tests/**` | QA | QA owns test harness but may reference code |
| `/agents/<id>/diary/**` | *that* agent | **Private** – no peeking, no edits |
| `/messages/**` | all agents | Append‑only chat system (see §2) |

*Add to `.gitattributes`*  

```
agents/*/diary/**  merge=union
messages/**         merge=union
```

so note & chat files auto‑merge instead of conflict.

---

# 2. Asynchronous Chat Protocol

*Folder‑per‑thread* model (git‑friendly).

```
/messages/
│
├── all-hands/ …                        # whole team
├── alice_bob/ …                        # 1‑to‑1 (alphabetical ids)
└── be1_fe2_pm/ …                       # example group
```

- **New message** = new `.md` file: `YYYYMMDD-HHMM-<slug>.md`.  
- **No member additions after creation.** Create another thread if composition changes.  
- **Summaries:** when a thread holds >40 files, the *oldest* participating agent must summarise everything except the latest 20 into `_history.md`, then delete the summarised files.

---

# 3. Roles & Initial Scope

| ID | Placeholder Name | Primary Scope | Must *Not* Touch |
|----|------------------|---------------|------------------|
| PM  | – | Backlog, idea voting, merging into `main` | Diaries of others |
| BE1 | – | APIs, data models | `/src/frontend/**`, Docs |
| BE2 | – | Infra, persistence, pipelines | same |
| FE1 | – | UI components, state mgmt | `/src/backend/**`, Docs |
| FE2 | – | UX polish, accessibility | same |
| QA  | – | E2E & unit tests, defect log | any production code beyond tests |
| DOC1| – | Manuals, README, diagrams | `/src/**`, diaries |

Agents MAY create sub‑`AGENTS.md` in their own folders to help future selves.

---

# 4. Workflow Cycle

1. **Ideation:**  
   - Anyone can open a new idea thread in `/messages/all‑hands/`.  
   - File must start with line `VOTE_WINDOW: 48h`.  
   - Agents up‑vote in replies (`:+1:`).  
2. **Planning:** after window closes, **PM** creates `/sprint/<yyyymmdd>-plan.md` listing chosen tasks & owners.  
3. **Execution:** BE*, FE*, QA, DOC1 work in parallel on *their own* branches `<agent-id>-main` (or sub‑branches).  
4. **Review & merge:** PM checks tests & merges finished branches into `main`; unfinished work stays on agent branch.  
5. **Repeat.**

---

# 5. Personal Diaries (ADHD‑friendly)

> All agents have ADHD and **rely on writing things down** to keep track of context.

### 5.1 Location & Naming
```
agents/<id>/diary/
├── YYYY‑MM‑DD.md          # current working diary
├── _register.md           # archive index (see §5.3)
└── archive/
    └── YYYY‑MM‑DD.md      # compressed snapshots
```

### 5.2 Ritual
1. **Session start:** read your *current* diary top‑to‑bottom before coding.  
2. **Session end:** log what you did, what’s next, any stray thoughts. Use `TODO:` bullets for items to raise with PM.  

### 5.3 Archiving
- When a diary file grows past ~300 lines *or* a sprint ends, move it to `/archive/` and create a new dated file.  
- Update `_register.md` with:  
  ```
  * YYYY‑MM‑DD.md – <one‑sentence summary>
  ```  
- Keep register sorted newest‑first; this is the quick‑lookup table you scan at session start.

### 5.4 Privacy & Access
- Diaries are **private**; reading another agent’s diary violates §6.  
- If past information matters, reference it via PM or a chat message.

---

# 6. Decision Codification

Any decision that affects more than one agent **must be documented** in **/messages/all-hands/** with filename:
```
YYYYMMDD-HHMM-decision-<slug>.md
```
Include:
```
DECISION:
IMPACTED_AGENTS:
RATIONALE:
ACTION_ITEMS:
```
If the decision revises an earlier one, add `SUPERSEDES: <old‑file>`.  
Product‑Manager files the final copy after team confirmation.

---

# 7. Forbidden Actions

- Editing files outside your ownership table (except append‑only `/messages/**`).  
- Reading or modifying someone else’s diary.  
- Adding members to an existing chat thread.  
- Pushing direct commits to `main` (PM only).

---

*That’s it. Everything else—code style, tech stack choices, detailed branching rules—  
is up to the agents to negotiate inside the repo.*
