import streamlit as st
import requests
from datetime import datetime

# API configuration
API_URL = "http://localhost:8000"

# Initialize session state
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "username" not in st.session_state:
    st.session_state.username = None

# Auth functions
def register(username, password):
    response = requests.post(
        f"{API_URL}/register",
        json={"username": username, "password": password}
    )
    return response.json()

def login(username, password):
    response = requests.post(
        f"{API_URL}/login",
        json={"username": username, "password": password}
    )
    return response.json()

# UI Components
def auth_section():
    st.title("Book Management App")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.form_submit_button("Login"):
                try:
                    result = login(username, password)
                    st.session_state.user_id = result.get("user_id")
                    st.session_state.username = username
                    st.success("Logged in successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Login failed: {str(e)}")
    
    with tab2:
        with st.form("register_form"):
            username = st.text_input("New Username")
            password = st.text_input("New Password", type="password")
            if st.form_submit_button("Register"):
                try:
                    result = register(username, password)
                    st.success(result.get("message", "Registration successful!"))
                except Exception as e:
                    st.error(f"Registration failed: {str(e)}")

def books_section():
    st.header(f"📚 Welcome, {st.session_state.username}!")
    
    # Add Book Form - Unique key with user_id
    with st.form(f"add_book_form_{st.session_state.user_id}"):
        title = st.text_input("Title*", key="book_title")
        author = st.text_input("Author*", key="book_author")
        link = st.text_input("Book Link (URL)", key="book_link")
        
        cols = st.columns(2)
        with cols[0]:
            rating = st.selectbox(
                "Rating (optional)",
                options=[""] + list("⭐"*i for i in range(1,6)),
                key="book_rating"
            )
        with cols[1]:
            progress = st.slider(
                "Progress %", 
                min_value=0, 
                max_value=100,
                value=0,
                key="book_progress"
            )
        
        if st.form_submit_button("Add Book"):
            if title and author:
                try:
                    response = requests.post(
                        f"{API_URL}/books",
                        json={
                            "title": title,
                            "author": author,
                            "link": link if link else None,
                            "rating": len(rating) if rating else None,
                            "progress": progress if progress > 0 else None
                        },
                        params={"user_id": st.session_state.user_id}
                    )
                    if response.status_code == 200:
                        st.success("Book added successfully!")
                        st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            else:
                st.warning("Please fill in required fields (*)")

    # Display Books
    st.subheader("Your Books")
    try:
        books = requests.get(
            f"{API_URL}/books",
            params={"user_id": st.session_state.user_id}
        ).json()
        
        if books:
            for book in books:
                with st.expander(f"{book['title']} by {book['author']}"):
                    cols = st.columns([1, 3])
                    
                    # Rating
                    with cols[0]:
                        current_rating = book.get('rating', 0)
                        new_rating = st.selectbox(
                            "Rating",
                            options=[""] + list("⭐"*i for i in range(1,6)),
                            index=current_rating,
                            key=f"rating_{book['id']}"
                        )
                        if new_rating and len(new_rating) != current_rating:
                            requests.put(
                                f"{API_URL}/books/{book['id']}",
                                json={"rating": len(new_rating)},
                                params={"user_id": st.session_state.user_id}
                            )
                            st.rerun()
                    
                    # Progress
                    with cols[1]:
                        current_progress = book.get('progress', 0)
                        new_progress = st.slider(
                            "Progress %",
                            min_value=0,
                            max_value=100,
                            value=current_progress,
                            key=f"progress_{book['id']}"
                        )
                        if new_progress != current_progress:
                            requests.put(
                                f"{API_URL}/books/{book['id']}",
                                json={"progress": new_progress},
                                params={"user_id": st.session_state.user_id}
                            )
                            st.rerun()
                    
                    # Visual progress bar
                    st.progress(current_progress / 100)
                    
                    # Link
                    if book.get('link'):
                        st.markdown(f"[🔗 Open Book]({book['link']})")
        else:
            st.info("No books found. Add your first book above!")
    except Exception as e:
        st.error(f"Failed to load books: {str(e)}")

# Main app logic
if not st.session_state.user_id:
    auth_section()
else:
    if st.button("Logout"):
        st.session_state.user_id = None
        st.session_state.username = None
        st.rerun()
    books_section()