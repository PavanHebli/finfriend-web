# FinFriend — Product Thinking & Design Decisions

This document explains the reasoning behind FinFriend: why it exists, what it deliberately does and does not do, and the decisions made along the way. It is written for anyone who wants to understand the product thinking, not just the code.

---

## Why FinFriend exists

I built FinFriend because I personally felt weak at finances.

Before making any financial decisions I realised I had no visibility — money came in, money went out, and I had no clear picture of where it went or whether I was making good choices. I knew vaguely that saving was important, that debt was bad, that I should think about the future. But I had no framework for understanding *how well I was actually doing* or *what I should do next*.

Most finance tools show you charts and numbers. That did not help me. I needed something that looked at my situation and said: here is what is actually going on, here is what is a problem, here is what to do about it — in plain language, without assuming I already understood financial concepts.

That is the gap FinFriend fills.

---

## Why AI narrative instead of charts

Most personal finance apps are built for people who already understand money. They show dashboards, graphs, percentage breakdowns. If you know what a debt-to-income ratio is, that is useful. If you do not, it is just a number.

The AI narrative exists to bridge that gap. Instead of showing a DTI of 38% and leaving the user to figure out if that is good or bad, FinFriend tells a story: what your numbers mean, what is working, what needs attention, and what to do this month — in plain language that does not require any financial background to understand.

The flexibility of natural language also means the explanation can be contextual. A 38% DTI means something different for a 24-year-old student than for a 40-year-old with a mortgage. Charts cannot carry that nuance. A narrative can.

The goal: someone who has never thought seriously about their finances should be able to read the output and feel like they understand their situation — without learning a single financial term.

---

## Why industry benchmarks for scoring

The health score (0–100) is built on four metrics, each scored against published industry standards:

| Metric | Benchmark | Source |
|--------|-----------|--------|
| Savings rate | 20% target | 50/30/20 rule |
| Debt-to-income | 43% maximum | CFPB qualified mortgage threshold |
| Emergency fund | 3–6 months | Fidelity / Vanguard guidelines |
| Housing ratio | 30% maximum | HUD affordability standard |

These are not arbitrary numbers. They are the same thresholds that banks, government agencies, and financial institutions use. This matters because the score needs to be trustworthy — users should feel confident that a score of 65 means something real, not something made up.

Every benchmark is documented. Users can look up the CFPB, HUD, or Fidelity guidelines and verify that the standards FinFriend uses are legitimate.

---

## Why open source

Two reasons.

First, the practical one: I was building a mobile app privately and the development was slow. The learning curve was steep and there was no feedback loop — just me, the code, and no users. Switching to an open, public approach meant I could get a working product in front of real people much faster, learn from how they used it, and build in the direction that actually mattered.

Second, the bigger reason: if something is genuinely useful, open source lets it grow beyond what one person can build. I came across the journey of opencode — a project that built something meaningful in the open and found an audience that cared about it. That model made sense to me. Transparency builds trust. If the tool is good, openness helps it spread.

There is also a third, honest reason: if the product never takes off, the code and the decisions documented here are a real portfolio of product thinking and engineering. Either way, the time is not wasted.

---

## Why build on AI now

AI gets used a lot these days, often for things that do not need it. Finance is different. Financial concepts are genuinely hard for most people — not because people are not smart, but because the education system does not teach it, the jargon is alienating, and most tools are built for people who already know what they are doing.

People are already turning to ChatGPT to understand their finances. They are asking "is my savings rate good?" and "what does debt-to-income mean?" FinFriend is a structured framework built on top of that behaviour — instead of an open-ended chat, it takes your actual numbers, applies real benchmarks, and gives you a grounded, personalised explanation.

The AI is not the product. The product is financial clarity. The AI is what makes that clarity accessible to people who would otherwise not know where to start.

---

## What FinFriend deliberately does not do

**It does not track your spending in real time.**
FinFriend is a diagnostic, not a tracker. You come to it when you want to understand your situation — monthly, or when something changes. Real-time tracking is a different product (Mint, YNAB) and a much harder infrastructure problem. FinFriend's value is in the analysis and the story, not in the data collection.

**It does not connect to your bank.**
Bank connections require OAuth integrations, compliance considerations, and significant infrastructure. More importantly, they change the relationship with the user — suddenly the app holds sensitive access to their accounts. That is a different level of trust and a different product. The current approach (user enters their own numbers) keeps the user in control and keeps the product simple.

**It does not have a budget planner.**
A budget planner — where you allocate income into custom goal buckets — is a commoditised feature. Every spreadsheet app does it. YNAB does it better than any web app could. Building it in FinFriend would be high effort, low differentiation, and would pull the product away from its core strength: diagnosis and narrative. The intent behind a budget planner (help users plan where money goes) is better served by the What-If Simulator — which shows you instantly how a spending change affects your score.

**It does not give investment advice.**
FinFriend operates at the level of financial health fundamentals — savings rate, debt, emergency fund, housing. Investment strategy is a separate domain that requires much more context (risk tolerance, time horizon, existing portfolio) and carries regulatory considerations. Getting the fundamentals right comes first. Investment guidance is a later feature.

---

## The core design principle

People would turn to AI to understand their finances eventually anyway. FinFriend just gives them a structured framework to do it — one grounded in real benchmarks, personalised to their actual numbers, and explained in language that does not require a finance degree.

The goal is not to be the most powerful finance tool. The goal is to be the one that makes the most people feel like they finally understand their own money.

---

*Built by Pavan Hebli · Open source · MIT License*
