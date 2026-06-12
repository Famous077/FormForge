import streamlit as st
from services.persistence.exercise_repository import get_or_create_user

def render_login_wall():
    if st.session_state.get("user_id") is not None:
      return True
    
    st.title("FormForge: Your AI-Powered Form Builder")
    st.markdown("### Welcome to FormForge! Please enter a username to get started.")
    
    
    with st.form("login_form", clear_on_submit=False):
      username = st.text_input("Name(unique)", placeholder="unique name e.g: Rahul")
      submit_button = st.form_submit_button("Start Session")
      
    if submit_button:
      if not username:
        st.error("Name cannot be empty. Please enter a unique name.")    
        return False
      user = get_or_create_user(username)
      if user is None:
        st.error("Failed to create or retrieve user. Try a different name.")
        return False

      # `user` is a sqlite3.Row with columns `id`, `username`, ...
      st.session_state["user_id"] = user["id"]
      st.session_state["username"] = user["username"]
      
      st.rerun()
        
    return False
  