"""
Vitals Analytics — session-level event tracking via Supabase.
All writes are upserts on a single row per session_id.
Fails silently — never breaks the app.

Set DEBUG = true in secrets.toml to enable console prints.
"""
import uuid
import streamlit as st
from supabase import create_client


def _debug() -> bool:
    return st.secrets.get("DEBUG", False)


def _get_client():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)


def _get_session_id() -> str:
    """Returns a random UUID tied to this browser session. No PII."""
    if "analytics_session_id" not in st.session_state:
        st.session_state.analytics_session_id = str(uuid.uuid4())
    return st.session_state.analytics_session_id


def _upsert(data: dict):
    """Upserts a row into the sessions table. Fails silently."""
    try:
        session_id = _get_session_id()
        client = _get_client()
        client.table("sessions").upsert(
            {"session_id": session_id, **data},
            on_conflict="session_id",
        ).execute()
        if _debug():
            print(f"[ANALYTICS] upsert ok — session={session_id[:8]} data={data}")
    except Exception as e:
        if _debug():
            print(f"[ANALYTICS] upsert failed — {e}")


def log_results_viewed(score_band: str):
    show_api = st.secrets.get("SHOW_API_INPUT", True)
    provider = st.session_state.get("llm_provider", "") if show_api else "hosted"
    _upsert({
        "results_viewed": True,
        "score_band":     score_band,
        "provider":       provider,
    })


def log_narrative_done():
    _upsert({"narrative_done": True})


def log_whatif_used():
    _upsert({"whatif_used": True})


def log_snapshot_saved():
    _upsert({"snapshot_saved": True})


def log_snapshot_loaded():
    _upsert({"snapshot_loaded": True})


def log_chat_message(category: str):
    """
    Increments chat_turns and updates chat_categories frequency map.
    category: the primary classifier category for this message.
    """
    try:
        session_id = _get_session_id()
        client     = _get_client()

        # Fetch current row if it exists
        res = client.table("sessions").select(
            "chat_turns, chat_categories"
        ).eq("session_id", session_id).execute()

        if res.data:
            row        = res.data[0]
            turns      = (row.get("chat_turns") or 0) + 1
            categories = row.get("chat_categories") or {}
        else:
            turns      = 1
            categories = {}

        categories[category] = categories.get(category, 0) + 1

        _upsert({"chat_turns": turns, "chat_categories": categories})
    except Exception as e:
        if _debug():
            print(f"[ANALYTICS] log_chat_message failed — {e}")
