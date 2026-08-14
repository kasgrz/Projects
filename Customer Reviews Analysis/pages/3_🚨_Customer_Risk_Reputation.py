from navigation import show_navigation
import streamlit as st
import pandas as pd
import plotly.express as px

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Customer Risk & Reputation",
    page_icon="🚨",
    layout="wide"
)

show_navigation("risk")
# ============================================================
# PAGE STYLING
# ============================================================
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("""
<style>

div[data-baseweb="popover"] {
    background-color: #131A22 !important;
}

div[data-baseweb="popover"] li {
    background-color: #131A22 !important;
    color: white !important;
}

div[data-baseweb="popover"] li:hover {
    background-color: #FF9900 !important;
    color: #131A22 !important;
}

div[data-baseweb="popover"] li[aria-selected="true"] {
    background-color: #B0B8C2 !important;
    color: #131A22 !important;
}

/* General dashboard styling */

* {
    font-family: Arial, Helvetica, sans-serif;
    font-weight: 400;
}

.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background-color: #131A22 !important;
    color: white;
}

/* Headings */

h1, h2, h3 {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# PAGE STYLING
# ============================================================

st.markdown(
    """
    """,
    unsafe_allow_html=True
)

# ============================================================
# LOAD DATA
# ============================================================

df_dashboard = pd.read_csv(
    "amazon_reviews_dashboard2.csv"
)

df_dashboard["review_date"] = pd.to_datetime(
    df_dashboard["review_date"]
)

escalation_risk = (
    df_dashboard[df_dashboard["escalation_score"] > 0]
    ["risk_level"]
    .value_counts()
)

# ============================================================
# SHORT PRODUCT NAME
# ============================================================

df_dashboard["product_short"] = (
    df_dashboard["product_title"]
    .str.split(r"[,/(\-]", regex=True)
    .str[0]
    .str.strip()
)



# ============================================================
# PAGE — CUSTOMER RISK & REPUTATION
# ============================================================

st.header("Reputation Risk Monitoring")

st.markdown(
    """
    Monitor reputation risk and customer escalation signals.
    """,
    unsafe_allow_html=True
)

# ============================================================
# RISK FILTERS
# ============================================================

risk_filter_col1, risk_filter_col2, risk_filter_col3, risk_filter_spacer = st.columns([1.2, 1.2, 0.8, 2.5])

with risk_filter_col1:
    selected_product_group = st.selectbox(
        "Product Group",
        ["All Product Groups"]
        + sorted(
            df_dashboard["product_group"]
            .dropna()
            .unique()
            .tolist()
        ),
        key="risk_product_group"
    )

with risk_filter_col2:

    store_options = (
        df_dashboard[
            df_dashboard["product_group"] == selected_product_group
        ]["store"]
        .dropna()
        .unique()
        .tolist()
        if selected_product_group != "All Product Groups"
        else
        df_dashboard["store"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_store = st.selectbox(
        "Brand",
        ["All Brands"] + sorted(store_options),
        key="risk_store"
    )

with risk_filter_col3:
    selected_month = st.selectbox(
        "Month",
        ["All Months"] + list(range(1, 13)),
        format_func=lambda x:
            "All Months"
            if x == "All Months"
            else pd.Timestamp(2024, x, 1).strftime("%B"),
        key="risk_month"
    )

# ============================================================
# APPLY RISK FILTERS
# ============================================================

if selected_product_group != "All Product Groups":
    df_dashboard = df_dashboard[
        df_dashboard["product_group"] == selected_product_group
    ]

if selected_store != "All Brands":
    df_dashboard = df_dashboard[
        df_dashboard["store"] == selected_store
    ]

if selected_month != "All Months":
    df_dashboard = df_dashboard[
        df_dashboard["review_date"].dt.month == selected_month
    ]

# ============================================================
# HIGH & CRITICAL REVIEWS
# ============================================================

risk_reviews = df_dashboard[
    df_dashboard["risk_level"].isin(["High", "Critical"])
].copy()

risk_reviews = risk_reviews.sort_values(
    "helpful_vote",
    ascending=False
)


# ============================================================
# HIGH & CRITICAL REVIEWS WITH ESCALATION
# ============================================================

high_impact = risk_reviews[
    risk_reviews["escalation_score"] > 0
].copy()

# ============================================================
# HIGH-IMPACT RISK SUMMARY
# ============================================================

risk_col1, risk_col2, risk_col3, risk_col4 = st.columns(4)

with risk_col1:
    st.metric(
        "High/Critical Risk Reviews",
        f"{len(risk_reviews):,}",
        help=("Reviews classified as High or Critical using a combined risk score based on rating, sentiment, and escalation potential."
        )
    )

with risk_col2:
    st.metric(
        "Escalation Signals Detected",
        f"{len(high_impact):,}",
        help=(
        "Reviews containing escalation signals that indicate an increased likelihood of customer action or business intervention, such as unresolved refund requests, consumer rights concerns, potential legal action, or intentions to share the issue on social media."
        )
    )

with risk_col3:
    
    st.metric(
        "Products Affected",
        risk_reviews["product_title"].nunique(),
        help=(
        "Unique products with at least one High or Critical review."
        
        )
    )


with risk_col4:
    avg_helpful = risk_reviews["helpful_vote"].mean()
    if pd.isna(avg_helpful):
        avg_helpful = 0
    st.metric(
        "Average Helpful Votes",
        f"{avg_helpful:.1f}",
        help=(
            "Average number of helpful votes received by High and Critical reviews."
        )
    )

# ============================================================
# CHARTS — CUSTOMER RISK PROFILE + RISK CONCENTRATION
# ============================================================

risk_counts = (
    df_dashboard["risk_level"]
    .value_counts()
    .reindex(["Low", "Medium", "High", "Critical"])
    .reset_index()
)

risk_counts.columns = ["risk_level", "reviews"]


# ============================================================
# TWO-COLUMN LAYOUT
# ============================================================

chart_col1, chart_col2 = st.columns(2)


# ============================================================
# CHART 1 — CUSTOMER RISK PROFILE
# ============================================================

with chart_col1:

    fig_risk = px.pie(
        risk_counts,
        names="risk_level",
        values="reviews",
        hole=0.55,
        color="risk_level",
        color_discrete_map={
            "Low": "#37475A",
            "Medium": "#A36A63",
            "High": "#CF4740",
            "Critical": "#B91C1C"
        }
    )

    fig_risk.update_traces(
        textposition="outside",
        textinfo="percent",
        texttemplate="%{percent:.1%}",
        textfont=dict(size=18),
        hovertemplate=(
            "<b>%{label}</b><br>"
            "%{value:,} reviews<br>"
            "%{percent:.1%}"
            "<extra></extra>"
        )
    )

    fig_risk.update_layout(
        title="Review Risk Distribution",
        height=450,
        paper_bgcolor="#0F141A",
        plot_bgcolor="#0F141A",
        font=dict(color="white"),
        showlegend=True,
        legend_title=None,
        margin=dict(
            l=10,
            r=10,
            t=60,
            b=10
        )
    )

    fig_risk.update_traces(
        domain=dict(
            x=[0.12, 0.88],
            y=[0.12, 0.88]
        )
    )

    st.plotly_chart(
        fig_risk,
        use_container_width=True
    )


# ============================================================
# CHART 2 — RISK RATE BY CATEGORY
# ============================================================

with chart_col2:

    risk_categories = (
        df_dashboard[
            df_dashboard["primary_aspect"].notna()
            & (df_dashboard["primary_aspect"] != "Other")
        ]
        .groupby("primary_aspect")
        .agg(
            total_reviews=("risk_level", "size"),
            high_reviews=(
                "risk_level",
                lambda x: (x == "High").sum()
            ),
            critical_reviews=(
                "risk_level",
                lambda x: (x == "Critical").sum()
            ),
        )
        .reset_index()
    )

    risk_categories["high_rate"] = (
        risk_categories["high_reviews"]
        / risk_categories["total_reviews"]
        * 100
    )

    risk_categories["critical_rate"] = (
        risk_categories["critical_reviews"]
        / risk_categories["total_reviews"]
        * 100
    )

    risk_categories["risk_rate"] = (
        risk_categories["high_rate"]
        + risk_categories["critical_rate"]
    )

    # Keep categories with at least 500 reviews
    risk_categories = risk_categories[
        risk_categories["total_reviews"] >= 500
    ]

    # Keep the 8 categories with the highest risk rate
    risk_categories = (
        risk_categories
        .nlargest(8, "risk_rate")
        .sort_values("risk_rate")
    )

    plot_data = (
        risk_categories[
            ["primary_aspect", "high_rate", "critical_rate"]
        ]
        .melt(
            id_vars="primary_aspect",
            var_name="risk_level",
            value_name="rate"
        )
    )


    plot_data["risk_level"] = plot_data["risk_level"].replace({
        "high_rate": "High",
        "critical_rate": "Critical"
    })
    
    fig_risk_rate = px.bar(
        plot_data,
        x="rate",
        y="primary_aspect",
        color="risk_level",
        orientation="h",
        barmode="stack",
        color_discrete_map={
            "High": "#CF4740",
            "Critical": "#B91C1C"
        }
    )
    
    fig_risk_rate.update_traces(
        hovertemplate=(
            "<b>%{y}</b><br>"
            "%{fullData.name}: %{x:.1f}%"
            "<extra></extra>"
        )
    )
    
    fig_risk_rate.update_layout(
        title=(
            "Categories Requiring Attention"
            "<br><sup>Share of High and Critical reviews · Minimum 500 reviews</sup>"
        ),
        height=450,
        paper_bgcolor="#0F141A",
        plot_bgcolor="#0F141A",
        font=dict(color="white"),
        legend_title=None,
        xaxis_title="% of Reviews",
        yaxis_title=None,
        margin=dict(l=10, r=40, t=60, b=40)
    )
    
    fig_risk_rate.update_xaxes(
        gridcolor="#37475A",
        ticksuffix="%"
    )
    
    fig_risk_rate.update_yaxes(
        gridcolor="#37475A"
    )

    # ============================================================
    # ADD TOTAL RISK RATE LABELS
    # ============================================================
    
    risk_categories["risk_label"] = (
        risk_categories["risk_rate"]
        .round(1)
        .astype(str)
        + "%"
    )
    
    for _, row in risk_categories.iterrows():
        fig_risk_rate.add_annotation(
            x=row["risk_rate"] + 0.3,
            y=row["primary_aspect"],
            text=row["risk_label"],
            showarrow=False,
            xanchor="left",
            font=dict(
                size=13,
                color="white"
            )
        )

    
    st.plotly_chart(
        fig_risk_rate,
        use_container_width=True
    )
# ============================================================
# HIGH-IMPACT RISK CASES
# ============================================================

st.subheader("High-Impact Risk Cases")

st.markdown(
    "High and Critical risk reviews "
    "prioritized by number of Helpful Votes received from other customers."
)

## Create filters

filter_col1, filter_col2 = st.columns(2)

with filter_col1:
    selected_risk = st.selectbox(
        "Risk Level",
        ["All", "High", "Critical"]
    )

with filter_col2:
    selected_category = st.selectbox(
        "Category",
        ["All"] + sorted(
            risk_reviews["primary_aspect"]
            .dropna()
            .unique()
            .tolist()
        )
    )

## Apply filters

risk_cases = risk_reviews.copy()

if selected_risk != "All":
    risk_cases = risk_cases[
        risk_cases["risk_level"] == selected_risk
    ]

if selected_category != "All":
    risk_cases = risk_cases[
        risk_cases["primary_aspect"] == selected_category
    ]

risk_cases = risk_cases.sort_values(
    "helpful_vote",
    ascending=False
)

show_escalation = st.checkbox(
    "Show potential escalation cases only",
    value=False
)

if show_escalation:
    risk_cases = risk_cases[
        risk_cases["escalation_score"] > 0
    ]
## Display

display_cases = risk_cases[
    [
        "store",
        "product_short",
        "primary_aspect",
        "helpful_vote",
        "escalation_score",
        "review"
    ]
]

display_cases = display_cases.rename(
    columns={
        "product_short": "Product",
        "primary_aspect": "Category",
        "store": "Brand",
        "helpful_vote": "Helpful Votes",
        "escalation_score": "Escalation Score",
        "review": "Review"
    }
)

st.dataframe(
    display_cases,
    use_container_width=True,
    hide_index=True
)

# ------------------------------------------------------------
# REVIEW COUNT
# ------------------------------------------------------------

matching_cases = len(display_cases)

st.markdown(
    f"""
    <div style="
        text-align: right;
        color: #A9B0B8;
        font-size: 14px;
        margin-top: 8px;
        margin-bottom: 12px;
    ">
        <strong style="
            color: white;
            font-size: 20px;
        ">
            {matching_cases:,}
        </strong>
        matching risk cases
    </div>
    """,
    unsafe_allow_html=True
)
# --------------------------------------------------------
# DOWNLOAD DISPLAYED RISK CASES
# --------------------------------------------------------

csv_data = display_cases.to_csv(index=False)

st.download_button(
    label="⬇ Download matching risk cases",
    data=csv_data,
    file_name="high_impact_risk_cases.csv",
    mime="text/csv"
)
