import streamlit as st


def show_navigation(active_page):

    # --------------------------------------------------------
    # ACTIVE PAGE BORDER COLORS
    # --------------------------------------------------------

    product_border = (
        "#FF9900" if active_page == "product" else "#37475A"
    )

    voice_border = (
        "#FF9900" if active_page == "voice" else "#37475A"
    )

    risk_border = (
        "#FF9900" if active_page == "risk" else "#37475A"
    )

    # --------------------------------------------------------
    # NAVIGATION
    # --------------------------------------------------------

    st.html(f"""
    <div style="
        text-align: center;
        margin-top: 5px;
        margin-bottom: 30px;
    ">

        <!-- Main title -->
        <div style="
            font-size: 46px;
            font-weight: 700;
            color: white;
            margin-bottom: 14px;
        ">
            🛒 Amazon Review Intelligence Dashboard
        </div>

        <!-- Description -->
        <div style="
            font-size: 18px;
            font-weight: 500;
            color: #D5DBDB;
            margin-bottom: 20px;
        ">
            Explore product performance, customer feedback, and review risk 
            across Amazon Sports & Outdoors products.
        </div>

        <!-- Navigation cards -->
        <div style="
            display: flex;
            justify-content: center;
            gap: 14px;
            flex-wrap: wrap;
        ">

            <!-- Product Analytics -->
            <a href="/" style="
                text-decoration: none;
            ">
                <div style="
                    background-color: #1B2530;
                    border: 1px solid {product_border};
                    border-radius: 8px;
                    padding: 10px 18px;
                    color: white;
                    font-size: 14px;
                    font-weight: 600;
                    cursor: pointer;
                ">
                    📦 Product Analytics
                </div>
            </a>

            <!-- Voice of Customer -->
            <a href="/Voice_of_Customer" style="
                text-decoration: none;
            ">
                <div style="
                    background-color: #1B2530;
                    border: 1px solid {voice_border};
                    border-radius: 8px;
                    padding: 10px 18px;
                    color: white;
                    font-size: 14px;
                    font-weight: 600;
                    cursor: pointer;
                ">
                    💬 Voice of Customer
                </div>
            </a>

            <!-- Customer Risk Management -->
            <a href="/Customer_Risk_Reputation" style="
                text-decoration: none;
            ">
                <div style="
                    background-color: #1B2530;
                    border: 1px solid {risk_border};
                    border-radius: 8px;
                    padding: 10px 18px;
                    color: white;
                    font-size: 14px;
                    font-weight: 600;
                    cursor: pointer;
                ">
                    🚨 Reputation Risk Monitoring
                </div>
            </a>

        </div>

    </div>
    """)