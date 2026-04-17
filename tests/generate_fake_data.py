#!/usr/bin/env python3
"""
Generates a fake 6-month .vit file for testing the Progress Charts tab.
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
        "saved_at": "2025-11",
        "version": "1",
        "inputs": {
            "income_main": 4500.0, "income_additional": 0.0,
            "expenses_rent": 1600.0, "expenses_groceries": 350.0,
            "expenses_transport": 280.0, "expenses_subscriptions": 120.0,
            "expenses_dining": 480.0, "expenses_shopping": 320.0, "expenses_other": 150.0,
            "savings_total": 800.0, "investments_total": 0.0,
            "debt_total": 12000.0, "debt_monthly": 350.0,
            "age": 28, "employment": "Employed",
            "has_health_insurance": True, "has_emergency_fund": "No", "contributing_401k": "No",
        },
        "outputs": {
            "overall_score": 28,
            "mirror_label": "Critical",
            "metrics": {
                "savings_rate": -4.0, "debt_to_income": 7.8,
                "emergency_fund_months": 0.3, "housing_ratio": 35.6,
                "net_monthly_flow": -180.0, "debt_payment_missing": False,
            },
            "metric_scores": {
                "savings_rate": {"score": 0, "status": "danger"},
                "debt_to_income": {"score": 18, "status": "ok"},
                "emergency_fund_months": {"score": 0, "status": "danger"},
                "housing_ratio": {"score": 10, "status": "warning"},
                "net_monthly_flow": {"value": -180.0},
            },
            "narrative": "You're spending more than you earn — $180 in the red this month. Dining and shopping are $800 combined and your savings are nearly zero. One unexpected bill could put you in serious trouble.",
        },
    },
    {
        "saved_at": "2025-12",
        "version": "1",
        "inputs": {
            "income_main": 4500.0, "income_additional": 0.0,
            "expenses_rent": 1600.0, "expenses_groceries": 320.0,
            "expenses_transport": 280.0, "expenses_subscriptions": 100.0,
            "expenses_dining": 350.0, "expenses_shopping": 200.0, "expenses_other": 150.0,
            "savings_total": 1200.0, "investments_total": 0.0,
            "debt_total": 12000.0, "debt_monthly": 350.0,
            "age": 28, "employment": "Employed",
            "has_health_insurance": True, "has_emergency_fund": "No", "contributing_401k": "No",
        },
        "outputs": {
            "overall_score": 38,
            "mirror_label": "At Risk",
            "metrics": {
                "savings_rate": 2.2, "debt_to_income": 7.8,
                "emergency_fund_months": 0.4, "housing_ratio": 35.6,
                "net_monthly_flow": 100.0, "debt_payment_missing": False,
            },
            "metric_scores": {
                "savings_rate": {"score": 10, "status": "warning"},
                "debt_to_income": {"score": 18, "status": "ok"},
                "emergency_fund_months": {"score": 0, "status": "danger"},
                "housing_ratio": {"score": 10, "status": "warning"},
                "net_monthly_flow": {"value": 100.0},
            },
            "narrative": "You cut dining and shopping — now $100 positive. Emergency fund is still dangerously low at 0.4 months. Keep cutting discretionary spend and move every spare dollar to savings.",
        },
    },
    {
        "saved_at": "2026-01",
        "version": "1",
        "inputs": {
            "income_main": 4500.0, "income_additional": 500.0,
            "expenses_rent": 1600.0, "expenses_groceries": 300.0,
            "expenses_transport": 250.0, "expenses_subscriptions": 80.0,
            "expenses_dining": 250.0, "expenses_shopping": 150.0, "expenses_other": 100.0,
            "savings_total": 2100.0, "investments_total": 0.0,
            "debt_total": 12000.0, "debt_monthly": 350.0,
            "age": 28, "employment": "Employed",
            "has_health_insurance": True, "has_emergency_fund": "No", "contributing_401k": "No",
        },
        "outputs": {
            "overall_score": 48,
            "mirror_label": "At Risk",
            "metrics": {
                "savings_rate": 14.8, "debt_to_income": 7.0,
                "emergency_fund_months": 0.7, "housing_ratio": 32.0,
                "net_monthly_flow": 720.0, "debt_payment_missing": False,
            },
            "metric_scores": {
                "savings_rate": {"score": 10, "status": "warning"},
                "debt_to_income": {"score": 18, "status": "ok"},
                "emergency_fund_months": {"score": 10, "status": "warning"},
                "housing_ratio": {"score": 10, "status": "warning"},
                "net_monthly_flow": {"value": 720.0},
            },
            "narrative": "Side income added $500. Savings rate at 14.8% and climbing. Emergency fund still under 1 month — that $720 cash should go straight to savings before anything else.",
        },
    },
    {
        "saved_at": "2026-02",
        "version": "1",
        "inputs": {
            "income_main": 4500.0, "income_additional": 500.0,
            "expenses_rent": 1600.0, "expenses_groceries": 280.0,
            "expenses_transport": 250.0, "expenses_subscriptions": 75.0,
            "expenses_dining": 200.0, "expenses_shopping": 100.0, "expenses_other": 100.0,
            "savings_total": 3800.0, "investments_total": 0.0,
            "debt_total": 11650.0, "debt_monthly": 350.0,
            "age": 28, "employment": "Employed",
            "has_health_insurance": True, "has_emergency_fund": "Not sure", "contributing_401k": "No",
        },
        "outputs": {
            "overall_score": 58,
            "mirror_label": "Fair",
            "metrics": {
                "savings_rate": 19.8, "debt_to_income": 7.0,
                "emergency_fund_months": 1.2, "housing_ratio": 32.0,
                "net_monthly_flow": 1045.0, "debt_payment_missing": False,
            },
            "metric_scores": {
                "savings_rate": {"score": 10, "status": "warning"},
                "debt_to_income": {"score": 18, "status": "ok"},
                "emergency_fund_months": {"score": 10, "status": "warning"},
                "housing_ratio": {"score": 10, "status": "warning"},
                "net_monthly_flow": {"value": 1045.0},
            },
            "narrative": "Savings rate nearly at 20% — one more push gets you there. Emergency fund at 1.2 months, up from 0.3 in November. Move $500 from this month's cash into savings to cross the 3-month mark faster.",
        },
    },
    {
        "saved_at": "2026-03",
        "version": "1",
        "inputs": {
            "income_main": 4500.0, "income_additional": 500.0,
            "expenses_rent": 1600.0, "expenses_groceries": 280.0,
            "expenses_transport": 250.0, "expenses_subscriptions": 75.0,
            "expenses_dining": 180.0, "expenses_shopping": 80.0, "expenses_other": 100.0,
            "savings_total": 5600.0, "investments_total": 500.0,
            "debt_total": 11300.0, "debt_monthly": 350.0,
            "age": 28, "employment": "Employed",
            "has_health_insurance": True, "has_emergency_fund": "Yes", "contributing_401k": "No",
        },
        "outputs": {
            "overall_score": 68,
            "mirror_label": "Fair",
            "metrics": {
                "savings_rate": 22.4, "debt_to_income": 7.0,
                "emergency_fund_months": 1.8, "housing_ratio": 32.0,
                "net_monthly_flow": 1135.0, "debt_payment_missing": False,
            },
            "metric_scores": {
                "savings_rate": {"score": 25, "status": "good"},
                "debt_to_income": {"score": 18, "status": "ok"},
                "emergency_fund_months": {"score": 10, "status": "warning"},
                "housing_ratio": {"score": 10, "status": "warning"},
                "net_monthly_flow": {"value": 1135.0},
            },
            "narrative": "Savings rate crossed 20% — that's real progress. Started investing $500. Emergency fund at 1.8 months, still short of the 3-month target. Keep the current pace and you'll hit 3 months by June.",
        },
    },
    {
        "saved_at": "2026-04",
        "version": "1",
        "inputs": {
            "income_main": 5200.0, "income_additional": 500.0,
            "expenses_rent": 1600.0, "expenses_groceries": 280.0,
            "expenses_transport": 250.0, "expenses_subscriptions": 75.0,
            "expenses_dining": 180.0, "expenses_shopping": 80.0, "expenses_other": 100.0,
            "savings_total": 7200.0, "investments_total": 1000.0,
            "debt_total": 10950.0, "debt_monthly": 350.0,
            "age": 28, "employment": "Employed",
            "has_health_insurance": True, "has_emergency_fund": "Yes", "contributing_401k": "Yes",
        },
        "outputs": {
            "overall_score": 78,
            "mirror_label": "Good",
            "metrics": {
                "savings_rate": 27.6, "debt_to_income": 6.1,
                "emergency_fund_months": 2.8, "housing_ratio": 27.6,
                "net_monthly_flow": 1585.0, "debt_payment_missing": False,
            },
            "metric_scores": {
                "savings_rate": {"score": 25, "status": "good"},
                "debt_to_income": {"score": 18, "status": "ok"},
                "emergency_fund_months": {"score": 10, "status": "warning"},
                "housing_ratio": {"score": 18, "status": "ok"},
                "net_monthly_flow": {"value": 1585.0},
            },
            "narrative": "Raise kicked in — income up to $5,700. Score jumped from 28 to 78 in 5 months. Emergency fund at 2.8 months, almost there. Move $400 from this month's cash to savings to hit the 3-month mark.",
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
