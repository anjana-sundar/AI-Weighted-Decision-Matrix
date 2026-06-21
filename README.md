# Weighted Decision Matrix AI

An AI-powered decision support tool that helps users make structured decisions by generating weighted evaluation criteria instead of relying on traditional pros-and-cons lists.

The application converts natural language decision prompts into a weighted decision matrix using a Large Language Model (LLM), allowing users to compare alternatives based on multiple criteria and priorities.

## Features

* Generate decision matrices from natural language input
* Automatically create decision criteria and assign weights
* Compare multiple options using weighted scoring
* Interactive frontend for adjusting priorities and scores
* FastAPI backend with REST API endpoints
* Groq LLM integration for AI-assisted decision analysis

## Example

**Input**

text
Should I pursue a Master's degree or start working after graduation?

**Generated Criteria**

* Salary Potential
* Career Growth
* Learning Opportunities
* Financial Cost
* Work Experience

The system assigns weights and scores to each criterion, then calculates an overall recommendation.

---

## Tech Stack

### Backend

* Python
* FastAPI
* Groq API

### Frontend

* HTML
* JavaScript
* Tailwind CSS

---

## Project Structure

decision/
│
├── controllers/
│   └── ai_controller.py
│
├── routes/
│   └── ai_routes.py
│
├── index.py
├── index.html
├── prototype_algorithm.py
├── requirements.txt
└── vercel.json

---

## API Endpoint

### Generate Decision Matrix

POST /ai

#### Request

json
{
  "user_input": "Should I pursue a Master's degree or start working after graduation?"
}


#### Response

json
{
  "success": true,
  "data": "{ generated decision matrix }"
}


---

## Running Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

env
GROQ_API_KEY=your_api_key

Start the server:

```bash
uvicorn index:app --reload
```

Open:

http://127.0.0.1:8000/docs

to access the API documentation.

---

## Development Journey

The project began as a simple weighted scoring algorithm implemented in Python (`prototype_algorithm.py`), where users manually entered options, criteria, weights, and scores.

It was later expanded into a full-stack application with:

* FastAPI backend
* Interactive frontend interface
* AI-generated criteria and scoring suggestions
* REST API architecture
* LLM integration using Groq
---
## Author

Anjana Sundar

Computer Science Engineering Student