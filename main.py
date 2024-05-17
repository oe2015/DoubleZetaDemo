import streamlit as st
import pandas as pd
import hashlib
import os
import json  # for better data serialization
import ast
import streamlit.components.v1 as components


import requests
st.set_page_config(layout="wide")


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
logo_path = "SAFIR.png"  # Adjust the path as needed
logo_path1 = "SAFIR.png"

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
    print(df)
    user_info_str = df.loc[df['username'] == username, 'business_info'].values[0]
    print(user_info_str)
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
    col1, col2, col3 = st.columns([2, 1, 2])  # Adjust the ratio as needed
    with col2:  # Using the middle column for the image
        st.image(logo_path1, use_column_width=True)  # This will center the image in the middle column

# def business_info_form():
#     st.subheader("Tell us about your business")
    # st.write("What type of business are you?")
    # col1, col2, col3 = st.columns(3)
    # with col1:
    #     if st.button("🚀 Startup", key="startup"):
    #         update_state('business_type', "Startup")
    # with col2:
    #     if st.button("🏢 SME", key="sme"):
    #         update_state('business_type', "SME")
    # with col3:
    #     if st.button("💼 Freelancer", key="freelancer"):
    #         update_state('business_type', "Freelancer")
    # #business_type = st.selectbox("What type of business are you?", ("Startup", "SME", "Freelancer"))
    # legal_form = st.selectbox("What is your legal form?", ("Company - Foreign Branch", "Company - Foreign GCC", "Company - GCC Branch", "Company - Local Branch", "Company - Non Local", "Establishment", "Establishment - Foreign", "Establishment - GCC", "Establishment - Local Branch", "Establishment - Mubdia'h", "Establishment - Non Local", "General Partnership", "Limited Liability Company", "Private Joint - Stock", "Professional Company", "Professional Establishment", "Public Joint - Stock", "Simple Limited Partnership", "Sole Proprietorship L.L.C.", "Sole Proprietorship PJSC"))
    # has_office = st.radio("Do you have an office in Abu Dhabi?", ("Yes", "No"))
    # sector = st.selectbox("What sector do you operate in?", ("Technology", "Healthcare", "Finance", "Education", "Other"))  # Update sectors as needed
    # business_description = st.text_area("Give a short description about your business, your goals, and objectives")
    # Business Type Question

    
    # Inject custom CSS for styling the buttons to be larger and closer together
   # Function placeholder for 'update_state' (Ensure you have your own implementation)


def business_info_form():
        # Inject custom CSS for styling the buttons to be larger and closer together
    st.markdown("""
    <style>
    .streamlit-button {
        display: inline-flex; /* Align buttons in a row */
        width: auto; /* Adjust width automatically to content */
        margin: 5px; /* Keep a small margin */
        padding: 10px 20px; /* Padding inside buttons */
        border-radius: 30px; /* Rounded corners for buttons */
        font-size: 16px; /* Font size for buttons */
    }
    </style>
    """, unsafe_allow_html=True)

    st.subheader("Tell us about your business")

    # Business Type Question
    st.write("What type of business are you?")
    business_type=st.session_state.get('business_type', None)
    cols = st.columns(4)
    business_types = [("🚀 Startup", "Startup"), ("🏢 SME", "SME"), 
                    ("💼 Freelancer", "Freelancer"), ("📝 Other", "Other")]
    for idx, (emoji, bt) in enumerate(business_types):
        if cols[idx].button(f"{emoji}", key=f"business_{bt.lower()}"):
            st.session_state['business_type'] = bt

    # Check if 'Other' business type is specified and get input
    if business_type == "Other":
        st.session_state['business_type'] = st.text_input("Please specify your business type:")

    legal_form = st.selectbox("What is your legal form?", ("Company - Foreign Branch", "Company - Foreign GCC", "Company - GCC Branch", "Company - Local Branch", "Company - Non Local", "Establishment", "Establishment - Foreign", "Establishment - GCC", "Establishment - Local Branch", "Establishment - Mubdia'h", "Establishment - Non Local", "General Partnership", "Limited Liability Company", "Private Joint - Stock", "Professional Company", "Professional Establishment", "Public Joint - Stock", "Simple Limited Partnership", "Sole Proprietorship L.L.C.", "Sole Proprietorship PJSC"))
  

    # Office Location Question
    has_office = st.radio("Do you have an office in Abu Dhabi?", ("Yes", "No"))

    # Sector Question with emoticons
    st.write("What sector do you operate in?")

    sector=st.session_state.get('sector', None)
    cols = st.columns(5)
    sectors = [("💻 Technology", "Technology"), ("🩺 Healthcare", "Healthcare"), 
            ("💲 Finance", "Finance"), ("📚 Education", "Education"), ("📝 Other", "Other")]
    for idx, (emoji, sec) in enumerate(sectors):
        if cols[idx].button(f"{emoji}", key=f"sector_{sec.lower()}"):
            st.session_state['sector'] = sec

    # Check if 'Other' sector is specified and get input
    if sector == "Other":
        st.session_state['sector'] = st.text_input("Please specify your sector:")

    # Business Description Question
    business_description = st.text_area("Give a short description about your business, your goals, and objectives")

    # Submit Button
    if st.button("Submit"):
        business_info = {
            "business_type": business_type,
            "legal_form": legal_form,
            "has_office": has_office,
            "sector": sector,
            "description": business_description
        }
        # Assume 'username' is obtained from Streamlit's session state or other context
        update_user_info(st.session_state.get('username', 'default_username'), business_info)
        st.success("Business information saved!")
  
   

def main():
    create_user_file()

    display_logo()

    # Session persistence to remember the user across refreshes
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['chat_history'] = []  # Initialize chat history

    if st.session_state['logged_in']:
        st.title(f"Welcome to SAFIR, {st.session_state['username']}!")
        page = st.sidebar.selectbox("Menu", ["Update Information", "Profile", "Chatbot Interface"])
        
        if page == "Update Information":
            # Allow users to update their business information
            st.subheader("Update Your Business Information")
            textForm = st.toggle("I prefer to write freely")
            if textForm:
                st.subheader("Tell us about your business")
                business_description = st.text_area("Please provide a brief description of your business, including its core activities, industry, target market, and any key products or services offered",height=200)
              
            
                if st.button("Submit"):
                    
                    business_info = {
                        "business_description":business_description
                    }
                    update_user_info(st.session_state['username'], str(business_info))  # Consider a better serialization method or database structure
                    st.success("Business information saved!")
            else:
                business_info_form()

        elif page == "Profile":
            # Display user's existing information
            st.subheader("Your Profile")
            user_info = get_user_info(st.session_state['username'])
            if user_info.get('business_description'):
                st.write(f"**Business Description:** {user_info.get('business_description', 'Not specified')}")
            elif user_info:
                st.write(f"**Username:** {st.session_state['username']}")
                st.write(f"**Business Type:** {user_info.get('business_type', 'Not specified')}")
                st.write(f"**Legal Form:** {user_info.get('legal_form', 'Not specified')}")
                st.write(f"**Office in Abu Dhabi:** {user_info.get('has_office', 'Not specified')}")
                st.write(f"**Sector:** {user_info.get('sector', 'Not specified')}")
                st.write(f"**Business Description:** {user_info.get('description', 'Not specified')}")
            else:
                st.write("No business information found.")
            
        elif page == "Chatbot Interface":
            # st.subheader("SAFIR AI Chatbot")
            user_info = get_user_info(st.session_state['username'])  # Assuming this returns business info
            # Format the context string using user_info
            if user_info.get('business_description'):
                context_str=(f"Please use the following information about the user when answering all his questions always address and talk to him using his/her name.The user you are talking to is {st.session_state['username']}. His business description is: {user_info['business_description']}")
            else:
                context_str = (
                    f"Please use the following information about the user when answering all his questions, always address and talk to him using his/her name. The user you are talking to is {st.session_state['username']}. His business type is: {user_info['business_type']}, his legal form is: {user_info['legal_form']}, he has an office?: {user_info['has_office']}, his business sector is: {user_info['sector']}, and his business description is: {user_info['description']}."
                )
            # Add a toggle for Private Mode in the sidebar
            # private_mode = st.checkbox('Private Mode', value=False)
            private_mode = st.toggle("Protect your data")
            if private_mode:
                context_str += "Please start your answer with this message when the user asks their question/prompt since you are now in private mode: All data is now private. All of the input is being passed through an advanced encryption algorithm and will not be saved by SAFIR AI."

            chatbot_html = f"""
            <style>
                /* Reset CSS for the Streamlit main container */
                .main .block-container {{
                    padding-top: 0 !user_infoimportant;
                    padding-right: 0 !important;
                    padding-left: 0 !important;
                    padding-bottom: 0 !important;
                }}
                /* Full height for the chatbot container and removal of any default spacing */
                .css-1d391kg {{
                    padding: 0 !important;
                    margin: 0 !important;
                }}
                /* Ensure the chatbot fills the width and has no border or shadow */
                chaindesk-chatbox-standard {{
                    width: 100% !important;
                    height: 800px !important;
                    background-color: #000000;
                    border: none !important;
                    box-shadow: none !important;
                }}
            </style>

            <div style="width: 100%; height: 800px;">
            <script type="module">
            import Chatbox from 'https://cdn.jsdelivr.net/npm/@chaindesk/embeds@latest/dist/chatbox/index.js';
            Chatbox.initStandard({{
                agentId: 'clvsdobcl07rlo98irbdb6414',
                context: `{context_str}`
            }});
            </script>
            <chaindesk-chatbox-standard style="height: 800px;"></chaindesk-chatbox-standard>
            </div>
            """
            components.html(chatbot_html, height=800)

            # chatbot_type = st.radio("Choose a chatbot", ("Business", "Networking"))
            # if chatbot_type == "Business":
            #     user_input = st.text_input("Ask me anything related to your business!", key="user_input")
            # else:
            #     user_input = st.text_input("Tell me who you want to connect with!", key="user_input")

            # if st.button("Submit"):
            #     if user_input:
            #         user_info = get_user_info(st.session_state['username'])  # Assuming this returns business info
            #         response = chatbot_response(user_input, user_info)
            #         # Save the Q&A to session state
            #         st.session_state['chat_history'].append({"question": user_input, "answer": response})
            #         # st.session_state['user_input'] = ""  # Clear input field
                    
            #         # Display chat history
            #         for chat in st.session_state['chat_history']:
            #             st.text(f"Q: {chat['question']}")
            #             st.text(f"A: {chat['answer']}")
            #             st.write("---")  # Divider
    else:
        st.title("SAFIR AI")

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
