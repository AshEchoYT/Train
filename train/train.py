import streamlit as st
import pandas as pd
import os

# CSV File to store bookings
CSV_FILE = "bookings.csv"

# List of available trains
TRAINS = {
    "12345": "Chennai Express",
    "67890": "Mumbai Rajdhani",
    "11223": "Kolkata Duronto",
    "44556": "Bangalore Shatabdi"
}

# Function to save booking
def save_booking(name, train_no, date, seat_class, age, gender, meal):
    new_entry = pd.DataFrame([[name, train_no, TRAINS.get(train_no, "Unknown"), date, seat_class, age, gender, meal]], 
                             columns=["Name", "Train Number", "Train Name", "Date", "Class", "Age", "Gender", "Meal Preference"])
    if not os.path.exists(CSV_FILE):
        new_entry.to_csv(CSV_FILE, index=False)
    else:
        new_entry.to_csv(CSV_FILE, mode='a', header=False, index=False)

def main():
    st.set_page_config(page_title="Train Ticket Booking", layout="wide")
    
    st.markdown("""
        <style>
            body { background-color: #f4f7f9; color: #2c3e50; font-family: 'Segoe UI', sans-serif; }
            .stApp { background-color: #ffffff; padding: 25px; border-radius: 12px; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1); }
            .stTitle { color: #2c3e50; font-size: 30px; font-weight: bold; text-align: center; margin-bottom: 20px; }
            .stDataFrame { background-color: #ffffff; border-radius: 12px; padding: 12px; }
            .stButton>button { background-color: #007bff; color: white; border-radius: 6px; padding: 12px; border: none; font-weight: bold; }
            .stButton>button:hover { background-color: #0056b3; }
            .stForm { background-color: #eef1f5; padding: 20px; border-radius: 10px; box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.1); }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("🚆 Train Ticket Booking System")
    
    with st.form("booking_form"):
        name = st.text_input("Enter Your Name:")
        train_no = st.selectbox("Select Train:", options=TRAINS.keys(), format_func=lambda x: f"{x} - {TRAINS[x]}")
        date = st.date_input("Select Date:")
        seat_class = st.selectbox("Choose Class:", ["Economy", "Business", "First Class"])
        age = st.number_input("Enter Your Age:", min_value=1, max_value=100, step=1)
        gender = st.selectbox("Select Gender:", ["Male", "Female", "Other"])
        meal = st.selectbox("Meal Preference:", ["Veg", "Non-Veg", "No Meal"])
        submit = st.form_submit_button("Book Ticket")
    
        if submit:
            if name and train_no:
                save_booking(name, train_no, date, seat_class, age, gender, meal)
                st.success(f"✅ Ticket booked successfully for {name} on train {train_no} - {TRAINS.get(train_no)} - {seat_class} class on {date}!")
            else:
                st.error("❌ Please fill all fields.")
    
    # Display all bookings
    if os.path.exists(CSV_FILE):
        st.subheader("📜 Bookings List")
        df = pd.read_csv(CSV_FILE)
        st.dataframe(df)

    # Cancel Booking Section
    st.subheader("❌ Cancel a Booking")
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        if not df.empty:
            selected_index = st.selectbox("Select a booking to cancel:", df.index)
            if st.button("Cancel Booking"):
                df.drop(selected_index, inplace=True)
                df.to_csv(CSV_FILE, index=False)
                st.success("✅ Booking cancelled successfully!")
                st.experimental_rerun()
        else:
            st.info("No bookings available to cancel.")
    else:
        st.info("No bookings found.")

if __name__ == "__main__":
    main()
