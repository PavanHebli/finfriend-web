import streamlit as st
from supabase import create_client, Client


def _get_client() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)


def submit_feedback(
    found_via: str,
    score_accuracy: int,
    most_useful: str,
    missing_or_confusing: str,
    feature_suggestion: str,
    anything_else: str,
    email: str,
) -> bool:
    """Insert one feedback row. Returns True on success, False on error."""
    try:
        client = _get_client()
        client.table("feedback").insert({
            "found_via":             found_via,
            "score_accuracy":        score_accuracy,
            "most_useful":           most_useful,
            "missing_or_confusing":  missing_or_confusing or None,
            "feature_suggestion":    feature_suggestion or None,
            "anything_else":         anything_else or None,
            "email":                 email or None,
        }).execute()
        return True
    except Exception as e:
        st.error(f"Could not save feedback: {e}")
        return False
