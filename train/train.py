import streamlit as st
import pandas as pd

# Initialize session state for ticket data and counter
if "ticket_data" not in st.session_state:
    st.session_state.ticket_data = []
    
if "ticket_counter" not in st.session_state:
    st.session_state.ticket_counter = 1  # Start counter at 1

# Initialize form submission state
if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False

# Clear fields
def reset_form():
    """Reset all form fields to default values"""
    st.session_state.name_input = ""
    st.session_state.train_no_select = 1010
    st.session_state.age_input = 1
    st.session_state.gender_radio = "Male"
    st.session_state.meal_select = "Veg"
    st.session_state.class_select = "Sleeper"    

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Book Ticket", "Delete Ticket", "View Records"])

# Booking Page
if page == "Book Ticket":
    st.title("🚆 Book a Train Ticket")

    train_numbers = ["Select Train",1010, 1025, 1050, 1075, 1090]

    with st.form("booking_form"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Enter your Name:")
            train_no = st.selectbox("Select Train Number:", train_numbers)
            age = st.number_input("Enter your Age:", min_value=1, max_value=100, step=1)

        with col2:
            gender = st.radio("Select Gender:", ["Male", "Female", "Other"])
            meal = st.selectbox("Meal Preference:", ["Select","Veg", "Non-Veg", "No Meal"])
            train_class = st.selectbox("Class:", ["Select Class","Sleeper", "AC 3 Tier", "AC 2 Tier", "First Class"])

        submit_button = st.form_submit_button("🎟️ Book Ticket")

    if submit_button:
        if name.strip() and train_no and age and gender and meal and train_class:
            # Generate formatted ticket number
            ticket_no = f"TT{st.session_state.ticket_counter:04d}"
            new_data = {
                "Ticket No": ticket_no,
                "Name": name, 
                "Train No": train_no, 
                "Age": age, 
                "Gender": gender, 
                "Meal": meal, 
                "Class": train_class
            }
            
            st.session_state.ticket_data.append(new_data)
            st.session_state.ticket_counter += 1  # Increment counter
            
            st.success(f"✅ Ticket Booked Successfully! Your Ticket Number: `{ticket_no}`")
        else:
            st.error("⚠️ All fields are required! Please fill in all details.")

# Delete Page
elif page == "Delete Ticket":
    st.title("🗑️ Delete a Booking")

    if st.session_state.ticket_data:
        ticket_numbers = [record["Ticket No"] for record in st.session_state.ticket_data]
        delete_ticket = st.selectbox("Select Ticket Number to Delete:", ticket_numbers)

        if st.button("🗑️ Confirm Delete"):
            # Delete the selected ticket
            st.session_state.ticket_data = [record for record in st.session_state.ticket_data 
                                          if record["Ticket No"] != delete_ticket]
            
            # Check if all records are deleted
            if not st.session_state.ticket_data:
                st.session_state.ticket_counter = 1  # Reset the counter to 1
            
            st.success(f"✅ Ticket `{delete_ticket}` Deleted Successfully!")
    else:
        st.warning("⚠️ No bookings available to delete.")
# View Records Page
elif page == "View Records":
    st.title("📋 View Booked Tickets")

    if st.session_state.ticket_data:
        df = pd.DataFrame(st.session_state.ticket_data)
        # Set Ticket No as the first column
        df = df[["Ticket No"] + [col for col in df.columns if col != "Ticket No"]]
        st.dataframe(
            df.style.set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#4CAF50'), ('color', 'white')]}
            ])
        )
    else:
        st.warning("⚠️ No bookings available.")
