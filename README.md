# BOOK_HUB
Provides the book (digital copy) for reading for free!!!
# 📚 Book Management App

A full-stack application with FastAPI backend and Streamlit frontend for managing your personal book collection with ratings and progress tracking.

## Features

- 🔐 **User Authentication**
  - Secure login/registration
  - Password hashing
- 📖 **Book Management**
  - Add books with titles, authors, and links
  - Rate books (1-5 stars)
  - Track reading progress (0-100%)
- 📊 **Interactive Dashboard**
  - Visual progress bars
  - Expandable book cards
  - Real-time updates
- 🚀 **Modern Tech Stack**
  - FastAPI backend
  - Streamlit frontend
  - SQLite database

## Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Backend Setup
``bash
cd backend
pip install -r requirements.txt
python main.py
Frontend Setup
bash
Copy
cd frontend
pip install -r requirements.txt
streamlit run app.py
Usage
Register a new account or Login

# Add Books:

Fill in title (required) and author (required)

Optionally add:

Book link (URL)

Rating (1-5 stars)

Reading progress (0-100%)

Manage Collection:

Update ratings/progress anytime

View all books in expandable cards

Click links to open books

# API Endpoints
Endpoint	Method	Description
/register	POST	Create new account
/login	POST	User authentication
/books	GET	Get all books for user
/books	POST	Add new book
/books/{id}	PUT	Update book details

# Project Structure
Copy
book-app/
├── backend/
│   ├── main.py         # FastAPI server
│   ├── requirements.txt
│   └── app.db          # Database (auto-created)
└── frontend/
    ├── app.py          # Streamlit UI
    └── requirements.txt
# Troubleshooting
Common Issues:

401 Unauthorized: Check your login credentials

404 Not Found: Ensure backend is running

500 Server Error: Check terminal logs for details

# Reset Database:

bash
Copy
rm backend/app.db
Future Enhancements
Book categories/tags

Reading statistics dashboard

Mobile app integration

Export/import functionality

# License
MIT License - Free for personal and commercial use

Copy

---

### Key Elements Included:
1. **Clear Header** with placeholder for screenshot
2. **Feature Highlights** with emojis
3. **Step-by-Step Installation**
4. **Usage Instructions**
5. **API Documentation**
6. **Project Structure**
7. **Troubleshooting** common issues
8. **Future Roadmap**
9. **License Information**

To use:
1. Create a `README.md` file in your project root
2. Paste this content
3. Replace placeholder screenshot with actual image
4. Customize future enhancements as needed

## DEVELOPER 
SIDDHARTH RAGHUNATHA SHETTY 
[Linked in](https://www.linkedin.com/in/siddharth-shetty-657797283/overlay/about-this-profile/?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base%3Bo%2BHt9X6SShmxtmjUNL0UJA%3D%3D)
