import streamlit as st
import pandas as pd

# Load player wallet data
df = pd.read_csv("wallet.csv")

st.title("⚽ Turf Wallet Manager")

# Input: Today's players
players_today = st.multiselect("Select players who played today", df["Name"].tolist())

# Input: Total turf cost
total_cost = st.number_input("Total turf rent today", min_value=0, value=3500)

# Deduct and update wallets
if st.button("Deduct and Update Wallets"):
    if players_today:
        cost_per_player = total_cost / len(players_today)
        already_deducted = []

        for player in players_today:
            current_balance = df.loc[df["Name"] == player, "Wallet"].values[0]
            if current_balance >= cost_per_player:
                df.loc[df["Name"] == player, "Wallet"] -= cost_per_player
                st.success(f"{player} charged {cost_per_player:.2f} Taka. New balance: {df.loc[df['Name'] == player, 'Wallet'].values[0]:.2f}")
            else:
                already_deducted.append(player)

        if already_deducted:
            st.warning(f"Not enough balance or already deducted for: {', '.join(already_deducted)}")

        df.to_csv("wallet.csv", index=False)
    else:
        st.warning("No players selected.")

st.markdown("---")

# Add Money to Wallet
st.subheader("💸 Add Money to Player Wallet")
add_player = st.selectbox("Select player to add money", df["Name"].tolist())
add_amount = st.number_input("Amount to add", min_value=0.0, value=0.0, step=100.0)

if st.button("Add Money"):
    df.loc[df["Name"] == add_player, "Wallet"] += add_amount
    st.success(f"{add_amount:.2f} Taka added to {add_player}'s wallet.")
    df.to_csv("wallet.csv", index=False)

st.markdown("---")

# Manual Balance Override
st.subheader("✏️ Manually Update Wallet")
manual_player = st.selectbox("Select player to update wallet manually", df["Name"].tolist())
new_balance = st.number_input("New wallet balance", min_value=0.0, value=0.0, step=100.0)

if st.button("Update Wallet Manually"):
    df.loc[df["Name"] == manual_player, "Wallet"] = new_balance
    st.success(f"{manual_player}'s wallet updated to {new_balance:.2f} Taka.")
    df.to_csv("wallet.csv", index=False)

st.markdown("---")

# Show wallet table
st.subheader("📋 Current Wallets")
st.dataframe(df)
