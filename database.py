from supabase import create_client
import pandas as pd
import streamlit as st

# Get Supabase credentials from Streamlit secrets
supabase_url = st.secrets["SUPABASE"]["SUPABASE_URL"]
supabase_key = st.secrets["SUPABASE"]["SUPABASE_KEY"]

@st.cache_resource
def init_connection():
    """Initialize connection to Supabase."""
    try:
        return create_client(supabase_url, supabase_key)
    except Exception as e:
        st.error(f"Failed to connect to Supabase: {e}")
        return None

def save_comment(section, comment, user_name="Anonymous"):
    """Save a comment to Supabase database."""
    if not comment.strip():
        return False, "Comment cannot be empty"
    
    try:
        supabase = init_connection()
        if not supabase:
            return False, "Database connection failed"
        
        data = {
            "section": section,
            "comment": comment,
            "user_name": user_name,
        }
        
        response = supabase.table("comments").insert(data).execute()
        
        if hasattr(response, 'error') and response.error:
            return False, f"Error saving comment: {response.error}"
        return True, "Comment saved successfully!"
    
    except Exception as e:
        return False, f"Error saving comment: {e}"

def get_comments(section=None):
    """Get comments from Supabase database."""
    try:
        supabase = init_connection()
        if not supabase:
            return pd.DataFrame()
        
        query = supabase.table("comments").select("*")
        
        if section:
            query = query.eq("section", section)
        
        query = query.order("created_at", desc=True)
        response = query.execute()
        
        if hasattr(response, 'data') and response.data:
            return pd.DataFrame(response.data)
        return pd.DataFrame()
    
    except Exception as e:
        st.error(f"Error retrieving comments: {e}")
        return pd.DataFrame()
