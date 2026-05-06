import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="ESPORTS ANALYTICS",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# ADVANCED GAMING UI
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=Poppins:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* MAIN APP */

.stApp {
    background:
    linear-gradient(rgba(5,8,22,0.90), rgba(5,8,22,0.95)),
    url("https://images.unsplash.com/photo-1542751371-adc38448a05e?q=80&w=2070&auto=format&fit=crop");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    color: white;
}

/* SIDEBAR */

[data-testid="stSidebar"] {
    background: rgba(10,15,31,0.92);
    backdrop-filter: blur(14px);
    border-right: 1px solid rgba(140,255,0,0.15);
}

/* HEADINGS */

h1, h2, h3 {
    font-family: 'Orbitron', sans-serif;
    color: white !important;
}

/* KPI CARDS */

div[data-testid="metric-container"] {
    background: rgba(17,24,39,0.72);
    border: 1px solid rgba(140,255,0,0.15);
    padding: 18px;
    border-radius: 18px;
    backdrop-filter: blur(12px);
    box-shadow: 0px 0px 18px rgba(140,255,0,0.08);
    transition: 0.3s ease-in-out;
}

div[data-testid="metric-container"]:hover {
    transform: translateY(-4px);
    box-shadow: 0px 0px 22px rgba(140,255,0,0.18);
}

/* CHART CONTAINER */

.plot-container {
    border-radius: 20px;
    overflow: hidden;
}

/* INSIGHT BOX */

.stAlert {
    background: rgba(17,24,39,0.80) !important;
    border: 1px solid rgba(140,255,0,0.20) !important;
    border-radius: 16px;
    padding: 20px !important;
    color: white !important;
    line-height: 2 !important;
    font-size: 18px !important;
}

/* REMOVE STREAMLIT TOP GAP */

.block-container {
    padding-top: 1rem;
}

/* SCROLLBAR */

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-thumb {
    background: #8cff00;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================

st.title("🎮 GAMING ANALYTICS DASHBOARD")
st.markdown(
    "### Competitive Gaming Intelligence • Match Analytics • Tournament Insights • Revenue Performance"
)

# =========================================================
# SAMPLE DATA
# =========================================================

np.random.seed(42)

n = 1000

games = [
    "Valorant",
    "PUBG",
    "Free Fire",
    "Call of Duty",
    "CS GO"
]

cities = [
    "Chennai",
    "Bangalore",
    "Mumbai",
    "Delhi",
    "Hyderabad"
]

devices = [
    "PC",
    "Console",
    "Mobile",
    "Gaming Laptop"
]

plans = [
    "Free",
    "Pro",
    "Elite"
]

teams = [
    "Phoenix",
    "Lions",
    "Cobra",
    "Titans",
    "Shadow"
]

payment_modes = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "PayPal"
]

date_range = pd.date_range(
    start="2025-01-01",
    end="2026-05-01",
    periods=n
)

df = pd.DataFrame({
    "User_ID": range(1, n + 1),
    "Date": date_range,
    "City": np.random.choice(cities, n),
    "Game": np.random.choice(games, n),
    "Device": np.random.choice(devices, n),
    "Subscription": np.random.choice(plans, n, p=[0.55, 0.30, 0.15]),
    "Matches_Played": np.random.randint(5, 120, n),
    "Wins": np.random.randint(0, 95, n),
    "Tournament_Joined": np.random.randint(0, 15, n),
    "Hours_Streamed": np.random.randint(1, 150, n),
    "Revenue": np.random.randint(500, 20000, n),
    "Favorite_Team": np.random.choice(teams, n),
    "Payment_Mode": np.random.choice(payment_modes, n),
    "Satisfaction": np.random.randint(2, 6, n)
})

# =========================================================
# DERIVED METRICS
# =========================================================

df["Win_Rate"] = (df["Wins"] / df["Matches_Played"]) * 100
df["Active_User"] = np.where(df["Matches_Played"] > 40, 1, 0)
df["Paid_User"] = np.where(df["Revenue"] > 0, 1, 0)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🎯 Dashboard Filters")

selected_game = st.sidebar.multiselect(
    "Select Game",
    df["Game"].unique(),
    default=df["Game"].unique()
)

selected_city = st.sidebar.multiselect(
    "Select City",
    df["City"].unique(),
    default=df["City"].unique()
)

selected_plan = st.sidebar.multiselect(
    "Select Subscription",
    df["Subscription"].unique(),
    default=df["Subscription"].unique()
)

filtered_df = df[
    (df["Game"].isin(selected_game)) &
    (df["City"].isin(selected_city)) &
    (df["Subscription"].isin(selected_plan))
]

# =========================================================
# KPI SECTION
# =========================================================

total_users = filtered_df["User_ID"].nunique()
active_users = filtered_df["Active_User"].sum()
total_matches = filtered_df["Matches_Played"].sum()
total_revenue = filtered_df["Revenue"].sum()
avg_win_rate = filtered_df["Win_Rate"].mean()
tournaments = filtered_df["Tournament_Joined"].sum()
stream_hours = filtered_df["Hours_Streamed"].sum()
paid_users = filtered_df["Paid_User"].sum()

engagement_rate = (active_users / total_users) * 100

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("👥 Registered Players", f"{total_users:,}")

with col2:
    st.metric("🔥 Active Gamers", f"{active_users:,}")

with col3:
    st.metric("🎮 Matches Played", f"{total_matches:,}")

with col4:
    st.metric("💰 Platform Revenue", f"₹ {total_revenue:,.0f}")

col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric("🏆 Avg Win Rate", f"{avg_win_rate:.1f}%")

with col6:
    st.metric("🏟 Tournament Entries", f"{tournaments:,}")

with col7:
    st.metric("📡 Streaming Hours", f"{stream_hours:,}")

with col8:
    st.metric("💳 Premium Users", f"{paid_users:,}")

# =========================================================
# REVENUE TREND
# =========================================================

st.subheader("📈 Monthly Revenue Growth")

monthly_rev = filtered_df.groupby(
    filtered_df["Date"].dt.strftime("%b %Y")
)["Revenue"].sum().reset_index()

fig1 = px.area(
    monthly_rev,
    x="Date",
    y="Revenue",
    template="plotly_dark"
)

fig1.update_traces(line=dict(width=4))

fig1.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    height=420
)

st.plotly_chart(fig1, use_container_width=True)

# =========================================================
# GAME ANALYTICS
# =========================================================

col9, col10 = st.columns(2)

with col9:

    st.subheader("🎯 Most Played Games")

    game_pop = filtered_df.groupby(
        "Game"
    )["Matches_Played"].sum().reset_index()

    fig2 = px.bar(
        game_pop,
        x="Game",
        y="Matches_Played",
        color="Matches_Played",
        template="plotly_dark",
        text_auto=True
    )

    fig2.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=420
    )

    st.plotly_chart(fig2, use_container_width=True)

with col10:

    st.subheader("🏆 Favorite Esports Teams")

    team_pop = filtered_df["Favorite_Team"].value_counts().reset_index()
    team_pop.columns = ["Favorite_Team", "Count"]

    fig3 = px.pie(
        team_pop,
        names="Favorite_Team",
        values="Count",
        hole=0.55,
        template="plotly_dark"
    )

    fig3.update_traces(
        textposition='inside',
        textinfo='percent+label'
    )

    fig3.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=420
    )

    st.plotly_chart(fig3, use_container_width=True)

# =========================================================
# DEVICE & CITY
# =========================================================

col11, col12 = st.columns(2)

with col11:

    st.subheader("🌍 City-wise Revenue")

    city_perf = filtered_df.groupby(
        "City"
    )["Revenue"].sum().reset_index()

    fig4 = px.bar(
        city_perf,
        x="City",
        y="Revenue",
        color="Revenue",
        template="plotly_dark",
        text_auto=True
    )

    fig4.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=420
    )

    st.plotly_chart(fig4, use_container_width=True)

with col12:

    st.subheader("💻 Gaming Device Distribution")

    device_dist = filtered_df["Device"].value_counts().reset_index()
    device_dist.columns = ["Device", "Count"]

    fig5 = px.pie(
        device_dist,
        names="Device",
        values="Count",
        template="plotly_dark"
    )

    fig5.update_traces(
        textposition='inside',
        textinfo='percent+label'
    )

    fig5.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=420
    )

    st.plotly_chart(fig5, use_container_width=True)

# =========================================================
# SATISFACTION & STREAMING
# =========================================================

col13, col14 = st.columns(2)

with col13:

    st.subheader("⭐ Player Satisfaction")

    satisfaction = filtered_df.groupby(
        "Game"
    )["Satisfaction"].mean().reset_index()

    fig6 = px.bar(
        satisfaction,
        x="Game",
        y="Satisfaction",
        color="Satisfaction",
        template="plotly_dark",
        text_auto=True
    )

    fig6.update_layout(
        yaxis=dict(range=[0,5]),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=420
    )

    st.plotly_chart(fig6, use_container_width=True)

with col14:

    st.subheader("📡 Streaming Activity")

    stream = filtered_df.groupby(
        "Game"
    )["Hours_Streamed"].sum().reset_index()

    fig7 = px.line(
        stream,
        x="Game",
        y="Hours_Streamed",
        markers=True,
        template="plotly_dark"
    )

    fig7.update_traces(line=dict(width=5))

    fig7.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=420
    )

    st.plotly_chart(fig7, use_container_width=True)

# =========================================================
# HEATMAP
# =========================================================

st.subheader("🔥 Win Rate by Subscription")

heatmap_data = filtered_df.pivot_table(
    values="Win_Rate",
    index="Game",
    columns="Subscription",
    aggfunc="mean"
)

fig8 = px.imshow(
    heatmap_data,
    text_auto=True,
    aspect="auto",
    template="plotly_dark"
)

fig8.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    height=500
)

st.plotly_chart(fig8, use_container_width=True)

# =========================================================
# ADVANCED PROFESSIONAL VISUAL
# =========================================================

st.subheader("🎮 Match Engagement Analysis")

engagement = filtered_df.groupby(
    "Game"
).agg({
    "Matches_Played":"mean",
    "Wins":"mean",
    "Hours_Streamed":"mean"
}).reset_index()

fig9 = go.Figure()

fig9.add_trace(go.Scatterpolar(
    r=engagement["Matches_Played"],
    theta=engagement["Game"],
    fill='toself',
    name='Matches'
))

fig9.add_trace(go.Scatterpolar(
    r=engagement["Wins"],
    theta=engagement["Game"],
    fill='toself',
    name='Wins'
))

fig9.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    polar=dict(
        bgcolor="rgba(0,0,0,0)"
    ),
    height=550
)

st.plotly_chart(fig9, use_container_width=True)

# =========================================================
# BUSINESS INSIGHTS
# =========================================================

st.subheader("📌 BUSINESS Insights")

top_game = game_pop.sort_values(
    by="Matches_Played",
    ascending=False
).iloc[0]["Game"]

top_city = city_perf.sort_values(
    by="Revenue",
    ascending=False
).iloc[0]["City"]

top_team = team_pop.iloc[0]["Favorite_Team"]

st.success(f"""
🎮 {top_game} dominates the platform with the highest player engagement and tournament activity, making it the leading competitive title on Stackly.

🏆 {top_team} has emerged as the most followed esports team, indicating strong fan engagement and community participation.

🌍 {top_city} contributes the highest platform revenue, showing strong adoption of competitive gaming and premium memberships.

🔥 Active gamer engagement reached {engagement_rate:.2f}%, reflecting consistent player participation across ranked matches, multiplayer sessions, and esports tournaments.

💳 Premium and Elite memberships continue to drive monetization through tournament access, exclusive gaming rewards, and premium competitive events.

📡 Streaming activity between January 2025 and May 2026 shows consistent growth, highlighting rising player interaction and content creation across the platform.

🎯 Mobile and PC gaming remain the dominant access platforms, while Gaming Laptop users demonstrate higher average gameplay hours and competitive participation.

⭐ Player satisfaction scores remain high across PUBG, Valorant, Free Fire, and Call of Duty, indicating strong gameplay experience and esports ecosystem quality.
""")

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown(
    """
    <center>
    <h4 style='color:#8cff00; font-family:Orbitron;'>
    ESPORTS ANALYTICS DASHBOARD
    </h4>
    </center>
    """,
    unsafe_allow_html=True
)
