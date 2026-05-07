import random
import streamlit as st
from modules.snapshot import render_api_config, render_income_section, render_expenses_section, render_position_section, render_context_section
from modules.storage import load_vit, get_latest, populate_state_from_snapshot
from modules.analytics import log_snapshot_loaded


def fill_sample_data():
    income = float(random.choice([3500, 4500, 6000, 8000, 10000]))
    st.session_state.income_main = income
    st.session_state.income_additional = float(random.choice([0, 0, 500, 1000]))
    st.session_state.expenses_rent = float(random.choice([1200, 1500, 1800, 2000]))
    st.session_state.expenses_groceries = float(random.choice([0, 200, 300, 400]))
    st.session_state.expenses_transport = float(random.choice([0, 150, 250, 400]))
    st.session_state.expenses_subscriptions = float(random.choice([0, 0, 80, 150]))
    st.session_state.expenses_dining = float(random.choice([0, 200, 350, 500]))
    st.session_state.expenses_shopping = float(random.choice([0, 0, 150, 300]))
    st.session_state.expenses_other = float(random.choice([0, 100, 200]))
    st.session_state.savings_total = float(random.choice([0, 500, 2000, 8000]))
    st.session_state.investments_total = float(random.choice([0, 0, 5000, 20000]))
    st.session_state.debt_total = float(random.choice([0, 0, 5000, 15000, 30000]))
    st.session_state.debt_monthly = float(random.choice([0, 0, 200, 400, 600]))
    st.session_state.age = random.randint(24, 45)
    st.session_state.employment = random.choice(["Employed", "Employed", "Self-employed", "Job hunting"])
    st.session_state.has_health_insurance = random.choice([True, True, False])
    st.session_state.has_emergency_fund = random.choice(["Yes", "No", "Not sure"])
    st.session_state.contributing_401k = random.choice(["Yes", "No", "No", "Not sure"])


def clear_all_fields():
    keys_to_reset = {
        "income_main": 0.0, "income_additional": 0.0,
        "expenses_rent": 0.0, "expenses_groceries": 0.0, "expenses_transport": 0.0,
        "expenses_subscriptions": 0.0, "expenses_dining": 0.0, "expenses_shopping": 0.0,
        "expenses_other": 0.0, "savings_total": 0.0, "investments_total": 0.0,
        "debt_total": 0.0, "debt_monthly": 0.0,
        "age": 25, "employment": "Employed", "has_health_insurance": False,
        "has_emergency_fund": "Not sure", "contributing_401k": "No",
    }
    for key, value in keys_to_reset.items():
        st.session_state[key] = value
    st.session_state.sample_input_active = False


def render_form_panel():
    col1, col2 = st.columns([6, 1])
    with col1:
        st.title("🩺 Vitals")
        st.markdown("### Your Personal Financial Health Checkup")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            "<a href='/feedback' target='_self' style='"
            "font-size:1rem; padding:6px 14px; border:1.5px solid #ccc; border-radius:6px;"
            "text-decoration:none; color:inherit;'>💬 Feedback</a>",
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # --- Sample data banner — always visible ---
    col_txt, col_try, col_clear = st.columns([4, 1.2, 1])
    with col_txt:
        st.markdown(
            "<p style='font-size:1.05rem; margin:0; padding-top:6px;'>"
            "🚀 <b>First time here?</b> No API key needed — try the app instantly with sample data.</p>",
            unsafe_allow_html=True,
        )
    with col_try:
        if st.button("Try sample data →", type="primary", use_container_width=True):
            st.session_state.sample_input_active = True
            fill_sample_data()
            st.rerun()
    with col_clear:
        if st.button("Clear all", type="secondary", use_container_width=True):
            clear_all_fields()

    if st.session_state.get("sample_input_active", False):
        st.success("✅ Form pre-filled with sample data — scroll down to review and click **Generate my report**.")

    st.markdown("---")

    # --- Import previous snapshot ---
    uploaded = st.file_uploader(
        "Import previous data (my_vitals.vit)",
        type=["vit"],
        key=f"snapshot_upload_{st.session_state.get('file_uploader_key', 0)}",
        label_visibility="visible",
    )

    if uploaded and "snapshot_preview_data" not in st.session_state:
        try:
            st.session_state.snapshot_preview_data = load_vit(uploaded)
        except ValueError as e:
            st.error(str(e))

    if "snapshot_preview_data" in st.session_state:
        data     = st.session_state.snapshot_preview_data
        latest   = get_latest(data)
        n        = len(data)
        score    = latest["outputs"]["overall_score"]
        label    = latest["outputs"]["mirror_label"]
        date     = latest["saved_at"]

        st.info(
            f"📁 Found **{n} snapshot{'s' if n > 1 else ''}** — most recent: **{date}**  \n"
            f"Score: **{score}/100 ({label})**  \n"
            "This will pre-fill the form with your previous data. Review and update any values that have changed."
        )

        col_load, col_cancel, _ = st.columns([1, 1, 4])
        with col_load:
            if st.button("Load into form", type="primary"):
                populate_state_from_snapshot(latest, st.session_state)
                st.session_state.previous_snapshot  = latest
                st.session_state.loaded_snapshots   = data
                log_snapshot_loaded()
                st.session_state.pop("narrative_text", None)
                st.session_state.file_uploader_key  = st.session_state.get("file_uploader_key", 0) + 1
                del st.session_state.snapshot_preview_data
                st.rerun()
        with col_cancel:
            if st.button("Cancel", type="secondary"):
                st.session_state.file_uploader_key = st.session_state.get("file_uploader_key", 0) + 1
                del st.session_state.snapshot_preview_data
                st.rerun()

    st.markdown("---")

    if st.session_state.get("previous_snapshot"):
        date = st.session_state.previous_snapshot["saved_at"]
        st.success(
            f"Form loaded from your **{date}** snapshot. "
            "Review your numbers — update anything that has changed since then."
        )

    st.info(
        "**Don't have exact numbers?** Estimates are fine — a rough figure is better than leaving fields at 0. "
        "Open your bank or credit card app: most show a monthly spending breakdown by category."
    )

    with st.form("financial_form"):
        render_api_config()
        render_income_section()
        render_expenses_section()
        render_position_section()
        render_context_section()

        st.markdown("---")
        submitted = st.form_submit_button("Show me my financial picture →", type="primary")

    if submitted:
        if not st.session_state.api_key:
            st.error("Please enter an API key to continue.")
        elif st.session_state.income_main == 0:
            st.error("Please enter your monthly income to continue.")
        elif st.session_state.debt_monthly > 0 and st.session_state.debt_total == 0:
            st.error(
                f"Monthly debt payment is ${st.session_state.debt_monthly:,.0f} but total debt is $0. "
                "Either enter your total debt balance or set the monthly payment to $0."
            )
        else:
            st.session_state.current_page = "results"
            st.rerun()
