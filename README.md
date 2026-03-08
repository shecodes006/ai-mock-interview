![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Scikit--Learn-orange)

# AI Mock Interview Platform

An AI-powered backend system that simulates technical interviews, evaluates answers, and provides analytics to help users track their performance across multiple interview sessions.

This project is built using **FastAPI, PostgreSQL, and Machine Learning**, and generates detailed analytics graphs after each interview.

---

# Project Demo

Watch the backend system in action:

[Download Demo Video](assets/backend1.0_output.mp4)

### Database Setup

Create a PostgreSQL database named `ai_mock_interview`.

Then update the database credentials in:

backend/database/connection.py
# Features

### Interview System

* Start and manage interview sessions
* Technical and HR interview questions
* Automatic interview termination when question limit is reached
* Answer evaluation and scoring

### Resume Processing

* Resume PDF upload
* Resume text extraction
* Job role prediction using Machine Learning

### Analytics & Visualization

* Score progression during interview
* Category performance analysis
* Skill strength comparison
* Score distribution pie chart
* Score histogram
* Progress tracking across multiple interviews

### Data Storage

* PostgreSQL database integration
* Interview session history
* Stored questions, answers, scores, and feedback

---

# Tech Stack

### Backend

* FastAPI
* Python

### Database

* PostgreSQL
* pgAdmin4

### Machine Learning

* Scikit-learn
* TF-IDF Vectorization
* Logistic Regression

### Visualization

* Matplotlib

---

# Project Structure

```
ai-mock-interview
│
├── backend
│   ├── routers
│   ├── services
│   ├── database
│   ├── models
│   ├── data
│   ├── graphs
│   ├── utils
│   ├── main.py
│   └── requirements.txt
│
├── .gitignore
└── README.md
```

---

# API Endpoints

### Start Interview

```
POST /interview/start
```

### Submit Answer

```
POST /interview/answer
```

### End Interview

```
POST /interview/end
```

### Get Interview Result

```
GET /interview/result
```

### Get Interview History

```
GET /interview/history
```

### View Analytics Dashboard

```
GET /interview/graphs
```

### Upload Resume

```
POST /resume/upload
```

---

# Analytics Graphs

The platform generates the following graphs after an interview session:

1. Score progression during the interview
2. Category performance analysis
3. Skill strength comparison
4. Interview score distribution (pie chart)
5. Score histogram
6. User progress across multiple interviews

Graphs are automatically generated and stored in the `graphs/` folder.

---

# Running the Project

### 1 Install dependencies

```
pip install -r requirements.txt
```

### 2 Start the FastAPI server

```
uvicorn main:app --reload
```

### 3 Open API documentation

```
http://127.0.0.1:8000/docs
```

---

# Database

The system uses PostgreSQL with the following main tables:

* users
* resumes
* interview_sessions
* interview_questions

These tables store user data, interview sessions, questions, answers, scores, and analytics results.

---

# Future Improvements

* Frontend dashboard
* GPT-based answer evaluation
* Authentication and user accounts
* Deployment to cloud platforms
* Enhanced analytics and reporting

---

# Author

AI Mock Interview Backend Project
