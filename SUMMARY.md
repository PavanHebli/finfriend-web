# FinFriend — Complete Development Summary

> This file is the single source of truth for new sessions. Read this before touching any code.
> For product thinking and design rationale, read DECISIONS.md.
> For the feature backlog, read TODO.md.

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Current State](#current-state)
3. [Project Structure](#project-structure)
4. [Architecture & Data Flow](#architecture--data-flow)
5. [Session State Reference](#session-state-reference)
6. [Functions Implemented](#functions-implemented)
7. [Streamlit Patterns & Pitfalls](#streamlit-patterns--pitfalls)
8. [Issues Encountered and Fixes](#issues-encountered-and-fixes)
9. [Design Decisions Log](#design-decisions-log)
10. [Running the App](#running-the-app)
11. [What to Build Next](#what-to-build-next)

---

## Project Overview

**FinFriend** is an open-source personal finance app built with Python + Streamlit. It takes a user's financial data, scores it against industry benchmarks, generates an AI narrative, and gives contextual education — all in plain language.

**Live app:** https://finfriend-web.streamlit.app/
**License:** MIT
**LLM Providers:** Anthropic (claude-opus-4-6), OpenAI (gpt-4o), Groq (llama-3.3-70b-versatile), Gemini (gemini-1.5-flash)
**User brings their own API key.**

### The 5 Modules
| Module | Description | Status |
|--------|-------------|--------|
| 1 — Financial Snapshot | Form collecting income, expenses, savings, debt, context | ✅ Done |
| 2 — Health Score + Mirror | Scores finances across 4 industry-standard metrics (0–100) | ✅ Done |
| 3 — AI Narrative | Streams a Q&A narrative: picture, working, attention, action | ✅ Done |
| 4 — Contextual Education | Pre-written "why this matters" for flagged metrics | ✅ Done |
| 5 — One Next Step | Lives inside narrative Q4 ("What should you do this month?") | ✅ Done |

---

## Current State

### What the app does end-to-end

1. User fills the form (Panel 1): income, 7 expense categories, savings/investments/debt, context (age, employment, insurance, 401k)
2. Validation: API key required + income > 0. Without these, CTA is blocked.
3. User clicks "Show me my financial picture →" → switches to Panel 2 (results)
4. Results panel renders:
   - Health score (0–100) + mirror label (Critical / At Risk / Fair / Good / Healthy)
   - Metrics breakdown: savings rate, DTI, emergency fund, housing ratio — each with status dot and score/25
   - Net monthly cash flow
   - **3 tabs below the breakdown:**
     - **Tab 1 — Your Financial Story:** AI narrative streams once, cached in session state. Subsequent tab switches show cached text (no re-stream). Education expander ("Why this matters") shown below narrative for flagged metrics only.
     - **Tab 2 — What If?:** Interactive simulator with 5 sliders (income, dining, shopping, subscriptions, debt payment). Shows score delta, cash delta, and raw metric deltas live.
     - **Tab 3 — Ask FinFriend:** Placeholder. Decision Helper not yet built.

### What happens on "← Edit my data"
- Clears `narrative_text` from session state (forces re-stream on next results visit)
- Clears all `sim_*` keys (forces simulator sliders to reseed from new form values)
- Sets `current_page = "form"` + `st.rerun()`

---

## Project Structure

```
finfriend/
├── requirements.txt              # all dependencies
├── README.md                     # public-facing, live app link
├── DECISIONS.md                  # product thinking + design rationale
├── summary.md                    # this file — full dev context
├── TODO.md                       # prioritised feature backlog
├── .gitignore
└── app/
    ├── main.py                   # page config + session state init + panel routing
    └── modules/
        ├── snapshot.py           # Module 1: all form section render functions
        ├── health.py             # Module 2: pure calculation logic (no Streamlit)
        ├── narrative.py          # Module 3: build_prompt() + call_llm() streaming
        ├── education.py          # Module 4: education content + render function
        ├── simulator.py          # What-If Simulator: sliders + live recalculation
        ├── panel_form.py         # Panel 1 UI: form, toggle, clear, CTA
        └── panel_results.py      # Panel 2 UI: score, breakdown, 3 tabs
```

---

## Architecture & Data Flow

```
User fills form (panel_form.py)
    ↓ session state holds all values
CTA clicked → validate → set current_page="results" → st.rerun()
    ↓
panel_results.py renders:
    calculate_metrics(st.session_state)      → health.py (pure math)
    score_metrics(metrics)                   → health.py (pure math)
    calculate_overall_score(metric_scores)   → health.py
    get_mirror_label(score)                  → health.py
    ↓
    render_health_score()                    → centered score + label
    render_metrics_breakdown()               → 4-row table + net flow
    ↓
    Tab 1: build_prompt() → call_llm() → st.write_stream() → cache result
           render_education()
    Tab 2: render_whatif_simulator()         → simulator.py
    Tab 3: placeholder
```

**health.py has zero Streamlit imports.** All UI lives in panel files. This separation is intentional — health.py can be tested independently.

---

## Session State Reference

### Form data keys (set by snapshot.py / panel_form.py)
| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `llm_provider` | str | "anthropic" | Selected AI provider |
| `api_key` | str | "" | User's API key |
| `income_main` | float | 0.0 | Monthly take-home income |
| `income_additional` | float | 0.0 | Freelance / side income |
| `expenses_rent` | float | 0.0 | Rent or mortgage |
| `expenses_groceries` | float | 0.0 | Groceries |
| `expenses_transport` | float | 0.0 | Transport |
| `expenses_subscriptions` | float | 0.0 | Subscriptions |
| `expenses_dining` | float | 0.0 | Dining out / delivery |
| `expenses_shopping` | float | 0.0 | Shopping / personal |
| `expenses_other` | float | 0.0 | Other expenses |
| `savings_total` | float | 0.0 | Total savings (checking + savings) |
| `investments_total` | float | 0.0 | Total investments |
| `debt_total` | float | 0.0 | Total debt |
| `debt_monthly` | float | 0.0 | Monthly debt payments |
| `age` | int | 25 | Age |
| `employment` | str | "Employed" | Employment status |
| `has_health_insurance` | bool | False | Health insurance (stored as bool, shown as Yes/No in prompt) |
| `has_emergency_fund` | str | "Not sure" | Emergency fund status |
| `contributing_401k` | str | "No" | 401k contribution status |

### Navigation + UI state keys
| Key | Type | Description |
|-----|------|-------------|
| `current_page` | str | "form" or "results" — controls which panel renders |
| `sample_input_active` | bool | Whether sample data toggle is on |

### Results page cache keys (set by panel_results.py)
| Key | Type | Description |
|-----|------|-------------|
| `narrative_text` | str | Cached narrative after first stream. Cleared on "← Edit my data". |

### Simulator keys (set by simulator.py)
| Key | Type | Description |
|-----|------|-------------|
| `sim_income` | int | Slider value for total income |
| `sim_dining` | int | Slider value for dining |
| `sim_shopping` | int | Slider value for shopping |
| `sim_subscriptions` | int | Slider value for subscriptions |
| `sim_debt_payment` | int | Slider value for monthly debt payment |
| `sim_reset` | bool | Flag set by Reset button, consumed before sliders render |

All `sim_*` keys are cleared when user clicks "← Edit my data".

---

## Functions Implemented

### `app/main.py`
- **`init_session_state()`** — Sets all keys to defaults if not already present. Runs on every page load.
- **`main()`** — Sets page config, calls init, routes to form or results panel based on `current_page`.

### `app/modules/snapshot.py` — Module 1
- **`render_api_config()`** — Provider selectbox + API key password input. Returns `(provider, api_key)`.
- **`render_income_section()`** — Main + additional income inputs. Returns `(main_income, additional_income)`.
- **`render_expenses_section()`** — 7 expense inputs with benchmark captions and estimation hints. Returns `expenses` dict.
- **`render_position_section()`** — Savings, investments, debt, monthly debt payments. Returns tuple of 4.
- **`render_context_section()`** — Age, employment, insurance (radio), emergency fund, 401k. Returns tuple of 5.

### `app/modules/health.py` — Module 2 (no Streamlit)
- **`calculate_metrics(state)`** — Takes session state dict. Returns: `savings_rate`, `debt_to_income`, `emergency_fund_months`, `housing_ratio`, `net_monthly_flow`, `debt_payment_missing`. Edge case: expenses=0 + income>0 → emergency_fund = savings/income. `debt_payment_missing = debt_total > 0 and debt_monthly = 0`.
- **`score_metrics(metrics)`** — Returns per-metric `{score: 0-25, status: danger|warning|ok|good}`. Net flow returned as raw value only (not scored). If `debt_payment_missing` is True, DTI is capped at danger (0/25) regardless of calculated DTI.
- **`calculate_overall_score(metric_scores)`** — Sums 4 scored metrics. Returns 0–100.
- **`get_mirror_label(score)`** — Returns `{label, description}`. Labels: Critical (≤30), At Risk (≤50), Fair (≤70), Good (≤85), Healthy (>85).

**Scoring benchmarks:**
| Metric | Danger | Warning | OK | Good |
|--------|--------|---------|-----|------|
| Savings rate | <0% | <10% | <20% | ≥20% |
| Debt-to-income | >43% | >20% | >10% | ≤10% |
| Emergency fund | <1 mo | <3 mo | <6 mo | ≥6 mo |
| Housing ratio | >50% | >35% | >25% | ≤25% |

### `app/modules/narrative.py` — Module 3
- **`build_prompt(state, metrics, metric_scores, overall_score, mirror)`** — Full LLM prompt. Q&A format with 4 bold-header questions. Rules: 50-60 words per answer, banned vague adjectives (decent, solid, fairly, etc.), numbers always paired with meaning, ONE action in Q4, health insurance shown as Yes/No not True/False. Includes: zero-value rules (debt_payment_missing treated as DANGER, not just data gap), minimum expense floors per category (rent never cut directly, groceries floor $250, transport $200, subscriptions $75).
- **`call_llm(prompt, provider, api_key)`** — Generator yielding text chunks. Used with `st.write_stream()`. Supports all 4 providers.

### `app/modules/education.py` — Module 4
- **`get_education(metric_scores)`** — Returns list of education items for danger/warning metrics only. Skips net_monthly_flow and ok/good metrics.
- **`render_education(metric_scores)`** — Renders `st.expander("Why this matters")` with color-coded titles. Only shown when at least one metric is flagged.

### `app/modules/panel_form.py` — Panel 1
- **`fill_sample_data()`** — Sets all session state fields to randomised realistic floats. All values cast to `float()` explicitly.
- **`clear_all_fields()`** — Resets all fields to defaults + sets `sample_input_active = False`.
- **`render_form_panel()`** — Renders title, Sample Input toggle (uses `value=` not `key=`), Clear All button, framing note, and `st.form()` wrapper. Previous-state tracking for toggle to avoid calling fill/clear on every rerun.

### `app/modules/panel_results.py` — Panel 2
- **`render_health_score(score, mirror)`** — Centered score (X/100) + color-coded label + description.
- **`render_metrics_breakdown(metrics, metric_scores)`** — 4-row table with colored status dots and score/25. Net flow shown below in green/red.
- **`render_expense_chart(state, metrics, metric_scores)`** — Plotly horizontal bar chart. Shows each expense category as % of income, sorted largest to smallest. All bars same neutral color (#4A90D9). Dashed 30% reference line (HUD benchmark). Skips zero-value categories.
- **`render_results_panel()`** — Full results page. Back button clears `narrative_text` + all `sim_*` keys. Score + breakdown + expense chart always visible above tabs. 3 tabs below.

### `app/modules/simulator.py` — What-If Simulator
- **`_seed_sim_values()`** — Seeds `sim_*` session state keys from current form values. Called before sliders render (never after).
- **`render_whatif_simulator(current_score, current_metric_scores)`** — 5 sliders, each with `help=` tooltip explaining: what the metric is, its target benchmark, and which sliders affect it. Reset uses `sim_reset` flag pattern. Shows score delta, cash delta, and 4 raw metric deltas with correct `delta_color` direction (inverse for DTI and housing ratio). `delta_color="off"` when delta=0 to avoid misleading colored arrows.

---

## Streamlit Patterns & Pitfalls

These are non-obvious Streamlit behaviours that caused bugs during development. Read before writing any new UI code.

### 1. Widget key rule — never modify after instantiation
```python
# WRONG — raises StreamlitAPIException
st.slider("Income", key="sim_income")
st.session_state.sim_income = 5000  # error: already instantiated

# RIGHT — set value BEFORE the widget renders
st.session_state.sim_income = 5000
st.slider("Income", key="sim_income")
```

### 2. Flag pattern for reset buttons
When a button needs to reset a widget's value, it cannot call the setter directly (widget already rendered). Use a flag + rerun:
```python
# Button sets flag + reruns
if st.button("Reset"):
    st.session_state.sim_reset = True
    st.rerun()

# Top of next render — BEFORE widgets — check and consume the flag
if st.session_state.pop("sim_reset", False) or "sim_income" not in st.session_state:
    _seed_sim_values()  # runs BEFORE sliders render → no error

# Then render sliders normally
st.slider(..., key="sim_income")
```

### 3. Toggle — use value= not key=
```python
# WRONG — StreamlitAPIException when clear_all_fields() tries to set sample_toggle
sample_on = st.toggle("Sample Input", key="sample_toggle")

# RIGHT — no key, use value= + separate state variable
previous = st.session_state.get("sample_input_active", False)
sample_on = st.toggle("Sample Input", value=previous)
st.session_state.sample_input_active = sample_on
```

### 4. Previous-state tracking for toggle
```python
# Only call fill/clear when state ACTUALLY changes — not on every rerun
if sample_on and not previous:      # just turned ON
    fill_sample_data()
elif not sample_on and previous:    # just turned OFF
    clear_all_fields()
# If neither — do nothing
```

### 5. Mixed numeric types error
```python
# WRONG — StreamlitMixedNumericTypesError (value=int, step=float)
st.number_input("Income", value=5000, step=100.0)

# RIGHT — all same type
st.number_input("Income", value=5000.0, step=100.0)
# fill_sample_data() must cast all values explicitly: float(random.choice([...]))
```

### 6. Dollar signs in st.markdown() trigger LaTeX
```python
# WRONG — $8,000 renders as vertical character-by-character LaTeX math
st.markdown("You earn $8,000 monthly")

# RIGHT — escape dollar signs before passing to st.markdown()
st.markdown(text.replace("$", "\\$"))
```
Note: `st.write_stream()` handles dollar signs correctly during live streaming. The escaping is only needed when displaying cached/static text via `st.markdown()`.

### 7. Tab switches cause full reruns — cache the narrative
```python
# Without caching — narrative re-streams every time user clicks a tab
# With caching:
if "narrative_text" not in st.session_state:
    result = st.write_stream(call_llm(...))        # streams once
    st.session_state.narrative_text = result        # cache it
else:
    st.markdown(st.session_state.narrative_text.replace("$", "\\$"))  # instant
```
Clear `narrative_text` on "← Edit my data" so the next visit re-streams with updated data.

### 8. st.rerun() required for panel switching
```python
# WRONG — flag set but panel doesn't switch; main() already ran past the routing logic
if st.button("Go to results"):
    st.session_state.current_page = "results"

# RIGHT
if st.button("Go to results"):
    st.session_state.current_page = "results"
    st.rerun()
```

---

## Issues Encountered and Fixes

| Issue | Root Cause | Fix |
|-------|-----------|-----|
| CTA required two clicks to switch panels | `main()` reads `current_page` before the button sets it — change only takes effect next rerun | Add `st.rerun()` after setting `current_page` |
| Score showed 60/100 with empty form | `debt=0` and `housing=0` both score "good" giving a false 60/100 | Block CTA if `income=0`, not just if `api_key` is empty |
| `StreamlitAPIException: sample_toggle cannot be modified` | `clear_all_fields()` tried to set `st.session_state.sample_toggle` after the toggle widget was already instantiated | Remove `key=` from toggle; use `value=` + separate `sample_input_active` variable |
| `StreamlitMixedNumericTypesError` | `fill_sample_data()` set int values but `step=` was float — Streamlit requires all numeric args to be the same type | Cast all values in `fill_sample_data()` to `float()` |
| Missing Submit Button error | `clear_all_fields()` was called on every rerun (not just on toggle state change), causing mid-render form interruption | Previous-state tracking — only call fill/clear when toggle state actually changes |
| `StreamlitAPIException: sim_income cannot be modified` | Reset button called `_seed_sim_values()` directly after sliders were already rendered | Flag pattern: button sets `sim_reset=True` + reruns; flag consumed before sliders render on next pass |
| Narrative re-streams on every tab switch | Tab clicks trigger full reruns; no caching in place | Cache `st.write_stream()` result in `narrative_text` session state; clear on "← Edit my data" |
| Dollar signs render as vertical LaTeX in cached narrative | `st.markdown()` treats `$` as a LaTeX math delimiter | Escape with `.replace("$", "\\$")` before passing to `st.markdown()` |
| Simulator score only changes with income slider | Scoring uses fixed tiers — small expense changes don't cross thresholds; income affects all 4 ratios simultaneously | Added raw metric deltas below the score metrics so users see continuous changes even within a tier |
| `watchdog=>6.0.0` in requirements.txt invalid | Wrong operator `=>` instead of `>=` | Fixed to `>=` |
| `anthropic` module not found on Streamlit Cloud | Library not installed in active venv | `pip install -r requirements.txt` in the correct active environment |

---

## Design Decisions Log

| Topic | Decision |
|-------|----------|
| API key + income validation | Both required to reach results panel |
| Optional fields | Default to 0.0 |
| LLM providers | Anthropic (claude-opus-4-6), OpenAI (gpt-4o), Groq (llama-3.3-70b-versatile), Gemini (gemini-1.5-flash) |
| health.py isolation | Pure logic, zero Streamlit imports — UI only in panel files |
| Scoring | 4 metrics × 25pts = 100. Net flow shown as raw value, not scored |
| Benchmarks | CFPB (DTI 43%), HUD (housing 30%), Fidelity/Vanguard (emergency 3-6mo), 50/30/20 rule (savings 20%) |
| Narrative format | Q&A: 4 fixed bold-header questions, 50-60 words each, banned vague adjectives, numbers always paired with meaning |
| Module 5 | Not a separate section — lives inside narrative Q4 ("What should you do this month?") |
| Panel navigation | `current_page` session state + `st.rerun()` on every navigation action |
| Results page layout | Score + breakdown always visible above tabs. Tabs: Story / What If? / Ask FinFriend |
| Narrative caching | `st.write_stream()` return value stored in `narrative_text`. Cleared on "← Edit my data". |
| Simulator state isolation | `sim_*` keys separate from form keys. Cleared on "← Edit my data" so sliders reseed from new form values |
| Simulator score sensitivity | Score tiers are coarse — show raw metric deltas alongside score delta for continuous feedback |
| Toggle state | `value=` not `key=` on `st.toggle()`. Previous-state comparison to detect ON/OFF transitions |
| Dollar signs in markdown | Escape with `.replace("$", "\\$")` before `st.markdown()` — streaming handles natively |
| Budget planner | Dropped — commoditised, high effort, off-brand. Simulator covers the planning intent better |
| Guided estimation flow | Dropped — sufficiently addressed by form framing change + benchmark captions |
| Module 5 as separate section | Dropped — redundant with narrative Q4 |
| Debt payment missing | `debt_total > 0` + `debt_monthly = 0` → scored as danger (0/25), not warning. Flagged in narrative as DANGER: missing debt payments harm credit, trigger penalty interest, risk collections. |
| Minimum expense floors | Prompt explicitly tells AI the per-category minimums before it can suggest cuts. Prevents bad advice on already-minimal expenses. |
| Expense chart bar colors | Rent/Mortgage bar is colored by housing ratio status (danger/warning/ok/good). All other bars are neutral (#4A90D9). |

---

## Running the App

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run from project root
```bash
PYTHONPATH=. streamlit run app/main.py
```

### Run from app directory
```bash
cd app
streamlit run main.py
```

Open browser at `http://localhost:8501`

### Reset stale session state
If you see unexpected errors after code changes, clear the browser session:
- Open Streamlit hamburger menu (top right) → Clear cache
- Hard refresh: `Cmd+Shift+R` (Mac) / `Ctrl+Shift+R` (Windows)

---

## What to Build Next

### Immediate — P0 remaining
| Feature | What | Where |
|---------|------|-------|
| **Decision Helper** | Chat input in Tab 3. User asks financial questions ("I got a raise — what should I do?"). AI answers using full session context. Mostly a prompt + chat UI. | `panel_results.py` Tab 3, new `decision.py` |

### After that — P1
| Feature | What |
|---------|------|
| CSV / Bank Statement Import | User uploads bank CSV → auto-fills expense form. Solves "I don't know my numbers" problem. |
| Metric Citations | Show CFPB/HUD source next to each metric in the breakdown. Builds trust. |
| AI Personas | Narrative tone selector: Honest Friend / Finance Professional / Coach / Tough Love. |

### Infrastructure needed before P2
Cloud storage (download/upload JSON snapshot, or Google Drive) is required before: monthly check-in + score delta, goal tracker, export settings.

Full backlog with priorities in TODO.md.
