import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

def sign_up(email, password):
    try:
        user = supabase.auth.sign_up({"email": email, "password": password})
        return user
    except Exception as e:
        st.error(f"Registration failed: {e}")

def sign_in(email, password):
    try:
        user = supabase.auth.sign_in_with_password({"email": email, "password": password})
        return user
    except Exception as e:
        st.error(f"Login failed: {e}")

def sign_out():
    try:
        supabase.auth.sign_out()
        st.session_state["user"]=None
        make_current_page("log_in")
        st.rerun()

    except Exception as e:
        st.error(f"Logout failed: {e}")




#-------------------------------------------------------------------------------------------


def make_current_page(name):
    st.session_state["current_page"]=name


def main_page():
    st.success(f"welcome {st.session_state["user"]}")
    if st.button("Sign out"):
        sign_out()


def sign_up_page():
  st.title("Sign-Up")
  userName=st.text_input("Username",key="sign_up_username")
  password=st.text_input("Password",type="password",key="sign_up_password")
  cols=st.columns([7,1])
  with cols[0]:
      sign_up_button=st.button("Sign-Up",key="sign_up_button")
  with cols[1]:
      st.button("Return",on_click=make_current_page,args=("log_in",))
  if sign_up_button and not(userName and password):
        st.error("Please enter username and password")
  elif(sign_up_button and userName and password):
      user=sign_up(userName,password)
      if user:
          st.success("Succesfully signed up, Please confirm your mail.")
  
  
  
    
  

def log_in_page():
  st.title("To-Do App Authentication")
  userName=st.text_input("Username")
  password=st.text_input("Password",type="password")
  cols=st.columns([7,1])
  with cols[0]:
      login_button=st.button("Login")
  with cols[1]:
      st.button("Sign-Up",on_click=make_current_page,args=("sign_up",))

  if login_button and not(userName and password):
      st.error("Please enter username and password")

  if login_button and userName and password:
      with st.spinner("Logging in"):

        user=sign_in(userName,password)
      if user:
          st.session_state["user"]=user.user
          st.rerun()

if "user" not in st.session_state:
    st.session_state["user"]=None
    st.session_state["current_page"]="log_in"



if st.session_state["user"]:
    main_page()
elif not st.session_state["user"] and st.session_state["current_page"]=="log_in" :
    log_in_page()
elif not st.session_state["user"] and st.session_state["current_page"]=="sign_up":
    sign_up_page()

