import streamlit as st 
import requests 

st.title("Live currency converter")
amount = st.number_input("Enter the amount in INR", min_value=1)
target_curr = st.selectbox("Conver to : ", ["USD" , "EUR", "GBP", "JPY"])

if st.button("Convert"):
  url = "https://api.exchangerate-api.com/v4/latest/INR"
  res = requests.get(url)

  if res.status_code == 200:
    ans = res.json()["rates"][target_curr]*amount 
    st.success(f"{amount} INK = {ans:.2f} {target_curr}")
  else:
    st.error("Failed to convert! Try again...")
