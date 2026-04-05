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


def render_whatif_simulator(current_score: int, current_metric_scores: dict):
    st.caption(
        "Adjust any value to see how it would affect your score. "
        "Your original data is not changed."
    )

    # Seed on first visit, or when reset was requested on the previous rerun
    # Both cases run BEFORE sliders are instantiated — avoids StreamlitAPIException
    if st.session_state.pop("sim_reset", False) or "sim_income" not in st.session_state:
        _seed_sim_values()

    col1, col2 = st.columns(2)

    with col1:
        st.slider(
            "Total monthly income",
            min_value=0,
            max_value=int(max((st.session_state.get("income_main", 0.0) + st.session_state.get("income_additional", 0.0)) * 2, 10000)),
            step=100,
            key="sim_income",
            help="Drag up to simulate a raise or side income"
        )
        st.slider(
            "Dining out / Food delivery",
            min_value=0,
            max_value=int(max(st.session_state.get("expenses_dining", 0.0) * 3, 600)),
            step=25,
            key="sim_dining",
        )
        st.slider(
            "Shopping / Personal",
            min_value=0,
            max_value=int(max(st.session_state.get("expenses_shopping", 0.0) * 3, 600)),
            step=25,
            key="sim_shopping",
        )

    with col2:
        st.slider(
            "Subscriptions",
            min_value=0,
            max_value=int(max(st.session_state.get("expenses_subscriptions", 0.0) * 3, 300)),
            step=5,
            key="sim_subscriptions",
        )
        st.slider(
            "Monthly debt payment",
            min_value=0,
            max_value=int(max(st.session_state.get("debt_monthly", 0.0) * 3, 1500)),
            step=25,
            key="sim_debt_payment",
        )

    if st.button("Reset to my current values", type="secondary"):
        st.session_state.sim_reset = True
        st.rerun()

    # Build simulated state — only override the slider fields, keep everything else real
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

    score_delta = sim_score - current_score
    cur_flow    = current_metric_scores["net_monthly_flow"]["value"]
    sim_flow    = sim_metrics["net_monthly_flow"]
    flow_delta  = sim_flow - cur_flow

    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Current Score", f"{current_score} / 100")
    with col2:
        st.metric(
            "Simulated Score",
            f"{sim_score} / 100",
            delta=f"{score_delta:+d} pts",
        )
    with col3:
        st.metric(
            "Cash left / month",
            f"${sim_flow:,.0f}",
            delta=f"${flow_delta:+,.0f}",
        )

    # Show raw metric deltas so users see changes even within a scoring tier
    cur_metrics = calculate_metrics(dict(st.session_state))
    st.markdown("##### How your metrics shift")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(
            "Savings Rate",
            f"{sim_metrics['savings_rate']}%",
            delta=f"{sim_metrics['savings_rate'] - cur_metrics['savings_rate']:+.1f}%"
        )
    with m2:
        st.metric(
            "Debt-to-Income",
            f"{sim_metrics['debt_to_income']}%",
            delta=f"{sim_metrics['debt_to_income'] - cur_metrics['debt_to_income']:+.1f}%",
            delta_color="inverse"
        )
    with m3:
        st.metric(
            "Emergency Fund",
            f"{sim_metrics['emergency_fund_months']} mo",
            delta=f"{sim_metrics['emergency_fund_months'] - cur_metrics['emergency_fund_months']:+.1f} mo"
        )
    with m4:
        st.metric(
            "Housing Ratio",
            f"{sim_metrics['housing_ratio']}%",
            delta=f"{sim_metrics['housing_ratio'] - cur_metrics['housing_ratio']:+.1f}%",
            delta_color="inverse"
        )
