# FinFriend — Product Thinking & Design Decisions

This document captures how we think about FinFriend — the product, the architecture, and the choices made along the way. Written for anyone who wants to understand the reasoning, not just the code.

---

## The problem

Most personal finance tools are built for people who already understand money. They show dashboards, ratios, and percentage breakdowns. If you know what a debt-to-income ratio is, that is useful. If you do not, it is just a number.

FinFriend exists for the second group. Not because they are less capable, but because financial education is genuinely poor — the jargon is alienating, the concepts are taught nowhere, and most tools assume fluency you never got. The goal is to look at someone's actual numbers and say: here is what is going on, here is what is a problem, here is what to do about it — in plain language, without assuming any prior knowledge.

The AI is not the product. The product is financial clarity. The AI is what makes that clarity accessible.

---

## The score

The health score (0–100) is built on four metrics, each benchmarked against published industry standards: savings rate (50/30/20 rule, 20% target), debt-to-income (CFPB qualified mortgage threshold, 43% max), emergency fund (Fidelity/Vanguard, 3–6 months), and housing ratio (HUD affordability standard, 30% max). These are the same thresholds banks, government agencies, and financial institutions use — not arbitrary numbers.

One deliberate deviation: FinFriend uses take-home income for DTI, not gross. The CFPB standard uses gross. We use take-home because your rent and debt payments come out of what actually hits your bank account — not what you earn before tax. This makes FinFriend's DTI stricter than a lender's calculation. That is intentional. The tool's job is an honest picture, not telling users what they want to hear. The choice is disclosed on the results page and in the simulator tooltip.

---

## Language over charts

A 38% DTI means something different for a 24-year-old student than for a 40-year-old with a mortgage. Charts cannot carry that nuance. A narrative can.

The AI narrative streams four answers: what the overall picture looks like, what is working, what needs attention, and one concrete action to take this month. Every answer is grounded in the user's specific numbers — not generic advice. Vague adjectives are banned from the prompt (decent, solid, fairly, significant). Numbers must always be paired with what they mean in real life.

The goal: someone who has never thought seriously about their finances reads the output and feels like they understand their situation — without learning a single financial term.

---

## Your data

FinFriend saves snapshots as `.fin` files rather than plain JSON. The format is branded — `.fin` signals clearly that this is a FinFriend file. More importantly, plain JSON is readable by anyone. A file on a shared computer, in a cloud sync folder, or accidentally emailed would expose income, debt, and savings to anyone who opened it. Fernet encryption (AES-128-CBC + HMAC) prevents that. The key is baked into the app — no password friction, no "forgot my password" problem. The threat model is accidental exposure, not a determined attacker.

One file holds all months. Same-month saves overwrite. Re-downloading replaces the old file in the downloads folder naturally. The user manages one file, not twelve.

Progress charts include the current unsaved session as a live point — hollow marker, dotted line. This is deliberate. If a user just updated their income or cut a budget item, they should immediately see where that puts them on the trend line without needing to save first. The hollow marker signals it is a preview, not a confirmed entry.

---

## FinFriend Chat

**The friend model, not the compliance model.** The chat is designed to feel like a financially savvy friend — warm, direct, honest, and specific. Not a textbook and not a compliance officer. The guardrails exist to keep the chat useful, not to make it restrictive. A friend who knows finance will tell you about types of investments, explain how insurance works, and discuss income strategies — they just will not tell you to buy a specific stock or sign up for a specific platform.

The line is specificity, not topic. Categories and strategies are always fine. Specific company names, buy/sell calls, and product endorsements are not. When pushed for a specific name, the response is: here is how to evaluate your options — not a flat refusal.

**Guardrail layers.** There are two: a keyword pre-filter blocks obvious out-of-scope requests (legal action, tax filing) before any API call is made. The system prompt handles everything else through a decision framework that teaches the model how to think about any question type — casual, core finance, finance-adjacent, borderline, off-topic, writing tasks, career advice, or requests for specific companies. A flat refusal is never the right response. Redirect warmly, or explain why you are not the right person and point to what would actually help.

**Emotional signals.** People often come to FinFriend not just with a financial question but with real weight behind it — feeling overwhelmed, stuck, or hopeless because of money. A good friend notices this. Emotional awareness is always active in the base prompt — not a separate mode, not something that only triggers for certain question types. When distress is detected: acknowledge briefly, pivot to the financial picture, use real numbers to show a path. The path IS the relief — most of the distress comes from not being able to see one. For severe signals, one gentle line about talking to someone is added. One line. Not the focus.

**Routed multi-prompt architecture.** Each question is classified before answering. The classifier is a fast, cheap LLM call — no base system prompt, just a classify instruction and the message — that returns 1–2 categories from: `debt`, `savings`, `housing`, `insurance`, `score`, `scenario`, `app`, `emotional`, `general`. Stripping the base prompt from the classifier saves ~800 tokens per call and keeps classification fast. A targeted category prompt is then injected on top of the always-present base prompt. If the classifier returns 2 categories, both blocks are injected. If 3+ topics genuinely mix, it routes to general.

A single generic prompt was considered and rejected. A generic prompt hedges across all question types and gives vaguer answers. A targeted debt prompt says "focus on this user's DTI at 52%" rather than dumping all eight metrics and hoping the model picks the right one.

**No external framework.** The tools are local Python functions in `health.py`. Native tool calling via each provider's SDK handles this — no LangChain, LlamaIndex, or LangGraph needed. All four providers support native tool calling. The framework is `chat.py` itself.

**Conversation summarisation.** Three tiers: full recent messages (last 6–8 turns), a rolling summary of older turns, and the user's financial snapshot which is always injected in full and never summarised or dropped. Token count stays bounded. The grounding that makes FinFriend Chat different from a generic chatbot is preserved.

---

## What FinFriend isn't

**Not a spending tracker.** FinFriend is a diagnostic. You come to it when you want to understand your situation — monthly, or when something changes. Real-time tracking is a different product (Mint, YNAB) and a harder infrastructure problem. The value is in the analysis and the story, not the data collection.

**Not connected to your bank.** Bank connections require OAuth, compliance work, and significant infrastructure. More importantly, they change the relationship — suddenly the app holds sensitive access to accounts. The current approach keeps the user in control and the product simple.

**Not a budget planner.** Commoditised. Every spreadsheet app does it. The intent (help users plan where money goes) is better served by the What-If Simulator — which shows instantly how a spending change affects the score.

**Not an investment advisor.** FinFriend operates at financial health fundamentals. Investment strategy requires more context (risk tolerance, time horizon, portfolio) and carries regulatory considerations. Getting the fundamentals right comes first.

**Not open source for altruistic reasons alone.** Building in the open meant getting a working product in front of real people faster, learning from how they used it, and building in the direction that actually mattered. If the product never takes off, the code and decisions here are a real portfolio of product thinking. Either way, the time is not wasted.

---

*Built by Pavan Hebli · Open source · MIT License*
