import streamlit as st
from modules.panel_form import render_form_panel
from modules.panel_results import render_results_panel


def init_session_state():
    defaults = {
        "llm_provider": "groq",
        "api_key": "",
        "income_main": 0.0,
        "income_additional": 0.0,
        "expenses_rent": 0.0,
        "expenses_groceries": 0.0,
        "expenses_transport": 0.0,
        "expenses_subscriptions": 0.0,
        "expenses_dining": 0.0,
        "expenses_shopping": 0.0,
        "expenses_other": 0.0,
        "savings_total": 0.0,
        "investments_total": 0.0,
        "debt_total": 0.0,
        "debt_monthly": 0.0,
        "age": 25,
        "employment": "Employed",
        "has_health_insurance": False,
        "has_emergency_fund": "Not sure",
        "contributing_401k": "No",
        "data_entered": False,
        "current_page": "form",
        "sample_input_active": False,
        "file_uploader_key": 0,
        "loaded_snapshots": [],
        "chat_history": [],
        "chat_summary": "",

    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def main():
    st.set_page_config(
        page_title="Vitals",
        page_icon="🩺",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Global font sizes — change --label-size and --caption-size to affect everything at once
    st.markdown("""
        <style>
            :root {
                --label-size:   1.05rem;
                --caption-size: 0.5rem;
                --body-size:    1.05rem;
                --input-size:   1.0rem;
                --button-size:  1.0rem;
                --tab-size:     1.5rem;
            }

            /* Body text and markdown paragraphs */
            .stMarkdown p, .stMarkdown li { font-size: var(--body-size); line-height: 1.75; }

            /* All form labels — target the <p> inside the label element */
            label p { font-size: var(--label-size) !important; font-weight: 500; }
            [data-testid="stWidgetLabel"] p { font-size: var(--label-size) !important; font-weight: 500; }
            .stRadio label p, .stCheckbox label p { font-size: var(--label-size) !important; }
            .stFileUploader label p { font-size: var(--label-size) !important; font-weight: 500; }

            /* Input field values */
            .stNumberInput input, .stTextInput input { font-size: var(--input-size) !important; }
            .stSelectbox div[data-baseweb="select"] { font-size: var(--input-size); }
            .stFileUploader section { font-size: var(--input-size); }

            /* Captions — secondary hint text */
            .stCaption p { font-size: var(--caption-size) !important; }

            /* Tabs — full width, equal spacing, intuitive and clickable */
            .stTabs [data-baseweb="tab-list"] {
                width: 100%;
                display: flex;
                gap: 8px;
            }
            .stTabs [data-baseweb="tab"] {
                flex: 1;
                justify-content: center;
                padding: 10px 0;
                border-radius: 6px 6px 0 0;
                background: rgba(255,255,255,0.05);
                cursor: pointer;
                transition: background 0.2s ease;
                font-weight: 400;
            }
            .stTabs [data-baseweb="tab"]:hover {
                background: rgba(255,255,255,0.1);
            }
            .stTabs [data-baseweb="tab"][aria-selected="true"] {
                background: rgba(255,255,255,0.12);
                border-bottom: 2px solid #1C83E1;
                font-weight: 600;
            }
            .stTabs [data-baseweb="tab"] p { font-size: var(--tab-size) !important; }
            .stTabs [data-baseweb="tab"][aria-selected="true"] p { font-size: var(--tab-size) !important; font-weight: 600 !important; }
            .stTabs button p { font-size: var(--tab-size) !important; }

            /* Buttons */
            .stButton button, .stDownloadButton button { font-size: var(--button-size); }
        </style>
    """, unsafe_allow_html=True)

    init_session_state()

    if st.session_state.current_page == "form":
        render_form_panel()
    else:
        render_results_panel()


if __name__ == "__main__":
    main()
