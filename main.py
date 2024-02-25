import streamlit as st
import pandas as pd
import hashlib
import os
import json  # for better data serialization
import ast


import requests

def chatbot_response(question, context):
    response = requests.post("http://127.0.0.1:5000/generate", json={"question": question, "context": context})
    # response = requests.post("http://127.0.0.1:5000", json={"question": question}, headers={"Content-Type": "application/json"})
    print(response)
    if response.status_code == 200:
        return response.json()
    else:
        return "Error: Could not generate response."

# File where user details are stored (for simplicity, using CSV here)
user_file = "users.csv"
logo_path = "/Users/omarelherraoui/Desktop/Double_Zeta/logo.png"  # Adjust the path as needed

def create_user_file():
    if not os.path.exists(user_file):
        df = pd.DataFrame(columns=["username", "password", "business_info"])
        df.to_csv(user_file, index=False)

def add_user(username, password):
    try:
        df = pd.read_csv(user_file)
        # Check if the username already exists
        if username in df['username'].values:
            st.warning("Username already exists. Please choose a different username.")
            return False
        else:
            new_row = pd.DataFrame({"username": [username], "password": [password], "business_info": [""]})
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(user_file, index=False)
            return True
    except Exception as e:
        st.error(f"Failed to add user: {e}")
        return False

def update_user_info(username, business_info):
    df = pd.read_csv(user_file)
    # Store the info as a JSON string
    df.loc[df['username'] == username, 'business_info'] = json.dumps(business_info)
    df.to_csv(user_file, index=False)

import math

def get_user_info(username):
    df = pd.read_csv(user_file)
    user_info_str = df.loc[df['username'] == username, 'business_info'].values[0]
    try:
        user_info_str = user_info_str.strip('"""')
        # If it's a string representation of a dict, safely convert it to a dict
        user_info = ast.literal_eval(user_info_str) if user_info_str else {}
    except (ValueError, SyntaxError) as e:
        st.error(f"Error parsing user information: {e}")
        user_info = {}

    return user_info

def verify_login(username, password):
    df = pd.read_csv(user_file)
    user = df[(df['username'] == username) & (df['password'] == password)]
    return not user.empty

def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def display_logo():
    st.image(logo_path, width=100)  # Adjust width as needed

def business_info_form():
    st.subheader("Tell us about your business")
    business_type = st.selectbox("What type of business are you?", ("Startup", "SME", "Freelancer"))
    legal_form = st.selectbox("What is your legal form?", ("Company - Foreign Branch", "Company - Foreign GCC", "Company - GCC Branch", "Company - Local Branch", "Company - Non Local", "Establishment", "Establishment - Foreign", "Establishment - GCC", "Establishment - Local Branch", "Establishment - Mubdia'h", "Establishment - Non Local", "General Partnership", "Limited Liability Company", "Private Joint - Stock", "Professional Company", "Professional Establishment", "Public Joint - Stock", "Simple Limited Partnership", "Sole Proprietorship L.L.C.", "Sole Proprietorship PJSC"))
    has_office = st.radio("Do you have an office in Abu Dhabi?", ("Yes", "No"))
    sector = st.selectbox("What sector do you operate in?", ("Technology", "Healthcare", "Finance", "Education", "Other"))  # Update sectors as needed
    business_description = st.text_area("Give a short description about your business, your goals, and objectives")
    
    if st.button("Submit"):
        business_info = {
            "business_type": business_type,
            "legal_form": legal_form,
            "has_office": has_office,
            "sector": sector,
            "description": business_description
        }
        update_user_info(st.session_state['username'], str(business_info))  # Consider a better serialization method or database structure
        st.success("Business information saved!")


def main():
    create_user_file()

    display_logo()

    # Session persistence to remember the user across refreshes
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['chat_history'] = []  # Initialize chat history

    if st.session_state['logged_in']:
        st.title(f"Welcome to Double Zeta, {st.session_state['username']}!")
        page = st.sidebar.selectbox("Menu", ["Update Information", "Profile", "Chatbot Interface"])
        
        if page == "Update Information":
            # Allow users to update their business information
            st.subheader("Update Your Business Information")
            business_info_form()

        elif page == "Profile":
            # Display user's existing information
            st.subheader("Your Profile")
            user_info = get_user_info(st.session_state['username'])
            if user_info:
                st.write(f"**Username:** {st.session_state['username']}")
                st.write(f"**Business Type:** {user_info.get('business_type', 'Not specified')}")
                st.write(f"**Legal Form:** {user_info.get('legal_form', 'Not specified')}")
                st.write(f"**Office in Abu Dhabi:** {user_info.get('has_office', 'Not specified')}")
                st.write(f"**Sector:** {user_info.get('sector', 'Not specified')}")
                st.write(f"**Business Description:** {user_info.get('description', 'Not specified')}")
            else:
                st.write("No business information found.")
            
        elif page == "Chatbot Interface":
            st.subheader("Chatbot")

            chatbot_type = st.radio("Choose a chatbot", ("Business", "Networking"))
            if chatbot_type == "Business":
                user_input = st.text_input("Ask me anything related to your business!", key="user_input")
            else:
                user_input = st.text_input("Tell me who you want to connect with!", key="user_input")

            if st.button("Submit"):
                if user_input:
                    user_info = get_user_info(st.session_state['username'])  # Assuming this returns business info
                    response = chatbot_response(user_input, user_info)
                    # Save the Q&A to session state
                    st.session_state['chat_history'].append({"question": user_input, "answer": response})
                    # st.session_state['user_input'] = ""  # Clear input field
                    
                    # Display chat history
                    for chat in st.session_state['chat_history']:
                        st.text(f"Q: {chat['question']}")
                        st.text(f"A: {chat['answer']}")
                        st.write("---")  # Divider
    else:
        st.title("Double Zeta")

        menu = ["Login", "SignUp"]
        choice = st.sidebar.selectbox("Menu", menu)

        if choice == "Login":
            st.subheader("Login Section")
            username = st.text_input("Username")
            password = st.text_input("Password", type='password')

            if st.button("Login"):
                hashed_password = hash_password(password)
                if verify_login(username, hashed_password):
                    st.success(f"Logged In as {username}")
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = username
                    st.experimental_rerun()
                else:
                    st.warning("Incorrect Username/Password")

        elif choice == "SignUp":
            st.subheader("Create New Account")
            new_user = st.text_input("Username")
            new_password = st.text_input("Password", type='password')

            if st.button("SignUp"):
                if add_user(new_user, hash_password(new_password)):
                    st.success("You have successfully created an account!")
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = new_user
                    st.experimental_rerun()

if __name__ == '__main__':
    main()
