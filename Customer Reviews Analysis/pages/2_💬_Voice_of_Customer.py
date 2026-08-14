import streamlit as st
import pandas as pd
import plotly.express as px

from navigation import show_navigation

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Voice of Customer",
    page_icon="💬",
    layout="wide"
)

show_navigation("voice")


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
# ============================================================
# PAGE STYLING
# ============================================================

st.markdown("""
<style>

/* ----------------------------------------------------------
   Dropdown menu
---------------------------------------------------------- */

div[data-baseweb="popover"] {
    background-color: #131A22 !important;
}

div[data-baseweb="popover"] li {
    background-color: #131A22 !important;
    color: white !important;
}

/* Highlighted dropdown option */
div[data-baseweb="popover"] li:hover {
    background-color: #FF9900 !important;
    color: #131A22 !important;
}

/* Selected dropdown option */
div[data-baseweb="popover"] li[aria-selected="true"] {
    background-color: #B0B8C2 !important;
    color: #131A22 !important;
}


/* ----------------------------------------------------------
   General dashboard styling
---------------------------------------------------------- */

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


/* ----------------------------------------------------------
   Headings
---------------------------------------------------------- */

h1, h2, h3 {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)



# ============================================================
# LOAD DATA
# ============================================================

df_dashboard = pd.read_csv(
    "amazon_reviews_dashboard2.csv"
)

df_dashboard["review_date"] = pd.to_datetime(
    df_dashboard["review_date"]
)

df_dashboard["product_short"] = (
    df_dashboard["product_title"]
    .str.split(r"[,/(\-]", regex=True)
    .str[0]
    .str.strip()
)
# ============================================================
# PAGE 2 — VOICE OF CUSTOMER
# ============================================================

st.header("Voice of Customer")

st.markdown(
    """
    <div style="
        font-size: 20px;
        font-weight: 400;
        color: white;
        margin-bottom: 28px;
    ">
        Explore what customers are talking about across their reviews.
    </div>
    """,
    unsafe_allow_html=True
)


st.subheader("What Customers Comment On")

month_col, _ = st.columns([1, 4])

with month_col:
    selected_month = st.selectbox(
        "Month",
        ["All Months"] + list(range(1, 13)),
        format_func=lambda x: (
            "All Months"
            if x == "All Months"
            else pd.Timestamp(2024, x, 1).strftime("%B")
        ),
        key="comment_month"
    )
# ------------------------------------------------------------
# RATING FILTER
# ------------------------------------------------------------

st.markdown(
"""
Rating
""",
unsafe_allow_html=True
)

rating_cols = st.columns(5)

selected_ratings = []

for i, rating in enumerate([1, 2, 3, 4, 5]):

    with rating_cols[i]:

        if st.checkbox(
            "⭐" * rating,
            value=rating in [1, 2, 3],
            key=f"rating_{rating}"
        ):
            selected_ratings.append(rating)

explorer_df = df_dashboard.copy()

if selected_ratings:
    explorer_df = explorer_df[
        explorer_df["rating"].isin(selected_ratings)
    ]

if selected_month != "All Months":
    explorer_df = explorer_df[
        explorer_df["review_date"].dt.month == selected_month
    ]

# ============================================================
# Dynamic chart color based on selected ratings
# ============================================================

RATING_COLORS = {
    1: "#7A2E2E",   # 1★
    2: "#A14A2A",   # 2★
    3: "#C46A1A",   # 3★
    4: "#E68A00",   # 4★
    5: "#FF9900"    # 5★
}

selected = sorted(selected_ratings)

if selected == [1]:
    chart_color = RATING_COLORS[1]

elif selected == [2]:
    chart_color = RATING_COLORS[2]

elif selected == [3]:
    chart_color = RATING_COLORS[3]

elif selected == [4]:
    chart_color = RATING_COLORS[4]

elif selected == [5]:
    chart_color = RATING_COLORS[5]

# 1★ + 2★
elif selected == [1, 2]:
    chart_color = "#8D3C2C"

# 1★ + 2★ + 3★
elif selected == [1, 2, 3]:
    chart_color = RATING_COLORS[2]

# 4★ + 5★
elif selected == [4, 5]:
    chart_color = "#F28F00"

# Everything else (e.g. All, 2+3, 3+4, 1+3+5...)
else:
    chart_color = RATING_COLORS[3]

# ============================================================
# CHART 1
# ============================================================

aspect_rating_counts = (
    explorer_df[
        explorer_df["primary_aspect"].notna()
        & (explorer_df["primary_aspect"] != "Other")
    ]
    .groupby(
        ["primary_aspect", "rating"]
    )
    .size()
    .reset_index(name="reviews")
)

aspect_rating_counts["rating"] = (
    aspect_rating_counts["rating"]
    .astype(int)
    .astype(str)
)

# Keep the 10 most mentioned categories overall
top_aspects = (
    aspect_rating_counts
    .groupby("primary_aspect")["reviews"]
    .sum()
    .nlargest(10)
    .index
)

aspect_rating_counts = aspect_rating_counts[
    aspect_rating_counts["primary_aspect"].isin(top_aspects)
]

aspect_rating_counts["percentage"] = (
    aspect_rating_counts["reviews"]
    / aspect_rating_counts.groupby("primary_aspect")["reviews"].transform("sum")
    * 100
)

# ------------------------------------------------------------
# Chart
# ------------------------------------------------------------

fig_aspects = px.bar(
    aspect_rating_counts,
    x="reviews",
    y="primary_aspect",
    color="rating",
    orientation="h",
    text="reviews",
    category_orders={
        "primary_aspect": (
            aspect_rating_counts
            .groupby("primary_aspect")["reviews"]
            .sum()
            .sort_values()
            .index
            .tolist()
        ),
        "rating": ["1", "2", "3", "4", "5"]
    },
    color_discrete_map={
        "1": "#7A2E2E",
        "2": "#A14A2A",
        "3": "#C46A1A",
        "4": "#E68A00",
        "5": "#FF9900"
    }
)

fig_aspects.update_traces(
    text=None,
    customdata=aspect_rating_counts["percentage"],
    hovertemplate=(
        "<b>%{y}</b><br>"
        "Rating: %{fullData.name}★<br>"
        "Reviews: %{x:,}<br>"
        "Share: %{customdata:.1f}%"
        "<extra></extra>"
    )
)

# Total reviews per category
category_totals = (
    aspect_rating_counts
    .groupby("primary_aspect")["reviews"]
    .sum()
)

for category, total in category_totals.items():

    fig_aspects.add_annotation(
        x=total,
        y=category,
        text=f"{total:,}",
        showarrow=False,
        xanchor="left",
        xshift=8,
        font=dict(
            color="white",
            size=14
        )
    )

fig_aspects.update_layout(
    title="Most Mentioned Categories",
    height=500,
    barmode="stack",
    showlegend=True,
    paper_bgcolor="#0F141A",
    plot_bgcolor="#0F141A",
    font=dict(
        color="white"
    ),
    xaxis_title="Number of Reviews",
    yaxis_title=None,
    legend_title="Rating",
    margin=dict(
        l=10,
        r=80,
        t=60,
        b=40
    )
)

fig_aspects.update_xaxes(
    gridcolor="#37475A",
    zerolinecolor="#37475A"
)

fig_aspects.update_yaxes(
    gridcolor="#37475A",
    categoryorder="total ascending"
)

st.plotly_chart(
    fig_aspects,
    use_container_width=True
)

# ============================================================
# REVIEW EXPLORER
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("Review Explorer")

import re

def short_product_name(product):
    if product == "Select a product":
        return product

    # Cut at the first major punctuation mark
    short_name = re.split(r"[,/():;\[\]\-–—|]", product)[0]

    return short_name.strip()

# ============================================================
# REVIEW EXPLORER FILTERS
# ============================================================

# ------------------------------------------------------------
# ROW 1 — CATEGORY + FINDING
# ------------------------------------------------------------

filter_col1, filter_col2 = st.columns(2)

with filter_col1:

    selected_category = st.selectbox(
        "Category",
        ["All Categories"]
        + sorted(
            df_dashboard[
                df_dashboard["primary_aspect"] != "Other"
            ]["primary_aspect"]
            .dropna()
            .unique()
            .tolist()
        ),
        key="explorer_category"
    )


with filter_col2:

    selected_finding = st.selectbox(
        "Finding",
        ["All Findings"]
        + sorted(
            df_dashboard[
                (df_dashboard["primary_finding"] != "Other")
                & df_dashboard["primary_finding"].notna()
            ]["primary_finding"]
            .unique()
            .tolist()
        ),
        key="explorer_finding"
    )


# ------------------------------------------------------------
# ROW 2 — PRODUCT GROUP + PRODUCT
# ------------------------------------------------------------

filter_col3, filter_col4, filter_col5 = st.columns(3)

with filter_col3:

    selected_group = st.selectbox(
        "Product Group",
        ["All Product Groups"]
        + sorted(
            df_dashboard["product_group"]
            .dropna()
            .unique()
            .tolist()
        ),
        key="explorer_product_group"
    )

with filter_col4:

    brand_options = (
        df_dashboard[
            df_dashboard["product_group"] == selected_group
        ]["brand"]
        .dropna()
        .unique()
        .tolist()
        if selected_group != "All Product Groups"
        else
        df_dashboard["store"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_brand = st.selectbox(
        "Brand",
        ["All Brands"] + sorted(brand_options),
        key="explorer_brand"
    )


with filter_col5:

    product_df = df_dashboard.copy()

    if selected_group != "All Product Groups":
        product_df = product_df[
            product_df["product_group"] == selected_group
        ]

    if selected_brand != "All Brands":
        product_df = product_df[
            product_df["store"] == selected_brand
        ]

    product_options = sorted(
        product_df["product_title"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_product = st.selectbox(
        "Product",
        ["Select a product"] + product_options,
        format_func=short_product_name,
        key="explorer_product"
    )

explorer_df = explorer_df.copy()

# Product group filter
if selected_group != "All Product Groups":
    explorer_df = explorer_df[
        explorer_df["product_group"] == selected_group
    ]

# Rating filter
if selected_ratings:
    explorer_df = explorer_df[
        explorer_df["rating"].isin(selected_ratings)
    ]

# Brand filter

if selected_brand != "All Brands":
    explorer_df = explorer_df[
        explorer_df["store"] == selected_brand
    ]

# Product filter — only applied when a product is selected
if selected_product != "Select a product":
    explorer_df = explorer_df[
        explorer_df["product_title"] == selected_product
    ]

# Category filter
if selected_category != "All Categories":
    explorer_df = explorer_df[
        explorer_df["primary_aspect"] == selected_category
    ]

# Finding filter
if selected_finding != "All Findings":
    explorer_df = explorer_df[
        explorer_df["primary_finding"] == selected_finding
    ]

# ------------------------------------------------------------
# APPLY EXPLORER FILTERS
# ------------------------------------------------------------

explorer_df = explorer_df.copy()

# Shared Rating filter
if selected_ratings:
    explorer_df = explorer_df[
        explorer_df["rating"].isin(selected_ratings)
    ]

# Explorer-only Category filter
if selected_category != "All Categories":
    explorer_df = explorer_df[
        explorer_df["primary_aspect"] == selected_category
    ]

# Explorer-only Finding filter
if selected_finding != "All Findings":
    explorer_df = explorer_df[
        explorer_df["primary_finding"] == selected_finding
    ]

# Explorer-only Product Group filter
if selected_group != "All Product Groups":
    explorer_df = explorer_df[
        explorer_df["product_group"] == selected_group
    ]

# Explorer-only Product filter
if selected_product != "Select a product":
    explorer_df = explorer_df[
        explorer_df["product_title"] == selected_product
    ]

# ------------------------------------------------------------
# REVIEW COUNT
# ------------------------------------------------------------

review_count = len(explorer_df)

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
            {review_count:,}
        </strong>
        reviews match your selection
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# CATEGORY + FINDING EXPLORER
# ============================================================

col_category, col_finding = st.columns(2)


# ------------------------------------------------------------
# LEFT — CATEGORIES
# ------------------------------------------------------------

with col_category:

    if selected_finding == "All Findings":
        category_title = "Categories"
    else:
        category_title = f'Categories for "{selected_finding}"'

    st.subheader(category_title)

    category_counts = (
        explorer_df[
            explorer_df["primary_aspect"].notna()
            & (explorer_df["primary_aspect"] != "Other")
        ]["primary_aspect"]
        .value_counts()
        .head(8)
        .reset_index()
    )

    category_counts.columns = [
        "category",
        "reviews"
    ]

    fig_categories = px.bar(
        category_counts.sort_values("reviews"),
        x="reviews",
        y="category",
        orientation="h",
        text="reviews"
    )

    fig_categories.update_traces(
        marker_color=chart_color,
        texttemplate="%{text:,}",
        textposition="outside",
        textfont=dict(
            color="white",
            size=13
        ),
    cliponaxis=False
    )

    fig_categories.update_layout(
        height=420,
        showlegend=False,
        paper_bgcolor="#0F141A",
        plot_bgcolor="#0F141A",
        font=dict(color="white"),
        xaxis_title="Number of Reviews",
        yaxis_title=None,
        margin=dict(
            l=10,
            r=60,
            t=30,
            b=40
        )
    )

    fig_categories.update_xaxes(
        gridcolor="#37475A",
        zerolinecolor="#37475A"
    )

    st.plotly_chart(
        fig_categories,
        use_container_width=True
    )


# ------------------------------------------------------------
# RIGHT — FINDINGS
# ------------------------------------------------------------

with col_finding:

    if selected_category == "All Categories":
        finding_title = "Findings"
    else:
        finding_title = f"Findings within {selected_category}"

    st.subheader(finding_title)

    finding_counts = (
        explorer_df[
            explorer_df["primary_finding"].notna()
            & (explorer_df["primary_finding"] != "Other")
        ]["primary_finding"]
        .value_counts()
        .head(8)
        .reset_index()
    )

    finding_counts.columns = [
        "finding",
        "reviews"
    ]

    fig_findings = px.bar(
        finding_counts.sort_values("reviews"),
        x="reviews",
        y="finding",
        orientation="h",
        text="reviews"
    )

    fig_findings.update_traces(
        marker_color=chart_color,
        texttemplate="%{text:,}",
        textposition="outside",
        textfont=dict(
            color="white",  
            size=13
        ),
    cliponaxis=False
    )

    fig_findings.update_layout(
        height=420,
        showlegend=False,
        paper_bgcolor="#0F141A",
        plot_bgcolor="#0F141A",
        font=dict(color="white"),
        xaxis_title="Number of Reviews",
        yaxis_title=None,
        margin=dict(
            l=10,
            r=60,
            t=30,
            b=40
        )
    )

    fig_findings.update_xaxes(
        gridcolor="#37475A",
        zerolinecolor="#37475A"
    )

    st.plotly_chart(
        fig_findings,
        use_container_width=True
    )
# ------------------------------------------------------------
# CUSTOMER REVIEWS
# ------------------------------------------------------------

if not explorer_df.empty:

    st.subheader("Customer Reviews")

    # --------------------------------------------------------
    # SORT OPTIONS
    # --------------------------------------------------------

    title_col, sort_col = st.columns([5, 1])

    with sort_col:
        sort_option = st.selectbox(
        "Sort",
        [
            "Lowest rating",
            "Highest rating",
            "Most recent",
            "Most helpful"
        ],
        key="review_sort",
        label_visibility="collapsed"
    )

    # Full filtered dataset
    filtered_reviews = explorer_df.copy()

    # --------------------------------------------------------
    # SORT
    # --------------------------------------------------------

    if sort_option == "Lowest rating":

        filtered_reviews = filtered_reviews.sort_values(
            "rating",
            ascending=True
        )

    elif sort_option == "Highest rating":

        filtered_reviews = filtered_reviews.sort_values(
            "rating",
            ascending=False
        )

    elif sort_option == "Most recent":

        filtered_reviews = filtered_reviews.sort_values(
            "review_date",
            ascending=False
        )

    elif sort_option == "Most helpful":

        filtered_reviews = filtered_reviews.sort_values(
            "helpful_vote",
            ascending=False
        )

# --------------------------------------------------------
# PREVIEW — MAXIMUM 20 REVIEWS
# --------------------------------------------------------

st.caption(
    "Showing up to 20 matching reviews. "
    "Use the sort option to explore different feedback."
)

review_table = filtered_reviews[
    [
        "rating",
        "store",
        "product_short",
        "review",
        "sentiment"
    ]
].head(20).copy()


# Convert sentiment to colored dots
review_table["sentiment"] = review_table["sentiment"].map({
    "Positive": "         🟢",
    "Neutral": "         🟡",
    "Negative": "         🔴"
})

# Hide rating from displayed table
review_table = review_table.drop(
    columns=["rating"]
)

review_table.columns = [
    "Seller",
    "Product",
    "Review",
    "Sentiment"
]

st.dataframe(
    review_table.style
        .set_properties(
            subset=["Sentiment"],
            **{
                "text-align": "center",
                "font-size": "16px"
            }
        ),
    use_container_width=True,
    hide_index=True,
    height=500
)

# --------------------------------------------------------
# DOWNLOAD ALL FILTERED REVIEWS
# --------------------------------------------------------

csv_data = filtered_reviews.to_csv(
    index=False
)

st.download_button(
    label="⬇ Download all matching reviews",
    data=csv_data,
    file_name="filtered_customer_reviews.csv",
    mime="text/csv"
)