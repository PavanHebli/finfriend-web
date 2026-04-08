import streamlit as st
import plotly.graph_objects as go
from datetime import datetime


_SCORE_COLORS = {
    "Critical": "#FF4B4B",
    "At Risk":  "#FF8C00",
    "Fair":     "#FFD700",
    "Good":     "#1C83E1",
    "Healthy":  "#00C853",
}

_CHART_LAYOUT = dict(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="white", size=12),
    margin=dict(l=10, r=10, t=30, b=30),
    showlegend=False,
)


def _merge(snapshots: list, current_snapshot: dict) -> tuple[list, bool]:
    """
    Merges current session snapshot into history.
    Returns (merged_list, is_new_month).
    """
    current_month = current_snapshot["saved_at"]
    result = list(snapshots)
    for i, snap in enumerate(result):
        if snap.get("saved_at") == current_month:
            result[i] = current_snapshot
            return result, False
    result.append(current_snapshot)
    return result, True


def _line_chart(months, values, hist_len, title, color, y_suffix="",
                reference=None, reference_label="", marker_colors=None):
    """
    Line chart with split traces: solid for history, dotted+hollow for current point.
    marker_colors: optional per-point color list for historical markers (used for score chart).
    """
    fig = go.Figure()

    hist_marker_colors = marker_colors[:hist_len] if marker_colors else color

    # Historical trace — solid line + filled markers
    fig.add_trace(go.Scatter(
        x=months[:hist_len],
        y=values[:hist_len],
        mode="lines+markers",
        line=dict(color=color, width=2),
        marker=dict(size=9, color=hist_marker_colors, line=dict(color="white", width=1)),
        hovertemplate=f"%{{x}}: %{{y}}{y_suffix}<extra></extra>",
    ))

    # Current session point — dotted bridge + hollow marker
    if len(months) > hist_len:
        fig.add_trace(go.Scatter(
            x=[months[hist_len - 1], months[hist_len]],
            y=[values[hist_len - 1], values[hist_len]],
            mode="lines",
            line=dict(color=color, width=2, dash="dot"),
            hoverinfo="skip",
        ))
        current_color = marker_colors[hist_len] if marker_colors else color
        fig.add_trace(go.Scatter(
            x=[months[hist_len]],
            y=[values[hist_len]],
            mode="markers",
            marker=dict(size=11, color="rgba(0,0,0,0)",
                        line=dict(color=current_color, width=2)),
            hovertemplate=f"%{{x}} (current): %{{y}}{y_suffix}<extra></extra>",
        ))

    if reference is not None:
        fig.add_hline(
            y=reference,
            line_dash="dash",
            line_color="rgba(255,255,255,0.25)",
            annotation_text=reference_label,
            annotation_font_color="rgba(255,255,255,0.45)",
            annotation_position="top right",
        )

    fig.update_layout(
        title=dict(text=title, font=dict(size=13)),
        xaxis=dict(tickangle=-30),
        yaxis=dict(ticksuffix=y_suffix),
        height=220,
        **_CHART_LAYOUT,
    )
    return fig


def render_progress(snapshots: list, current_snapshot: dict):
    """
    Renders progress charts merging saved history with current session data.
    Current session point shown as hollow marker with dotted connecting line.
    Requires 2+ total points to show charts.
    """
    merged, is_new_month = _merge(snapshots, current_snapshot)

    if len(merged) < 2:
        st.info(
            "**No history yet.**  \n"
            "Save a snapshot each month — your progress charts will appear here "
            "once you have 2 or more entries.  \n"
            "Click **💾 Save snapshot** above after viewing your results."
        )
        return

    hist_len = len(merged) - 1 if is_new_month else len(merged)

    if is_new_month:
        st.caption("○ Hollow point = current session (not yet saved)")

    # --- Extract series ---
    months          = [s["saved_at"] for s in merged]
    scores          = [s["outputs"]["overall_score"] for s in merged]
    labels          = [s["outputs"]["mirror_label"] for s in merged]
    dot_colors      = [_SCORE_COLORS.get(l, "#FFFFFF") for l in labels]
    metrics_list    = [s["outputs"]["metrics"] for s in merged]
    savings_rates   = [m["savings_rate"] for m in metrics_list]
    dtis            = [m["debt_to_income"] for m in metrics_list]
    emergency_funds = [m["emergency_fund_months"] for m in metrics_list]
    housing_ratios  = [m["housing_ratio"] for m in metrics_list]
    net_flows       = [m["net_monthly_flow"] for m in metrics_list]

    # --- Score over time ---
    st.markdown("##### Overall Score")
    st.plotly_chart(
        _line_chart(months, scores, hist_len, "", "#1C83E1",
                    y_suffix=" pts", marker_colors=dot_colors),
        width="stretch",
    )

    # Override score chart height
    # (done inline above — title empty since markdown header is used instead)

    # --- 4 metric trends in 2x2 grid ---
    st.markdown("##### Metric Trends")
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            _line_chart(months, savings_rates, hist_len, "Savings Rate", "#00C853",
                        y_suffix="%", reference=20, reference_label="20% target"),
            width="stretch",
        )
        st.plotly_chart(
            _line_chart(months, emergency_funds, hist_len, "Emergency Fund", "#1C83E1",
                        y_suffix=" mo", reference=3, reference_label="3 mo minimum"),
            width="stretch",
        )

    with col2:
        st.plotly_chart(
            _line_chart(months, dtis, hist_len, "Debt-to-Income", "#FF8C00",
                        y_suffix="%", reference=43, reference_label="43% danger (CFPB)"),
            width="stretch",
        )
        st.plotly_chart(
            _line_chart(months, housing_ratios, hist_len, "Housing Ratio", "#FFD700",
                        y_suffix="%", reference=30, reference_label="30% limit (HUD)"),
            width="stretch",
        )

    # --- Net cash flow bar chart ---
    st.markdown("##### Cash Left Each Month")
    bar_colors = ["#00C853" if v >= 0 else "#FF4B4B" for v in net_flows]
    if is_new_month:
        bar_colors[-1] = "rgba(0,200,83,0.4)" if net_flows[-1] >= 0 else "rgba(255,75,75,0.4)"

    fig_flow = go.Figure()
    fig_flow.add_trace(go.Bar(
        x=months,
        y=net_flows,
        marker_color=bar_colors,
        hovertemplate="%{x}: $%{y:,.0f}<extra></extra>",
    ))
    fig_flow.add_hline(y=0, line_color="rgba(255,255,255,0.2)")
    fig_flow.update_layout(
        xaxis=dict(tickangle=-30),
        yaxis=dict(tickprefix="$"),
        height=220,
        **_CHART_LAYOUT,
    )
    st.plotly_chart(fig_flow, width="stretch")
