import streamlit as st 
import datetime

st.title("age calculator")
dob = st.date_input("Enter your date of birth", min_value=datetime.date(1900, 1, 1),)
submitted = st.button("calculate")

if submitted:
  age = datetime.date.today().year - dob.year
  st.success(f"Your age is {age}")
  
