# CodeReviewA

## Introduction
CodeReviewA is an automated coding assignment review tool that leverages OpenAI's GPT API and GitHub API to provide insightful code reviews. 

## Requirements
- Python 3.9+
- Poetry
- GitHub Token
- OpenAI API Key

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/CodeReviewA.git
   cd CodeReviewA

2. Install dependencies 
    ```bash
    pip3 install -r requirements.txt

3. Set enviroment variables in .env file

4. Start the application
    ```bash
    uvicorn app.main:app --reload

5. Test the API: Use tools like Postman or cURL to send a POST request to http://localhost:8000/review with JSON body:
    ```json
    {
    "assignment_description": "Implement a sorting algorithm.",
    "github_repo_url": "https://api.github.com/repos/username/repo_name/contents/",
    "candidate_level": "Junior"
    }

