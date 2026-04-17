"""
Classifier unit test — runs outside Streamlit, no UI needed.

Usage:
    OPENAI_API_KEY=sk-... python tests/test_classifier.py

Optional: override provider
    PROVIDER=groq GROQ_API_KEY=... python tests/test_classifier.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))

from modules.chat import classify_question

PROVIDER = os.environ.get("PROVIDER", "openai")
KEY_MAP  = {
    "openai":    "OPENAI_API_KEY",
    "groq":      "GROQ_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "gemini":    "GEMINI_API_KEY",
}
API_KEY = os.environ.get(KEY_MAP[PROVIDER], "")
if not API_KEY:
    print(f"[ERROR] Set {KEY_MAP[PROVIDER]} environment variable first.")
    sys.exit(1)

# (question, expected_categories_as_set)
# Order doesn't matter — we compare sets.
TEST_CASES = [

    # --- SCORE — asking about the scoring system, why a metric is at a level ---
    ("Why is my DTI score so low?",                              {"score"}),
    ("How does my health score work?",                          {"score"}),
    ("Why did my score go down?",                               {"score"}),
    ("What does a score of 63 mean?",                           {"score"}),
    ("how are you calculating the health score?",                     {"score"}),
    ("Why is my savings rate score only 10 out of 25?",         {"score"}),
    ("What do I need to do to move from Fair to Good?",         {"score"}),

    # --- DEBT — strategy, payoff, DTI as a debt problem ---
    ("I have $20k in debt, where do I start?",                  {"debt"}),
    ("Should I do debt avalanche or snowball?",                 {"debt"}),
    ("My credit card interest is killing me, what do I do?",   {"debt"}),
    ("Is it better to pay off debt or invest?",                 {"debt"}),
    ("How do I get my DTI under control?",                      {"debt"}),

    # --- SAVINGS — rate, emergency fund, building savings ---
    ("What is a Roth IRA?",                                     {"savings"}),
    ("How much emergency fund do I need?",                      {"savings"}),
    ("I want to start investing, where do I begin?",            {"savings"}),
    ("What is the 50/30/20 rule?",                              {"savings"}),
    ("Should I use a high yield savings account?",              {"savings"}),

    # --- HOUSING ---
    ("Should I rent or buy a house?",                           {"housing"}),
    ("My rent is really high, what can I do?",                  {"housing"}),
    ("Is my housing ratio too high?",                           {"housing"}),
    ("What are the hidden costs of buying a home?",             {"housing"}),

    # --- INSURANCE ---
    ("What type of life insurance should I get?",               {"insurance"}),
    ("Do I need disability insurance?",                         {"insurance"}),
    ("What is the difference between an HSA and PPO?",          {"insurance"}),
    ("Should I get term or whole life insurance?",              {"insurance"}),

    # --- APP — how Vitals features work ---
    ("How does the What-If simulator work?",                    {"app"}),
    ("How do I save my progress in Vitals?",                    {"app"}),
    ("What is the .fin file?",                                  {"app"}),
    ("How do I load a previous snapshot?",                      {"app"}),
    ("What does the Progress tab show?",                        {"app"}),
    ("How do I get an API key?",                                {"app"}),

    # --- SCENARIO — what-if planning, secondary = topic being modelled ---
    ("What if I paid an extra $300/month toward debt?",         {"scenario", "debt"}),
    ("What would happen to my score if I cut dining by $150?",  {"scenario", "score"}),
    ("What if I moved to a cheaper apartment?",                 {"scenario", "housing"}),
    ("What if I started saving $500 more per month?",           {"scenario", "savings"}),
    ("How much would my score improve if I paid off my car loan?", {"scenario", "score"}),

    # --- EMOTIONAL as secondary ---
    ("I feel completely overwhelmed by my debt",                {"debt", "emotional"}),
    ("I'm drowning in debt and don't see a way out",            {"debt", "emotional"}),
    ("I'm so stressed about money I can't sleep",               {"general", "emotional"}),
    ("I feel like I've wasted my 20s financially",              {"general", "emotional"}),
    ("I'm embarrassed by how bad my finances are",              {"general", "emotional"}),

    # --- GENERAL — casual, identity, conceptual ---
    ("How are you?",                                            {"general"}),
    ("What model are you?",                                     {"general"}),
    ("What is inflation?",                                      {"general"}),
    ("Can you explain compound interest?",                      {"general"}),

    # --- MULTI-TOPIC → general or scenario ---
    ("I want to buy a house, quit my job, and have a kid",     {"scenario", "general"}),
    ("Should I pay off debt, invest, and also move cities?",   {"general"}),
]

passed = failed = 0
print(f"\nRunning {len(TEST_CASES)} classifier tests  [provider: {PROVIDER}]\n")
print(f"{'STATUS':<8} {'RESULT':<25} {'EXPECTED':<25} QUESTION")
print("-" * 100)

for question, expected in TEST_CASES:
    result    = classify_question(question, PROVIDER, API_KEY)
    result_set = set(result)
    # Accept a match if result is a subset of expected OR expected is a subset of result
    # (emotional as secondary is acceptable when not expected, but wrong primary is a failure)
    primary_ok    = result[0] in expected or list(expected)[0] == result[0]
    exact_match   = result_set == expected
    ok = exact_match or (result[0] in expected and len(result_set - expected) == 0)

    status = "✅ PASS" if ok else "❌ FAIL"
    print(f"{status:<8} {'/'.join(result):<25} {'/'.join(sorted(expected)):<25} {question[:55]}")
    if ok:
        passed += 1
    else:
        failed += 1

print("-" * 100)
print(f"\n{passed}/{passed + failed} passed", end="")
if failed:
    print(f"  ← {failed} failure(s) to investigate")
else:
    print("  — all good")
print()
