import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth



if not firebase_admin._apps:
    cred = credentials.Certificate('timesheet-conversion-platform-1a4518ecf4e8.json')
    default_app = firebase_admin.initialize_app(cred)


st.title("Welcome to Timesheet processing application")
choice= st.selectbox("Login/SignUp", ['Login', 'SignUp'])
if choice== 'Login':
    email= st.text_input('Enter username')
    password= st.text_input('password', type='password')
    st.button('Login')
else:
    email = st.text_input('Enter your username')
    password= st.text_input('password', type='password')

    username= st.text_input('Enter your unique username')

    create_account=st.button('Create your account')
    if create_account:
        user= auth.create_user(email=email, password=password,uid= username)
        st.success('Account created successfully')
        st.markdown('Please login using your email and password')
        st.balloons()



##+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Define valid credentials
VALID_USERNAME = 'apexon'
VALID_PASSWORD = 'apexon'

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'page' not in st.session_state:
    st.session_state.page = 'Login'

# Page: Login
if st.session_state.page == 'Login':
    st.title("Apexon Timesheet Conversion Platform.")

    # Create login form
    with st.form(key='login_form'):
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        submit_button = st.form_submit_button("Login")

        if submit_button:
            if username == VALID_USERNAME and password == VALID_PASSWORD:
                st.session_state.authenticated = True
                st.session_state.page = 'Main'
                st.success("Login successful!")
            else:
                st.error("Invalid username or password.")

# Page: Main
elif st.session_state.page == 'Main':
    if st.session_state.authenticated:
        st.title("Apexon Timesheet Conversion Platform.")
        st.write("You have successfully logged in!")
        # The rest of your Streamlit app code
        # Sign out button
        if st.sidebar.button("Sign Out"):
            st.session_state.authenticated = False
            st.session_state.page = 'Login'
            # st.experimental_rerun()
    else:
        st.write("Please log in to access this page.")


###+++++++++++++++++++++++++++++++++++++++Login Mechanism+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import streamlit as st
import firebase_admin
import pyrebase
from firebase_admin import credentials, auth
from firebase_admin._auth_utils import UserNotFoundError

# Initialize Firebase app
if not firebase_admin._apps:
    cred = credentials.Certificate('timesheet-conversion-platform-79b3689b08bb.json')
    firebase_admin.initialize_app(cred)

# Pyrebase Configuration (use your Firebase project's configuration)
firebaseConfig = {
    "apiKey": "AIzaSyA_S_qNq5UlIaq5Mp2Xl2LdXeOYrgVA51k",
    "authDomain": "your-auth-domain",
    "databaseURL": "your-database-url",
    "projectId": "timesheet-conversion-platform",
    "storageBucket": "your-storage-bucket",
    "messagingSenderId": "865705745377",
    "appId": "your-app-id",
    "measurementId": "your-measurement-id"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth_client = firebase.auth()
# App State
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Authentication Flow
if st.session_state.logged_in:
    st.title("Timesheet Processing Platform")
    st.write("Timesheet Processing Platform!")

    if st.button("Sign out"):
        st.session_state.logged_in = False
        # st.experimental_rerun()

else:
    choice = st.selectbox("Login/SignUp", ['Login', 'SignUp'])

    st.title(f"{choice} Timesheet Processing Platform")
    email = st.text_input('Enter email')
    password = st.text_input('Password', type='password')

    if choice == "Login":
        if st.button("Login"):
            try:
                # Verify credentials
                # user = auth.get_user_by_email(email)
                user = auth_client.sign_in_with_email_and_password(email, password)
                st.session_state.logged_in = True
                st.success("Login successful!")
                st.balloons()
            except UserNotFoundError:
                st.error("Login failed. User not found. Please check your credentials.")
            except Exception as e:
                st.error(f"Invalid credentials entered")

    else:  # Sign Up
        if st.button("Sign Up"):
            try:
                # user = auth.create_user(email=email, password=password)
                user= auth_client.create_user_with_email_and_password(email, password)
                st.success('Account created successfully')
                st.markdown('Please log in using your email and password')
                st.balloons()
            except Exception as e:
                st.error(f"Enter valid email address and password")














# else:
#     pass
    # email = st.text_input('Enter email address')
    # password = st.text_input("Enter your password", type='password')
    # username= st.text_input('Enter your unique username')
    # if st.button('Create account'):
    #     user= auth.create_user(email= email, password= password, uid= username)
    #
    #     st.success("Account created successfully")
    #     st.markdown('Please login using your username and password')
    #     st.balloons()







