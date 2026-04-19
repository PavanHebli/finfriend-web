#!/usr/bin/env python3
"""
Generates a fake 14-month .vit file for testing the Progress Charts tab.
Shows a realistic improvement arc — user starts struggling, gradually gets better.

Usage:
    python tests/generate_fake_data.py
    # Outputs: tests/fake_data.vit
"""

import sys
import os
import base64
import json

from cryptography.fernet import Fernet

_RAW_KEY    = b'vitals__secret_key_v1___2026_!!!'
_FERNET_KEY = base64.urlsafe_b64encode(_RAW_KEY)
_cipher     = Fernet(_FERNET_KEY)

SNAPSHOTS = [
    {
        "saved_at": "2025-03",
        "version": "1",
        "inputs": {
            "income_main": 4200.0, "income_additional": 0.0,
            "expenses_rent": 1600.0, "expenses_groceries": 380.0,
            "expenses_transport": 300.0, "expenses_subscriptions": 150.0,
            "expenses_dining": 550.0, "expenses_shopping": 400.0, "expenses_other": 200.0,
            "savings_total": 400.0, "investments_total": 0.0,
            "debt_total": 14000.0, "debt_monthly": 420.0,
            "age": 28, "employment": "Employed",
            "has_health_insurance": False, "has_emergency_fund": "No", "contributing_401k": "No",
        },
        "outputs": {
            "overall_score": 18,
            "mirror_label": "Critical",
            "metrics": {
                "savings_rate": -9.5, "debt_to_income": 10.0,
                "emergency_fund_months": 0.1, "housing_ratio": 38.1,
                "net_monthly_flow": -400.0, "debt_payment_missing": False,
            },
            "metric_scores": {
                "savings_rate": {"score": 0, "status": "danger"},
                "debt_to_income": {"score": 18, "status": "ok"},
                "emergency_fund_months": {"score": 0, "status": "danger"},
                "housing_ratio": {"score": 0, "status": "danger"},
                "net_monthly_flow": {"value": -400.0},
            },
            "narrative": "Spending $400 more than you earn every month. Dining and shopping alone are nearly $1,000. No emergency fund, no insurance. One unexpected expense could spiral this fast.",
        },
    },
    {
        "saved_at": "2025-04",
        "version": "1",
        "inputs": {
            "income_main": 4200.0, "income_additional": 0.0,
            "expenses_rent": 1600.0, "expenses_groceries": 360.0,
            "expenses_transport": 290.0, "expenses_subscriptions": 130.0,
            "expenses_dining": 420.0, "expenses_shopping": 300.0, "expenses_other": 180.0,
            "savings_total": 600.0, "investments_total": 0.0,
            "debt_total": 14000.0, "debt_monthly": 420.0,
            "age": 28, "employment": "Employed",
            "has_health_insurance": False, "has_emergency_fund": "No", "contributing_401k": "No",
        },
        "outputs": {
            "overall_score": 24,
            "mirror_label": "Critical",
            "metrics": {
                "savings_rate": -4.3, "debt_to_income": 10.0,
                "emergency_fund_months": 0.2, "housing_ratio": 38.1,
                "net_monthly_flow": -180.0, "debt_payment_missing": False,
            },
            "metric_scores": {
                "savings_rate": {"score": 0, "status": "danger"},
                "debt_to_income": {"score": 18, "status": "ok"},
                "emergency_fund_months": {"score": 0, "status": "danger"},
                "housing_ratio": {"score": 0, "status": "danger"},
                "net_monthly_flow": {"value": -180.0},
            },
            "narrative": "Pulled back on dining and shopping — deficit dropped from $400 to $180. Still in the red. Housing at 38% is above the 30% limit. Emergency fund essentially zero.",
        },
    },
    {
        "saved_at": "2025-05",
        "version": "1",
        "inputs": {
            "income_main": 4200.0, "income_additional": 0.0,
            "expenses_rent": 1600.0, "expenses_groceries": 340.0,
            "expenses_transport": 280.0, "expenses_subscriptions": 100.0,
            "expenses_dining": 300.0, "expenses_shopping": 200.0, "expenses_other": 150.0,
            "savings_total": 900.0, "investments_total": 0.0,
            "debt_total": 13580.0, "debt_monthly": 420.0,
            "age": 28, "employment": "Employed",
            "has_health_insurance": False, "has_emergency_fund": "No", "contributing_401k": "No",
        },
        "outputs": {
            "overall_score": 33,
            "mirror_label": "At Risk",
            "metrics": {
                "savings_rate": 2.4, "debt_to_income": 10.0,
                "emergency_fund_months": 0.3, "housing_ratio": 38.1,
                "net_monthly_flow": 100.0, "debt_payment_missing": False,
            },
            "metric_scores": {
                "savings_rate": {"score": 10, "status": "warning"},
                "debt_to_income": {"score": 18, "status": "ok"},
                "emergency_fund_months": {"score": 0, "status": "danger"},
                "housing_ratio": {"score": 0, "status": "danger"},
                "net_monthly_flow": {"value": 100.0},
            },
            "narrative": "Finally in the black — $100 surplus this month. Savings rate turned positive. Emergency fund is still near zero. Keep cutting discretionary and stack savings before anything else.",
        },
    },
    {
        "saved_at": "2025-06",
        "version": "1",
        "inputs": {
            "income_main": 4200.0, "income_additional": 200.0,
            "expenses_rent": 1600.0, "expenses_groceries": 320.0,
            "expenses_transport": 260.0, "expenses_subscriptions": 90.0,
            "expenses_dining": 260.0, "expenses_shopping": 180.0, "expenses_other": 120.0,
            "savings_total": 1500.0, "investments_total": 0.0,
            "debt_total": 13160.0, "debt_monthly": 420.0,
            "age": 28, "employment": "Employed",
            "has_health_insurance": True, "has_emergency_fund": "No", "contributing_401k": "No",
        },
        "outputs": {
            "overall_score": 40,
            "mirror_label": "At Risk",
            "metrics": {
                "savings_rate": 7.8, "debt_to_income": 9.5,
                "emergency_fund_months": 0.5, "housing_ratio": 36.4,
                "net_monthly_flow": 350.0, "debt_payment_missing": False,
            },
            "metric_scores": {
                "savings_rate": {"score": 10, "status": "warning"},
                "debt_to_income": {"score": 18, "status": "ok"},
                "emergency_fund_months": {"score": 0, "status": "danger"},
                "housing_ratio": {"score": 0, "status": "danger"},
                "net_monthly_flow": {"value": 350.0},
            },
            "narrative": "Side income added $200 and you got health insurance sorted. Surplus up to $350. Emergency fund at 0.5 months — real progress but still dangerously thin. Target 1 month by August.",
        },
    },
    {
        "saved_at": "2025-07",
        "version": "1",
        "inputs": {
            "income_main": 4200.0, "income_additional": 400.0,
            "expenses_rent": 1600.0, "expenses_groceries": 310.0,
            "expenses_transport": 260.0, "expenses_subscriptions": 85.0,
            "expenses_dining": 230.0, "expenses_shopping": 150.0, "expenses_other": 100.0,
            "savings_total": 2400.0, "investments_total": 0.0,
            "debt_total": 12740.0, "debt_monthly": 420.0,
            "age": 28, "employment": "Employed",
            "has_health_insurance": True, "has_emergency_fund": "No", "contributing_401k": "No",
        },
        "outputs": {
            "overall_score": 47,
            "mirror_label": "At Risk",
            "metrics": {
                "savings_rate": 13.1, "debt_to_income": 9.1,
                "emergency_fund_months": 0.8, "housing_ratio": 34.5,
                "net_monthly_flow": 605.0, "debt_payment_missing": False,
            },
            "metric_scores": {
                "savings_rate": {"score": 10, "status": "warning"},
                "debt_to_income": {"score": 18, "status": "ok"},
                "emergency_fund_months": {"score": 10, "status": "warning"},
                "housing_ratio": {"score": 10, "status": "warning"},
                "net_monthly_flow": {"value": 605.0},
            },
            "narrative": "Side income growing, savings rate at 13%. Emergency fund crossed into warning zone — 0.8 months. Housing still above 30%. Savings at $2,400, keep the pace to hit 1 month by September.",
        },
    },
    {
        "saved_at": "2025-08",
        "version": "1",
        "inputs": {
            "income_main": 4200.0, "income_additional": 400.0,
            "expenses_rent": 1600.0, "expenses_groceries": 300.0,
            "expenses_transport": 250.0, "expenses_subscriptions": 80.0,
            "expenses_dining": 200.0, "expenses_shopping": 120.0, "expenses_other": 100.0,
            "savings_total": 3400.0, "investments_total": 0.0,
            "debt_total": 12320.0, "debt_monthly": 420.0,
            "age": 28, "employment": "Employed",
            "has_health_insurance": True, "has_emergency_fund": "Not sure", "contributing_401k": "No",
        },
        "outputs": {
            "overall_score": 52,
            "mirror_label": "Fair",
            "metrics": {
                "savings_rate": 17.0, "debt_to_income": 9.1,
                "emergency_fund_months": 1.1, "housing_ratio": 34.5,
                "net_monthly_flow": 750.0, "debt_payment_missing": False,
            },
            "metric_scores": {
                "savings_rate": {"score": 10, "status": "warning"},
                "debt_to_income": {"score": 18, "status": "ok"},
                "emergency_fund_months": {"score": 10, "status": "warning"},
                "housing_ratio": {"score": 10, "status": "warning"},
                "net_monthly_flow": {"value": 750.0},
            },
            "narrative": "Crossed into Fair for the first time. Emergency fund hit 1 month. Savings rate at 17%, close to the 20% target. Housing still above 30% — that won't change until rent does.",
        },
    },
    {
        "saved_at": "2025-09",
        "version": "1",
        "inputs": {
            "income_main": 4500.0, "income_additional": 400.0,
            "expenses_rent": 1600.0, "expenses_groceries": 300.0,
            "expenses_transport": 250.0, "expenses_subscriptions": 80.0,
            "expenses_dining": 190.0, "expenses_shopping": 100.0, "expenses_other": 100.0,
            "savings_total": 4600.0, "investments_total": 0.0,
            "debt_total": 11900.0, "debt_monthly": 420.0,
            "age": 28, "employment": "Employed",
            "has_health_insurance": True, "has_emergency_fund": "Not sure", "contributing_401k": "No",
        },
        "outputs": {
            "overall_score": 58,
            "mirror_label": "Fair",
            "metrics": {
                "savings_rate": 19.2, "debt_to_income": 8.6,
                "emergency_fund_months": 1.5, "housing_ratio": 32.8,
                "net_monthly_flow": 980.0, "debt_payment_missing": False,
            },
            "metric_scores": {
                "savings_rate": {"score": 10, "status": "warning"},
                "debt_to_income": {"score": 18, "status": "ok"},
                "emergency_fund_months": {"score": 10, "status": "warning"},
                "housing_ratio": {"score": 10, "status": "warning"},
                "net_monthly_flow": {"value": 980.0},
            },
            "narrative": "Small raise kicks in — income up to $4,900. Savings rate almost at 20%, emergency fund at 1.5 months. Debt slowly coming down. One more $300 cut or income boost and the savings rate flips to green.",
        },
    },
    {
        "saved_at": "2025-10",
        "version": "1",
        "inputs": {
            "income_main": 4500.0, "income_additional": 500.0,
            "expenses_rent": 1600.0, "expenses_groceries": 290.0,
            "expenses_transport": 250.0, "expenses_subscriptions": 80.0,
            "expenses_dining": 180.0, "expenses_shopping": 90.0, "expenses_other": 100.0,
            "savings_total": 6000.0, "investments_total": 0.0,
            "debt_total": 11480.0, "debt_monthly": 420.0,
            "age": 28, "employment": "Employed",
            "has_health_insurance": True, "has_emergency_fund": "Yes", "contributing_401k": "No",
        },
        "outputs": {
            "overall_score": 63,
            "mirror_label": "Fair",
            "metrics": {
                "savings_rate": 21.0, "debt_to_income": 8.4,
                "emergency_fund_months": 1.9, "housing_ratio": 32.0,
                "net_monthly_flow": 1110.0, "debt_payment_missing": False,
            },
            "metric_scores": {
                "savings_rate": {"score": 25, "status": "good"},
                "debt_to_income": {"score": 18, "status": "ok"},
                "emergency_fund_months": {"score": 10, "status": "warning"},
                "housing_ratio": {"score": 10, "status": "warning"},
                "net_monthly_flow": {"value": 1110.0},
            },
            "narrative": "Savings rate crossed 20% — now green. Side income at $500. Emergency fund at 1.9 months, closing in on the 3-month target. Score at 63, climbing steadily since March.",
        },
    },
    {
        "saved_at": "2025-11",
        "version": "1",
        "inputs": {
            "income_main": 4500.0, "income_additional": 500.0,
            "expenses_rent": 1600.0, "expenses_groceries": 290.0,
            "expenses_transport": 250.0, "expenses_subscriptions": 80.0,
            "expenses_dining": 175.0, "expenses_shopping": 90.0, "expenses_other": 100.0,
            "savings_total": 7400.0, "investments_total": 200.0,
            "debt_total": 11060.0, "debt_monthly": 420.0,
            "age": 28, "employment": "Employed",
            "has_health_insurance": True, "has_emergency_fund": "Yes", "contributing_401k": "No",
        },
        "outputs": {
            "overall_score": 65,
            "mirror_label": "Fair",
            "metrics": {
                "savings_rate": 21.4, "debt_to_income": 8.4,
                "emergency_fund_months": 2.3, "housing_ratio": 32.0,
                "net_monthly_flow": 1115.0, "debt_payment_missing": False,
            },
            "metric_scores": {
                "savings_rate": {"score": 25, "status": "good"},
                "debt_to_income": {"score": 18, "status": "ok"},
                "emergency_fund_months": {"score": 10, "status": "warning"},
                "housing_ratio": {"score": 10, "status": "warning"},
                "net_monthly_flow": {"value": 1115.0},
            },
            "narrative": "Started investing $200/month. Emergency fund at 2.3 months — within reach of the 3-month milestone. Score holding steady. One more month at this pace should cross the 3-month mark.",
        },
    },
    {
        "saved_at": "2025-12",
        "version": "1",
        "inputs": {
            "income_main": 4500.0, "income_additional": 500.0,
            "expenses_rent": 1600.0, "expenses_groceries": 290.0,
            "expenses_transport": 250.0, "expenses_subscriptions": 80.0,
            "expenses_dining": 175.0, "expenses_shopping": 200.0, "expenses_other": 150.0,
            "savings_total": 8400.0, "investments_total": 400.0,
            "debt_total": 10640.0, "debt_monthly": 420.0,
            "age": 28, "employment": "Employed",
            "has_health_insurance": True, "has_emergency_fund": "Yes", "contributing_401k": "No",
        },
        "outputs": {
            "overall_score": 60,
            "mirror_label": "Fair",
            "metrics": {
                "savings_rate": 17.6, "debt_to_income": 8.4,
                "emergency_fund_months": 2.7, "housing_ratio": 32.0,
                "net_monthly_flow": 755.0, "debt_payment_missing": False,
            },
            "metric_scores": {
                "savings_rate": {"score": 10, "status": "warning"},
                "debt_to_income": {"score": 18, "status": "ok"},
                "emergency_fund_months": {"score": 10, "status": "warning"},
                "housing_ratio": {"score": 10, "status": "warning"},
                "net_monthly_flow": {"value": 755.0},
            },
            "narrative": "Holiday spending bumped dining and shopping — savings rate dipped to 17.6%. Emergency fund at 2.7 months. Score dropped slightly to 60. Expect it to recover in January when spending normalises.",
        },
    },
    {
        "saved_at": "2026-01",
        "version": "1",
        "inputs": {
            "income_main": 4500.0, "income_additional": 500.0,
            "expenses_rent": 1600.0, "expenses_groceries": 290.0,
            "expenses_transport": 250.0, "expenses_subscriptions": 80.0,
            "expenses_dining": 175.0, "expenses_shopping": 90.0, "expenses_other": 100.0,
            "savings_total": 9800.0, "investments_total": 600.0,
            "debt_total": 10220.0, "debt_monthly": 420.0,
            "age": 28, "employment": "Employed",
            "has_health_insurance": True, "has_emergency_fund": "Yes", "contributing_401k": "No",
        },
        "outputs": {
            "overall_score": 68,
            "mirror_label": "Fair",
            "metrics": {
                "savings_rate": 21.4, "debt_to_income": 8.4,
                "emergency_fund_months": 3.1, "housing_ratio": 32.0,
                "net_monthly_flow": 1115.0, "debt_payment_missing": False,
            },
            "metric_scores": {
                "savings_rate": {"score": 25, "status": "good"},
                "debt_to_income": {"score": 18, "status": "ok"},
                "emergency_fund_months": {"score": 18, "status": "ok"},
                "housing_ratio": {"score": 10, "status": "warning"},
                "net_monthly_flow": {"value": 1115.0},
            },
            "narrative": "Emergency fund crossed 3 months — now in the OK zone. Savings rate back to green at 21.4%. Investments at $600. Score at 68, the highest yet. Housing ratio is the last big lever — if rent drops or income rises, score could hit 80+.",
        },
    },
    {
        "saved_at": "2026-02",
        "version": "1",
        "inputs": {
            "income_main": 4500.0, "income_additional": 500.0,
            "expenses_rent": 1600.0, "expenses_groceries": 290.0,
            "expenses_transport": 250.0, "expenses_subscriptions": 80.0,
            "expenses_dining": 170.0, "expenses_shopping": 90.0, "expenses_other": 100.0,
            "savings_total": 11000.0, "investments_total": 800.0,
            "debt_total": 9800.0, "debt_monthly": 420.0,
            "age": 28, "employment": "Employed",
            "has_health_insurance": True, "has_emergency_fund": "Yes", "contributing_401k": "Yes",
        },
        "outputs": {
            "overall_score": 71,
            "mirror_label": "Good",
            "metrics": {
                "savings_rate": 21.6, "debt_to_income": 8.4,
                "emergency_fund_months": 3.5, "housing_ratio": 32.0,
                "net_monthly_flow": 1120.0, "debt_payment_missing": False,
            },
            "metric_scores": {
                "savings_rate": {"score": 25, "status": "good"},
                "debt_to_income": {"score": 18, "status": "ok"},
                "emergency_fund_months": {"score": 18, "status": "ok"},
                "housing_ratio": {"score": 10, "status": "warning"},
                "net_monthly_flow": {"value": 1120.0},
            },
            "narrative": "First month in the Good band. Started 401k contributions. Emergency fund at 3.5 months. Debt under $10k for the first time. Savings and investments growing steadily. Housing is the only remaining red flag.",
        },
    },
    {
        "saved_at": "2026-03",
        "version": "1",
        "inputs": {
            "income_main": 4500.0, "income_additional": 500.0,
            "expenses_rent": 1600.0, "expenses_groceries": 285.0,
            "expenses_transport": 250.0, "expenses_subscriptions": 80.0,
            "expenses_dining": 165.0, "expenses_shopping": 85.0, "expenses_other": 100.0,
            "savings_total": 12200.0, "investments_total": 1100.0,
            "debt_total": 9380.0, "debt_monthly": 420.0,
            "age": 28, "employment": "Employed",
            "has_health_insurance": True, "has_emergency_fund": "Yes", "contributing_401k": "Yes",
        },
        "outputs": {
            "overall_score": 73,
            "mirror_label": "Good",
            "metrics": {
                "savings_rate": 21.8, "debt_to_income": 8.4,
                "emergency_fund_months": 3.9, "housing_ratio": 32.0,
                "net_monthly_flow": 1135.0, "debt_payment_missing": False,
            },
            "metric_scores": {
                "savings_rate": {"score": 25, "status": "good"},
                "debt_to_income": {"score": 18, "status": "ok"},
                "emergency_fund_months": {"score": 18, "status": "ok"},
                "housing_ratio": {"score": 10, "status": "warning"},
                "net_monthly_flow": {"value": 1135.0},
            },
            "narrative": "Score up to 73. Investments at $1,100. Emergency fund nearly at 4 months. Debt down to $9,380 — paid off over $4,600 since March 2025. Housing is the ceiling until something changes on rent or income.",
        },
    },
    {
        "saved_at": "2026-04",
        "version": "1",
        "inputs": {
            "income_main": 5200.0, "income_additional": 500.0,
            "expenses_rent": 1600.0, "expenses_groceries": 285.0,
            "expenses_transport": 250.0, "expenses_subscriptions": 80.0,
            "expenses_dining": 165.0, "expenses_shopping": 85.0, "expenses_other": 100.0,
            "savings_total": 13600.0, "investments_total": 1600.0,
            "debt_total": 8960.0, "debt_monthly": 420.0,
            "age": 28, "employment": "Employed",
            "has_health_insurance": True, "has_emergency_fund": "Yes", "contributing_401k": "Yes",
        },
        "outputs": {
            "overall_score": 80,
            "mirror_label": "Good",
            "metrics": {
                "savings_rate": 26.5, "debt_to_income": 7.2,
                "emergency_fund_months": 4.6, "housing_ratio": 27.6,
                "net_monthly_flow": 1635.0, "debt_payment_missing": False,
            },
            "metric_scores": {
                "savings_rate": {"score": 25, "status": "good"},
                "debt_to_income": {"score": 18, "status": "ok"},
                "emergency_fund_months": {"score": 18, "status": "ok"},
                "housing_ratio": {"score": 18, "status": "ok"},
                "net_monthly_flow": {"value": 1635.0},
            },
            "narrative": "Raise to $5,200 — housing ratio finally dropped below 30%. Score hit 80. All four metrics now green or ok. 13 months ago you were $400 in the red with an 18 score. That's a real turnaround.",
        },
    },
]


def main():
    output_path = os.path.join(os.path.dirname(__file__), "fake_data.vit")
    json_str    = json.dumps(SNAPSHOTS, indent=2)
    encrypted   = _cipher.encrypt(json_str.encode("utf-8"))

    with open(output_path, "wb") as f:
        f.write(encrypted)

    print(f"Generated: {output_path}")
    print(f"{len(SNAPSHOTS)} snapshots — {SNAPSHOTS[0]['saved_at']} to {SNAPSHOTS[-1]['saved_at']}")
    print(f"Score arc: {' → '.join(str(s['outputs']['overall_score']) for s in SNAPSHOTS)}")
    print(f"\nUpload this file on the form page to test Progress Charts.")


if __name__ == "__main__":
    main()
