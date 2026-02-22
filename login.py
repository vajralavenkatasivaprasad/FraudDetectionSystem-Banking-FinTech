import streamlit as st

# Initialize session state variables
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# User login function
def login():
    if st.session_state['authenticated']:
        st.success("You are already logged in!")
        return

    with st.form(key='login_form'):
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        submit_button = st.form_submit_button("Login")

        if submit_button:
            # Here you should implement your authentication logic
            # For demonstration, I'll just check against a hardcoded value
            if username == "user" and password == "pass":
                st.session_state['authenticated'] = True
                st.success("Successfully logged in!")
                st.balloons()
            else:
                st.error("Incorrect username or password")

# Main function to display the app
def app():
    st.title("Login Page")
    login()

if __name__ == "__main__":
    app()