import streamlit as st
import pandas as pd
import plotly.express as px
from navigation import show_navigation

AMAZON_ORANGE = "#FF9900"
AMAZON_DARK = "#232F3E"
AMAZON_LIGHT = "#E7E9EC"

st.set_page_config(
    page_title="Amazon Review Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)

show_navigation("product")

st.markdown("""
<style>

/* Dropdown menu */
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

/* Selected option */
div[data-baseweb="popover"] li[aria-selected="true"] {
    background-color: #B0B8C2 !important;
    color: #131A22 !important;
}
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

/* Top header */
.amazon-header {
    background-color: #131A22;
    padding: 18px 30px;
    margin: -60px -60px 0 -60px;
}

/* Navigation */
.amazon-nav {
    background-color: #131A22;
    color: white;
    padding: 12px 30px;
    margin: 0 -60px 30px -60px;
    font-size: 18px;
}

</style>
""", unsafe_allow_html=True)


st.markdown("""
<style>
[data-testid="stSidebar"] {
    display: none;
}

[data-testid="collapsedControl"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

import pandas as pd

# Load processed dataset
df_dashboard = pd.read_csv("amazon_reviews_dashboard2.csv")
df_dashboard["review_date"] = pd.to_datetime(df_dashboard["review_date"])

# ============================================================
# FILTERS
# ============================================================

# ------------------------------------------------------------
# Filters
# ------------------------------------------------------------

filter_col1, filter_col2, filter_col3, filter_spacer = st.columns([1.2, 0.8, 0.8, 1.2])

with filter_col1:
    selected_product_group = st.selectbox(
        "Product Group",
        ["All Product Groups"]
        + sorted(
            df_dashboard["product_group"]
            .dropna()
            .unique()
            .tolist()
        )
    )

with filter_col2:
    selected_purchase = st.selectbox(
        "Purchase Type",
        [
            "All Purchase Types",
            "Verified Purchase",
            "Non-Verified Purchase"
        ]
    )

with filter_col3:
    selected_month = st.selectbox(
        "Month",
        ["All Months"] + list(range(1, 13)),
        format_func=lambda x:
            "All Months"
            if x == "All Months"
            else pd.Timestamp(2024, x, 1).strftime("%B")
    )
# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df_dashboard.copy()

# Product Group
if selected_product_group != "All Product Groups":
    filtered_df = filtered_df[
        filtered_df["product_group"] == selected_product_group
    ]

if selected_purchase == "Verified Purchase":
    filtered_df = filtered_df[
        filtered_df["verified_purchase"] == True
    ]

elif selected_purchase == "Non-Verified Purchase":
    filtered_df = filtered_df[
        filtered_df["verified_purchase"] == False
    ]

if selected_month != "All Months":
    filtered_df = filtered_df[
        filtered_df["review_date"].dt.month == selected_month
    ]

# Reviews per calendar month
reviews_time = (
    filtered_df
    .assign(month=filtered_df["review_date"].dt.to_period("M"))
    .groupby("month")
    .size()
    .reset_index(name="reviews")
)

reviews_time["month"] = reviews_time["month"].dt.to_timestamp()

# ============================================================
# PAGE 1 — DATASET OVERVIEW
# ============================================================

st.header("Review Data Overview")

# ------------------------------------------------------------
# Basic dataset information
# ------------------------------------------------------------

total_reviews = len(filtered_df)

total_products = filtered_df["parent_asin"].nunique()

total_brands = filtered_df["store"].nunique()

total_product_groups = filtered_df["product_group"].nunique()

total_reviewers = filtered_df["user_id"].nunique()


# ------------------------------------------------------------
# KPI cards
# ------------------------------------------------------------

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Reviews",
    f"{total_reviews:,}"
)

col2.metric(
    "Products",
    f"{total_products:,}"
)

col3.metric(
    "Brands",
    f"{total_brands:,}"
)

col4.metric(
    "Product Groups",
    f"{total_product_groups:,}"
)

col5.metric(
    "Reviewers",
    f"{total_reviewers:,}"
)


# ============================================================
# RATING DISTRIBUTION
# ============================================================

rating_distribution = (
    filtered_df["rating"]
    .value_counts()
    .sort_index()
    .reset_index()
)

rating_distribution.columns = [
    "rating",
    "reviews"
]

rating_distribution["rating"] = rating_distribution["rating"].astype(str)

# ============================================================
# REVIEWS PER CALENDAR MONTH BY RATING GROUP
# ============================================================

# All reviews
all_reviews = (
    filtered_df
    .assign(month=filtered_df["review_date"].dt.to_period("M"))
    .groupby("month")
    .size()
    .reset_index(name="reviews")
)
all_reviews["rating_group"] = "All Reviews"

# Positive ratings (4★–5★)
positive_reviews = (
    filtered_df[filtered_df["rating"].isin([4, 5])]
    .assign(month=lambda df: df["review_date"].dt.to_period("M"))
    .groupby("month")
    .size()
    .reset_index(name="reviews")
)
positive_reviews["rating_group"] = "Positive Ratings (4–5★)"

# Negative ratings (1★–2★)
negative_reviews = (
    filtered_df[filtered_df["rating"].isin([1, 2])]
    .assign(month=lambda df: df["review_date"].dt.to_period("M"))
    .groupby("month")
    .size()
    .reset_index(name="reviews")
)
negative_reviews["rating_group"] = "Negative Ratings (1–2★)"

# Combine
reviews_time = pd.concat(
    [all_reviews, positive_reviews, negative_reviews],
    ignore_index=True
)

reviews_time["month"] = reviews_time["month"].dt.to_timestamp()

# ============================================================
# TOP PRODUCTS
# ============================================================

product_ratings = (
    filtered_df
    .groupby(["parent_asin", "product_title"])
    .agg(
        avg_rating=("rating", "mean"),
        reviews=("rating", "size")
    )
    .reset_index()
)

# Minimum 20 reviews per product
product_ratings = product_ratings[
    product_ratings["reviews"] >= 30
]

# Top 5 best-rated products
top_products = (
    product_ratings
    .sort_values("avg_rating", ascending=False)
    .head(5)
    .copy()
)

top_products["product_display"] = (
    top_products["product_title"]
    .apply(lambda x: x[:50] + "..." if len(x) > 50 else x)
)


# ============================================================
# TOP 5 BEST-RATED BRANDS
# ============================================================

brand_ratings = (
    filtered_df
    .groupby("store")
    .agg(
        avg_rating=("rating", "mean"),
        reviews=("rating", "size")
    )
    .reset_index()
)

brand_ratings = brand_ratings[
    brand_ratings["reviews"] >= 100
]

top_brands = (
    brand_ratings
    .sort_values("avg_rating", ascending=False)
    .head(5)
    .copy()
)


# ============================================================
# VERIFIED PURCHASE DISTRIBUTION
# ============================================================

verified_distribution = (
    filtered_df["verified_purchase"]
    .value_counts()
    .reset_index()
)

verified_distribution.columns = [
    "verified_purchase",
    "reviews"
]

verified_distribution["purchase_type"] = (
    verified_distribution["verified_purchase"]
    .map({
        True: "Verified Purchase",
        False: "Non-Verified Purchase"
    })
)

verified_distribution["percentage"] = (
    verified_distribution["reviews"] / total_reviews * 100
)


# ============================================================
# LOWEST-RATED PRODUCTS
# ============================================================

product_ratings = (
    filtered_df
    .groupby(["parent_asin", "product_title"])
    .agg(
        avg_rating=("rating", "mean"),
        reviews=("rating", "size")
    )
    .reset_index()
)

# Minimum 30 reviews per product
product_ratings = product_ratings[
    product_ratings["reviews"] >= 30
]

# Top 5 lowest-rated products
bottom_products = (
    product_ratings
    .sort_values("avg_rating", ascending=True)
    .head(5)
    .copy()
)

bottom_products["product_display"] = (
    bottom_products["product_title"]
    .apply(lambda x: x[:50] + "..." if len(x) > 50 else x)
)

# ============================================================
# LOWEST-RATED BRANDS
# ============================================================

brand_ratings = (
    filtered_df
    .groupby("store")
    .agg(
        avg_rating=("rating", "mean"),
        reviews=("rating", "size")
    )
    .reset_index()
)

# Minimum 100 reviews per brand
brand_ratings = brand_ratings[
    brand_ratings["reviews"] >= 100
]

bottom_brands = (
    brand_ratings
    .sort_values("avg_rating", ascending=True)
    .head(5)
    .copy()
)
# ---------------------------------------------------------------------------------------------------------------

# ============================================================
# CHARTS
# ============================================================

# ------------------------------------------------------------
# Rating distribution + Reviews over time
# ------------------------------------------------------------

rating_distribution["percentage"] = (
    rating_distribution["reviews"]
    / rating_distribution["reviews"].sum()
    * 100
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Rating Distribution")

    rating_distribution["rating"] = rating_distribution["rating"].astype(str)
    

    fig_rating = px.bar(
        rating_distribution,
        x="rating",
        y="reviews",
        text="percentage",
        labels={
            "rating": "Rating",
            "reviews": "Reviews"
        }
)

    fig_rating.update_traces(
        marker_color=[
            "#7A2E2E",  # 1
            "#A14A2A",  # 2
            "#C46A1A",  # 3
            "#E68A00",  # 4
            "#FF9900"   # 5
        ],
        texttemplate="%{text:.1f}%",
        textposition="outside",
        hovertemplate=(
            "<b>%{x}★</b><br>"
            "%{y:,} reviews<br>"
            "%{text:.1f}%"
            "<extra></extra>"
        )
    )

    fig_rating.update_layout(
        xaxis=dict(dtick=1),
        showlegend=False
    )

    st.plotly_chart(
        fig_rating,
        use_container_width=True
    )


with col2:
    st.subheader("Reviews Over Time")

    fig_time = px.line(
        reviews_time,
        x="month",
        y="reviews",
        color="rating_group",
        markers=True,
        color_discrete_map={
            "All Reviews": "#B0B8C2",
            "Positive Ratings (4–5★)": "#FF9900",
            "Negative Ratings (1–2★)": "#8D3C2C"
        },
        labels={
            "month": "Month",
            "reviews": "Number of Reviews",
            "rating_group": ""
        }
    )

    fig_time.for_each_trace(
        lambda trace: trace.update(
            line=dict(
                width=4 if trace.name == "All Reviews" else 2,
                dash="dash" if trace.name != "All Reviews" else "solid"
            ),
            marker=dict(
                size=7 if trace.name == "All Reviews" else 0
            ),
            mode="lines+markers" if trace.name == "All Reviews" else "lines"
        )
    )
    
    fig_time.update_traces(
        hovertemplate=(
            "<b>%{x|%B %Y}</b><br>"
            "%{fullData.name}: %{y:,}<extra></extra>"
        )
    )
    
    fig_time.update_xaxes(
        tickformat="%b %Y"
    )
    
    fig_time.update_layout(
        xaxis_title="Month",
        yaxis_title="Number of Reviews",
        legend_title=None,
        hovermode="x unified"
    )
    
    st.plotly_chart(
        fig_time,
        use_container_width=True
    )

# ------------------------------------------------------------
# Top products + Top brands
# ------------------------------------------------------------

col1, col2 = st.columns(2)

with col2:
    st.subheader("Top 5 Best-Rated Products")

    html = """
    <div style="
        background-color: #0F141A;
        border-radius: 12px;
        padding: 10px 20px;
        height: 500px;
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
    ">
        
    <div style="
        display: grid;
        grid-template-columns: 50px 1fr 180px 120px;
        padding: 15px 10px;
        color: white;
        font-weight: 700;
        border-bottom: 1px solid #2A3441;
    ">
        <div>#</div>
        <div>Product</div>
        <div>Average Rating</div>
        <div style="text-align:right;">Reviews</div>
    </div>
    """
    
    for i, row in top_products.reset_index(drop=True).iterrows():
    
        rating = row["avg_rating"]
        reviews = row["reviews"]
        product = row["product_display"]
    
        html += f"""
        <div style="
            display: grid;
            grid-template-columns: 50px 1fr 160px 100px;
            align-items: center;
            min-height: 75px;
            padding: 10px;
            border-bottom: 1px solid #2A3441;
            color: white;
        ">
    
            <div style="
                background-color: {AMAZON_ORANGE};
                color: #131A22;
                width: 32px;
                height: 32px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 700;
            ">
                {i + 1}
            </div>
    
            <div style="
                font-size: 15px;
                font-weight: 600;
                padding-right: 20px;
            ">
                {product}
            </div>
    
            <div>
                <span style="
                    color: {AMAZON_ORANGE};
                    font-size: 18px;
                    font-weight: 700;
                ">
                    ★ {rating:.2f}
                </span>
    
                <div style="
                    margin-top: 6px;
                    width: 130px;
                    height: 8px;
                    background-color: #37475A;
                    border-radius: 5px;
                ">
                    <div style="
                        width: {rating / 5 * 100:.1f}%;
                        height: 8px;
                        background-color: {AMAZON_ORANGE};
                        border-radius: 5px;
                    "></div>
                </div>
            </div>
    
            <div style="
                text-align: right;
                font-size: 16px;
            ">
                {reviews:,}
            </div>
    
        </div>
        """
    
    html += """
        <div style="
            color: #A9B0B8;
            font-size: 14px;
            margin-top: auto;
            padding: 0 10px 4px 10px;
        ">
            Ranked by average rating. Minimum 30 reviews per product.
        </div>
    </div>
    """

    st.html(html)


with col1:

    st.subheader("Top 5 Lowest-Rated Products")

    html = """
    <div style="
        background-color: #0F141A;
        border-radius: 12px;
        padding: 10px 20px;
        height: 500px;
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
    ">

    <div style="
        display: grid;
        grid-template-columns: 50px 1fr 180px 120px;
        padding: 15px 10px;
        color: white;
        font-weight: 700;
        border-bottom: 1px solid #2A3441;
    ">
        <div>#</div>
        <div>Product</div>
        <div>Average Rating</div>
        <div style="text-align:right;">Reviews</div>
    </div>
    """

    for i, row in bottom_products.reset_index(drop=True).iterrows():

        rating = row["avg_rating"]
        reviews = row["reviews"]
        product = row["product_display"]

        html += f"""
        <div style="
            display: grid;
            grid-template-columns: 50px 1fr 160px 100px;
            align-items: center;
            min-height: 75px;
            padding: 10px;
            border-bottom: 1px solid #2A3441;
            color: white;
        ">

            <div style="
                background-color: #7A2E2E;
                color: white;
                width: 32px;
                height: 32px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 700;
            ">
                {i + 1}
            </div>

            <div style="
                font-size: 15px;
                font-weight: 600;
                padding-right: 20px;
            ">
                {product}
            </div>

            <div>
                <span style="
                    color: #7A2E2E;
                    font-size: 18px;
                    font-weight: 700;
                ">
                    ★ {rating:.2f}
                </span>

                <div style="
                    margin-top: 6px;
                    width: 130px;
                    height: 8px;
                    background-color: #37475A;
                    border-radius: 5px;
                ">
                    <div style="
                        width: {rating / 5 * 100:.1f}%;
                        height: 8px;
                        background-color: #7A2E2E;
                        border-radius: 5px;
                    "></div>
                </div>
            </div>

            <div style="
                text-align: right;
                font-size: 16px;
            ">
                {reviews:,}
            </div>

        </div>
        """

    html += """
        <div style="
            color: #A9B0B8;
            font-size: 14px;
            margin-top: auto;
            padding: 0 10px 4px 10px;
        ">
            Ranked by average rating. Minimum 30 reviews per product.
        </div>
    </div>
    """

    st.html(html)

# ------------------------------------------------------------
# Verified vs. not verified + Avg. rating per prod. group
# ------------------------------------------------------------

col1, col2 = st.columns(2)

with col2:
    
    st.subheader("Top 5 Best-Rated Brands")

    html = """
    <div style="
        background-color: #0F141A;
        border-radius: 12px;
        padding: 10px 20px;
        height: 500px;
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
    ">
    
    <div style="
        display: grid;
        grid-template-columns: 50px 1fr 180px 120px;
        padding: 15px 10px;
        color: white;
        font-weight: 700;
        border-bottom: 1px solid #2A3441;
    ">
        <div>#</div>
        <div>Brand</div>
        <div>Average Rating</div>
        <div style="text-align:right;">Reviews</div>
    </div>
    """
    
    for i, row in top_brands.reset_index(drop=True).iterrows():
    
        rating = row["avg_rating"]
        reviews = row["reviews"]
        brand = row["store"]
    
        html += f"""
        <div style="
            display: grid;
            grid-template-columns: 50px 1fr 180px 120px;
            align-items: center;
            min-height: 75px;
            padding: 10px;
            border-bottom: 1px solid #2A3441;
            color: white;
        ">
    
            <div style="
                background-color: {AMAZON_ORANGE};
                color: #131A22;
                width: 32px;
                height: 32px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 700;
            ">
                {i + 1}
            </div>
    
            <div style="
                font-size: 16px;
                font-weight: 600;
                padding-right: 20px;
            ">
                {brand}
            </div>
    
            <div>
                <span style="
                    color: {AMAZON_ORANGE};
                    font-size: 18px;
                    font-weight: 700;
                ">
                    ★ {rating:.2f}
                </span>
    
                <div style="
                    margin-top: 6px;
                    width: 130px;
                    height: 8px;
                    background-color: #37475A;
                    border-radius: 5px;
                ">
                    <div style="
                        width: {rating / 5 * 100:.1f}%;
                        height: 8px;
                        background-color: {AMAZON_ORANGE};
                        border-radius: 5px;
                    "></div>
                </div>
            </div>
    
            <div style="
                text-align: right;
                font-size: 16px;
            ">
                {reviews:,}
            </div>
    
        </div>
        """
    
    html += """
        <div style="
            color: #A9B0B8;
            font-size: 14px;
            margin-top: auto;
            padding: 0 10px 4px 10px;
        ">
            Ranked by average rating. Minimum 100 reviews per brand.
        </div>
    </div>
    """

    st.html(html)    
with col1:

# ============================================================
# Bottom 5 Brands
# ============================================================
    
    st.subheader("Top 5 Lowest-Rated Brands")

    html = """
    <div style="
        background-color: #0F141A;
        border-radius: 12px;
        padding: 10px 20px;
        height: 500px;
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
    ">

    <div style="
        display: grid;
        grid-template-columns: 50px 1fr 180px 120px;
        padding: 15px 10px;
        color: white;
        font-weight: 700;
        border-bottom: 1px solid #2A3441;
    ">
        <div>#</div>
        <div>Brand</div>
        <div>Average Rating</div>
        <div style="text-align:right;">Reviews</div>
    </div>
    """

    for i, row in bottom_brands.reset_index(drop=True).iterrows():

        rating = row["avg_rating"]
        reviews = row["reviews"]
        brand = row["store"]

        html += f"""
        <div style="
            display: grid;
            grid-template-columns: 50px 1fr 180px 120px;
            align-items: center;
            min-height: 75px;
            padding: 10px;
            border-bottom: 1px solid #2A3441;
            color: white;
        ">

            <div style="
                background-color: #7A2E2E;
                color: white;
                width: 32px;
                height: 32px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 700;
            ">
                {i + 1}
            </div>

            <div style="
                font-size: 16px;
                font-weight: 600;
                padding-right: 20px;
            ">
                {brand}
            </div>

            <div>
                <span style="
                    color: #7A2E2E;
                    font-size: 18px;
                    font-weight: 700;
                ">
                    ★ {rating:.2f}
                </span>

                <div style="
                    margin-top: 6px;
                    width: 130px;
                    height: 8px;
                    background-color: #37475A;
                    border-radius: 5px;
                ">
                    <div style="
                        width: {rating / 5 * 100:.1f}%;
                        height: 8px;
                        background-color: #7A2E2E;
                        border-radius: 5px;
                    "></div>
                </div>
            </div>

            <div style="
                text-align: right;
                font-size: 16px;
            ">
                {reviews:,}
            </div>

        </div>
        """

    html += """
        <div style="
            color: #A9B0B8;
            font-size: 14px;
            margin-top: auto;
            padding: 0 10px 4px 10px;
        ">
            Ranked by average rating. Minimum 100 reviews per brand.
        </div>
    </div>
    """

    st.html(html)
    