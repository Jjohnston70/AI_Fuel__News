import os
from supabase import create_client
from dotenv import load_dotenv
import pandas as pd
import streamlit as st

# Load environment variables from .env file
load_dotenv()

# Get Supabase credentials from environment variables
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

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
        
        # Insert comment into the 'comments' table
        data = {
            "section": section,
            "comment": comment,
            "user_name": user_name,
            # created_at will be automatically set by Supabase
        }
        
        response = supabase.table("comments").insert(data).execute()
        
        if hasattr(response, 'error') and response.error:
            return False, f"Error saving comment: {response.error}"
        return True, "Comment saved successfully!"
    
    except Exception as e:
        return False, f"Error saving comment: {e}"

def get_comments(section=None):
    """Get comments from Supabase database.
    
    Args:
        section: Optional filter for specific section
    
    Returns:
        DataFrame with comments or empty DataFrame if error
    """
    try:
        supabase = init_connection()
        if not supabase:
            return pd.DataFrame()
        
        # Query the 'comments' table
        query = supabase.table("comments").select("*")
        
        # Filter by section if provided
        if section:
            query = query.eq("section", section)
        
        # Order by created_at (newest first)
        query = query.order("created_at", desc=True)
        
        # Execute the query
        response = query.execute()
        
        # Convert to DataFrame
        if hasattr(response, 'data') and response.data:
            return pd.DataFrame(response.data)
        return pd.DataFrame()
    
    except Exception as e:
        st.error(f"Error retrieving comments: {e}")
        return pd.DataFrame() 