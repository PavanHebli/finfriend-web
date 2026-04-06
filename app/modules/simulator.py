import streamlit as st
from modules.health import calculate_metrics, score_metrics, calculate_overall_score


def _seed_sim_values():
    """Seeds simulator sliders from current form values. Called on first visit."""
    income = st.session_state.get("income_main", 0.0) + st.session_state.get("income_additional", 0.0)
    st.session_state.sim_income        = int(income)
    st.session_state.sim_dining        = int(st.session_state.get("expenses_dining", 0.0))
    st.session_state.sim_shopping      = int(st.session_state.get("expenses_shopping", 0.0))
    st.session_state.sim_subscriptions = int(st.session_state.get("expenses_subscriptions", 0.0))
    st.session_state.sim_debt_payment  = int(st.session_state.get("debt_monthly", 0.0))


def _metric_delta_color(delta: float, inverse: bool = False) -> str:
    """
    Returns st.metric delta_color.
    - When delta is 0: always "off" (no color, no arrow — avoids misleading red/green on unchanged metrics)
    - inverse=True: positive delta is bad (red), negative is good (green) — used for DTI and housing ratio
    """
    if abs(delta) < 0.01:
        return "off"
    return "inverse" if inverse else "normal"


def render_whatif_simulator(current_score: int, current_metric_scores: dict):
    """
    Interactive simulator — adjust income and discretionary expenses to see
    how changes would affect the health score and individual metrics.
    """
    st.caption(
        "Adjust the sliders to explore how changes would affect your score. "
        "Your original data is not changed."
    )

    # Seed on first visit, or when reset was requested on the previous rerun.
    # Must run BEFORE sliders are instantiated — avoids StreamlitAPIException.
    if st.session_state.pop("sim_reset", False) or "sim_income" not in st.session_state:
        _seed_sim_values()

    # --- Sliders ---
    col1, col2 = st.columns(2)

    with col1:
        st.slider(
            "Total monthly income",
            min_value=0,
            max_value=int(max((st.session_state.get("income_main", 0.0) + st.session_state.get("income_additional", 0.0)) * 2, 10000)),
            step=100,
            key="sim_income",
            help="Affects all 4 metrics — savings rate, debt-to-income, emergency fund, and housing ratio all divide by income."
        )
        st.slider(
            "Dining out / Food delivery",
            min_value=0,
            max_value=int(max(st.session_state.get("expenses_dining", 0.0) * 3, 600)),
            step=25,
            key="sim_dining",
            help="Affects savings rate and emergency fund months. Does not affect debt-to-income or housing ratio."
        )
        st.slider(
            "Shopping / Personal",
            min_value=0,
            max_value=int(max(st.session_state.get("expenses_shopping", 0.0) * 3, 600)),
            step=25,
            key="sim_shopping",
            help="Affects savings rate and emergency fund months. Does not affect debt-to-income or housing ratio."
        )

    with col2:
        st.slider(
            "Subscriptions",
            min_value=0,
            max_value=int(max(st.session_state.get("expenses_subscriptions", 0.0) * 3, 300)),
            step=5,
            key="sim_subscriptions",
            help="Affects savings rate and emergency fund months. Does not affect debt-to-income or housing ratio."
        )
        st.slider(
            "Monthly debt payment",
            min_value=0,
            max_value=int(max(st.session_state.get("debt_monthly", 0.0) * 3, 1500)),
            step=25,
            key="sim_debt_payment",
            help="Affects debt-to-income ratio only. Note: DTI is calculated from your monthly payment amount, not your total debt balance."
        )

    st.caption(
        "Housing ratio is not a slider — rent/mortgage is fixed. "
        "To see housing ratio change, adjust the income slider."
    )

    if st.button("Reset to my current values", type="secondary"):
        st.session_state.sim_reset = True
        st.rerun()

    # --- Build simulated state ---
    sim_state = dict(st.session_state)
    sim_state["income_main"]            = float(st.session_state.sim_income)
    sim_state["income_additional"]      = 0.0
    sim_state["expenses_dining"]        = float(st.session_state.sim_dining)
    sim_state["expenses_shopping"]      = float(st.session_state.sim_shopping)
    sim_state["expenses_subscriptions"] = float(st.session_state.sim_subscriptions)
    sim_state["debt_monthly"]           = float(st.session_state.sim_debt_payment)

    sim_metrics       = calculate_metrics(sim_state)
    sim_metric_scores = score_metrics(sim_metrics)
    sim_score         = calculate_overall_score(sim_metric_scores)

    cur_metrics = calculate_metrics(dict(st.session_state))

    score_delta = sim_score - current_score
    cur_flow    = current_metric_scores["net_monthly_flow"]["value"]
    sim_flow    = sim_metrics["net_monthly_flow"]
    flow_delta  = sim_flow - cur_flow

    st.markdown("---")

    # --- Score + cash summary ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Current Score", f"{current_score} / 100")
    with col2:
        st.metric(
            "Simulated Score",
            f"{sim_score} / 100",
            delta=f"{score_delta:+d} pts" if score_delta != 0 else None,
        )
    with col3:
        st.metric(
            "Cash left / month",
            f"${sim_flow:,.0f}",
            delta=f"${flow_delta:+,.0f}" if abs(flow_delta) >= 1 else None,
        )

    # --- Raw metric deltas ---
    st.markdown("##### How your metrics shift")
    st.caption(
        "Metrics that are not affected by the sliders you moved will show no change. "
        "Green = improving · Red = worsening · Grey = unchanged."
    )

    d_sr  = round(sim_metrics["savings_rate"]          - cur_metrics["savings_rate"],          1)
    d_dti = round(sim_metrics["debt_to_income"]        - cur_metrics["debt_to_income"],         1)
    d_ef  = round(sim_metrics["emergency_fund_months"] - cur_metrics["emergency_fund_months"],  1)
    d_hr  = round(sim_metrics["housing_ratio"]         - cur_metrics["housing_ratio"],          1)

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(
            "Savings Rate",
            f"{sim_metrics['savings_rate']}%",
            delta=f"{d_sr:+.1f}%" if d_sr != 0 else None,
            delta_color=_metric_delta_color(d_sr, inverse=False),
            help="% of income left after expenses. Target: ≥20%. Income ↑ = better · Dining/Shopping/Subscriptions ↑ = worse."
        )
    with m2:
        st.metric(
            "Debt-to-Income",
            f"{sim_metrics['debt_to_income']}%",
            delta=f"{d_dti:+.1f}%" if d_dti != 0 else None,
            delta_color=_metric_delta_color(d_dti, inverse=True),
            help="Monthly debt payments as % of take-home income. Target: <20% (danger: >43%). Uses net income — stricter than lender benchmarks. Income ↑ = better · Debt payment ↑ = worse."
        )
    with m3:
        st.metric(
            "Emergency Fund",
            f"{sim_metrics['emergency_fund_months']} mo",
            delta=f"{d_ef:+.1f} mo" if d_ef != 0 else None,
            delta_color=_metric_delta_color(d_ef, inverse=False),
            help="Months your savings would last if income stopped. Target: 3–6 mo. Dining/Shopping/Subscriptions ↓ = savings stretch further. Change savings balance in the form."
        )
    with m4:
        st.metric(
            "Housing Ratio",
            f"{sim_metrics['housing_ratio']}%",
            delta=f"{d_hr:+.1f}%" if d_hr != 0 else None,
            delta_color=_metric_delta_color(d_hr, inverse=True),
            help="Rent as % of income. Target: ≤30%. Income slider only — rent is fixed in the simulator."
        )
