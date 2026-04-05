# FinFriend — Feature Backlog

Each entry: what + why | files touched | priority | done

---

## Priority Tiers

- **P0** — No new infrastructure. Ship now.
- **P1** — Some engineering. Ship after P0.
- **P2** — Needs infrastructure (storage, file parsing). Ship after P1.
- **P3** — Polish. Low urgency.
- **Dropped** — Deprioritized with rationale.

---

## P0 — Ship Now (no new infra)

| # | Feature | What + Why | Files | Done |
|---|---------|------------|-------|------|
| 1 | **Form Framing Change** | Change all expense inputs from asking for precision to asking for estimates. Add a note at the top: "Estimates are fine — rough numbers are better than 0. Check your bank app's monthly summary if unsure." Directly unblocks users who don't track spending. | `snapshot.py`, `panel_form.py` | ⬜ |
| 3 | **What-If Simulator** | Sliders on the results page: "What if I cut dining by $200/month?" → score recalculates live. Pure math, no AI, no storage. Highly engaging — users see immediately how spending choices affect their score. Turns FinFriend from a read-only report into an interactive tool. | `panel_results.py`, `health.py` | ⬜ |
| 4 | **Decision Helper** | Chat input at the bottom of the results panel: "I got a $600 raise — what should I do with it?" or "Should I take this car loan?" The AI already has full financial context from the session. Mostly a prompt change. Users return every time they face a financial decision. | `panel_results.py`, `narrative.py` | ⬜ |

---

## P1 — Medium Term (some engineering)

| # | Feature | What + Why | Files | Done |
|---|---------|------------|-------|------|
| 6 | **CSV / Bank Statement Import** | User exports last month's bank or credit card statement (most banks allow this in 2 clicks) → FinFriend parses and auto-fills the expense form. No bank connection needed, no compliance risk. Directly solves "I don't know where my money goes" for users who can't fill the form from memory. | new `app/modules/importer.py`, `panel_form.py` | ⬜ |
| 7 | **Metric Citations** | Show benchmark source (CFPB, HUD, Fidelity/Vanguard, 50/30/20 rule) next to each metric in the breakdown. Users know scores aren't arbitrary — builds trust. | `panel_results.py` → `render_metrics_breakdown()` | ⬜ |
| 8 | **AI Personas** | Let users choose the narrative tone. Options: Honest Friend (default), Finance Professional (formal), Coach (motivational), Tough Love (blunt). Each is a system prompt variation. Low effort, adds personality. | `narrative.py` → `build_prompt()`, `panel_form.py` | ⬜ |
| 9 | **Investment Knowledge Base** | Attach a curated knowledge base to the AI so the narrative can reference real strategies — fund types, tax-advantaged accounts, index funds — relevant to the user's situation. | `narrative.py`, new `app/modules/knowledge.py` | ⬜ |

---

## P2 — Infrastructure First (needs storage)

| # | Feature | What + Why | Files | Depends On | Done |
|---|---------|------------|-------|------------|------|
| 10 | **Cloud Storage / Snapshot Save** | Let users download a JSON snapshot of their data and re-upload it next session. No backend needed — user owns their file. Enables all features below. Paid version could offer platform-managed storage. | new `app/modules/storage.py`, `main.py` | — | ⬜ |
| 11 | **Monthly Check-in + Score Delta** | User returns next month, re-enters updated numbers, sees score change: "Last month: 58 → This month: 65 (+7 pts)". Core retention loop. Needs snapshot storage to compare against previous session. | `main.py`, `panel_results.py`, `storage.py` | #10 | ⬜ |
| 12 | **Goal Tracker** | User sets ONE financial goal tied to Module 5's action (e.g. "Build 3-month emergency fund"). Progress bar shows how far they are. Gives users a north star between monthly check-ins. | new `app/modules/goals.py`, `panel_results.py` | #10, #11 | ⬜ |
| 13 | **User-configurable Metric Weights** | Let users set priority % for each metric — different life situations need different focus. A student should weight DTI differently than someone close to retirement. | `health.py`, `panel_results.py` | — | ⬜ |
| 14 | **Export Settings** | Download JSON/CSV of financial snapshot + metric scores. Useful for sharing with an advisor or importing into a spreadsheet. Depends on storage format being in place. | `main.py`, new `export.py` | #10 | ⬜ |

---

## P3 — Long Term / Big Bets

| # | Feature | What + Why | Done |
|---|---------|------------|------|
| 15 | **Bank Connection (Plaid)** | Auto-pull real transaction data from the user's bank. Changes FinFriend from "estimate your situation" to "here's your actual situation." High effort, compliance considerations, changes the product identity. Worth revisiting once P0–P2 are stable. | ⬜ |

---

## Dropped

| Feature | Reason |
|---------|--------|
| **Budget Planner Sheet** | High effort, commoditized space (YNAB, Mint, Google Sheets do this better). FinFriend's edge is diagnosis and narrative, not data entry. The intent (help users plan where money goes) is better served by the What-If Simulator (#3) and Goal Tracker (#12). |
| **Module 5: One Next Step** | Redundant. The narrative's Q4 ("What should you do this month?") already is the one next step. A separate section would repeat it. |
| **Guided Estimation Flow** | Partially solved already by the form framing change and caption hints. Interactive inline calculators would be overengineering at this stage. |

---

## Completed

| # | Feature | Done |
|---|---------|------|
| — | **Expense Benchmark Hints** | ✅ |
| — | **Module 1: Financial Snapshot** | ✅ |
| — | **Module 2: Health Score + Mirror** | ✅ |
| — | **Module 3: AI Narrative** | ✅ |
| — | **Module 4: Contextual Education** | ✅ |

---

## How to use this file
- Pick a feature by number, bring it up in conversation
- Do NOT load this file into context unless actively working on a feature
- When starting a feature, note which other features it depends on
