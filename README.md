# AI Job Board Backend API

A backend REST API for an AI-focused job board platform built using FastAPI and SQLAlchemy.  
This project demonstrates backend API design, database integration, and search/sorting features.

---

## Features

- Add and list AI job postings  
- Search jobs by title, description, or skills  
- Sort jobs by salary (ascending & descending)  
- Mark and remove favourite jobs  
- SQLite database with SQLAlchemy ORM  
- Preloaded sample AI job listings  

---

## Tech Stack

- Python  
- FastAPI  
- SQLAlchemy  
- SQLite  
- Pydantic  

---

## API Endpoints

GET /jobs  
GET /jobs/search?query=python  
GET /jobs/salary_asc  
GET /jobs/salary_desc  
POST /jobs  
POST /jobs/{id}/favourite  
POST /jobs/{id}/unfavourite  
GET /favourites  

---

## Conclusion

This project simulates a real-world backend system for job platforms and showcases API design, database operations, and backend engineering fundamentals.  
It can be extended with authentication, PostgreSQL, and frontend UI in future.
