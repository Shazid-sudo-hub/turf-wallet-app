import base64
import os
import pandas as pd
import streamlit as st

# ---------------- Page Setup ----------------
st.set_page_config(
    page_title="Turf Wallet Manager",
    page_icon="⚽",
    layout="centered"
)
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

bg_image = get_base64_image("app_bc.jpg")
# ---------------- Custom Design ----------------
st.markdown(f"""
<style>
.stApp {{
    background:
        linear-gradient(rgba(0, 20, 10, 0.78), rgba(0, 20, 10, 0.88)),
        url("data:image/jpg;base64,{bg_image}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    color: white;
}}

.block-container {{
    padding-top: 2rem;
    max-width: 850px;
}}

.main-card {{
    background: rgba(0, 0, 0, 0.62);
    padding: 25px;
    border-radius: 18px;
    border: 1px solid rgba(255, 255, 255, 0.18);
    box-shadow: 0px 8px 25px rgba(0,0,0,0.45);
}}

.title {{
    font-size: 42px;
    font-weight: 800;
    text-align: center;
    margin-bottom: 5px;
}}

.subtitle {{
    text-align: center;
    font-size: 16px;
    color: #d6d6d6;
    margin-bottom: 25px;
}}

.section-title {{
    font-size: 24px;
    font-weight: 700;
    margin-top: 25px;
    margin-bottom: 10px;
}}

.stButton > button {{
    background-color: #12a150;
    color: white;
    border-radius: 10px;
    border: none;
    font-weight: 700;
    padding: 0.6rem 1rem;
}}

.stButton > button:hover {{
    background-color: #0e7f3f;
    color: white;
}}

hr {{
    border: 1px solid rgba(255,255,255,0.15);
}}
</style>
""", unsafe_allow_html=True)

# ---------------- Data Functions ----------------
CSV_FILE = "wallet.csv"

def load_wallet():
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
    else:
        df = pd.DataFrame(columns=["Name", "Wallet"])

    if "Name" not in df.columns:
        df["Name"] = ""

    if "Wallet" not in df.columns:
        df["Wallet"] = 0

    df["Wallet"] = pd.to_numeric(df["Wallet"], errors="coerce").fillna(0)
    return df

def save_wallet(df):
    df.to_csv(CSV_FILE, index=False)

df = load_wallet()

# ---------------- Header ----------------
st.markdown('<div class="main-card">', unsafe_allow_html=True)

st.markdown('<div class="title">⚽ Turf Wallet Manager</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Simple wallet system for daily football turf rent calculation</div>',
    unsafe_allow_html=True
)

# ---------------- Summary ----------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Players", len(df))

with col2:
    st.metric("Total Wallet Balance", f"{df['Wallet'].sum():.2f} Tk")

with col3:
    st.metric("Average Balance", f"{df['Wallet'].mean() if len(df)>0 else 0:.2f} Tk")

st.markdown("---")

# ---------------- Deduct Rent ----------------
st.markdown('<div class="section-title">💸 Deduct Today\'s Turf Rent</div>', unsafe_allow_html=True)

players_today = st.multiselect(
    "Select players who played today",
    df["Name"].tolist()
)

total_cost = st.number_input(
    "Total turf rent today",
    min_value=0.0,
    value=3500.0,
    step=100.0
)

if players_today:
    cost_per_player = total_cost / len(players_today)
    st.info(f"Each selected player will be charged: {cost_per_player:.2f} Tk")

if st.button("Deduct and Update Wallets"):
    if not players_today:
        st.warning("Please select at least one player.")
    else:
        cost_per_player = total_cost / len(players_today)
        already_deducted = []

        for player in players_today:
            current_balance = df.loc[df["Name"] == player, "Wallet"].values[0]

            if current_balance >= cost_per_player:
                df.loc[df["Name"] == player, "Wallet"] = current_balance - cost_per_player
            else:
                already_deducted.append(player)

        save_wallet(df)

        if already_deducted:
            st.warning("Not enough balance for: " + ", ".join(already_deducted))
        else:
            st.success("Wallets updated successfully.")

st.markdown("---")

# ---------------- Add Money ----------------
st.markdown('<div class="section-title">💵 Add Money to Player Wallet</div>', unsafe_allow_html=True)

add_player = st.selectbox(
    "Select player to add money",
    df["Name"].tolist(),
    key="add_player"
)

add_amount = st.number_input(
    "Amount to add",
    min_value=0.0,
    value=200.0,
    step=50.0
)

if st.button("Add Money"):
    df.loc[df["Name"] == add_player, "Wallet"] = df.loc[df["Name"] == add_player, "Wallet"] + add_amount
    save_wallet(df)
    st.success(f"{add_amount:.2f} Tk added to {add_player}'s wallet.")

st.markdown("---")

# ---------------- Manual Update ----------------
st.markdown('<div class="section-title">✏️ Manually Update Wallet</div>', unsafe_allow_html=True)

manual_player = st.selectbox(
    "Select player to update manually",
    df["Name"].tolist(),
    key="manual_player"
)

new_balance = st.number_input(
    "New wallet balance",
    min_value=0.0,
    value=0.0,
    step=50.0
)

if st.button("Update Wallet Manually"):
    df.loc[df["Name"] == manual_player, "Wallet"] = new_balance
    save_wallet(df)
    st.success(f"{manual_player}'s wallet updated to {new_balance:.2f} Tk.")

st.markdown("---")

# ---------------- Add New Player ----------------
st.markdown('<div class="section-title">➕ Add New Player</div>', unsafe_allow_html=True)

new_player_name = st.text_input("Player name")
initial_balance = st.number_input(
    "Initial wallet balance",
    min_value=0.0,
    value=0.0,
    step=50.0
)

if st.button("Add New Player"):
    if new_player_name.strip() == "":
        st.warning("Please enter a player name.")
    elif new_player_name in df["Name"].values:
        st.warning("This player already exists.")
    else:
        new_row = pd.DataFrame({
            "Name": [new_player_name],
            "Wallet": [initial_balance]
        })
        df = pd.concat([df, new_row], ignore_index=True)
        save_wallet(df)
        st.success(f"{new_player_name} added successfully.")

st.markdown("---")

# ---------------- Wallet Table ----------------
st.markdown('<div class="section-title">📋 Current Wallet Balances</div>', unsafe_allow_html=True)

df_display = df.copy()
df_display["Wallet"] = df_display["Wallet"].map(lambda x: f"{x:.2f} Tk")

st.dataframe(df_display, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)
