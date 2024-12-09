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

---

## 1. Handling 100+ New Review Requests per Minute

To manage a high volume of review requests, consider the following architectural strategies:

Asynchronous Processing: Implement an asynchronous task queue (e.g., using Celery with RabbitMQ or Redis) to handle incoming review requests. This allows the application to quickly acknowledge requests while offloading the actual review processing to background workers.

Load Balancing: Deploy multiple instances of the FastAPI application behind a load balancer (e.g., NGINX or AWS Elastic Load Balancing). This will distribute incoming requests evenly across multiple instances, improving response times and reliability.

Horizontal Scaling: Increase the number of application instances based on demand. Use container orchestration tools like Kubernetes to manage scaling automatically based on CPU and memory usage.

Caching: Utilize caching mechanisms (e.g., Redis) to store frequently requested data or review results. This reduces the number of requests sent to the OpenAI and GitHub APIs, thereby improving performance and reducing costs.

## 2. Handling Large Repositories with 100+ Files

When dealing with large repositories, the following strategies can be implemented:

File Chunking: If a repository contains many files, consider splitting the review process into chunks. Instead of sending all files for review at once, process files in smaller batches. This will help stay within OpenAI's token limits and reduce the load on the system.

Prioritize File Types: Implement logic to prioritize certain file types (e.g., .py, .js) over others (e.g., .md, .txt). This ensures that the most critical files are reviewed first.

Parallel Processing: Use concurrent processing to analyze multiple files simultaneously. This can be achieved through asynchronous programming (using asyncio) or multi-threading/multiprocessing techniques.

## 3. Managing Increased API Usage

To effectively manage the increased usage of the OpenAI and GitHub APIs, consider the following:

Rate Limiting: Implement rate limiting on API requests to prevent hitting the API limits. Use backoff strategies (e.g., exponential backoff) to handle API rate limit responses gracefully.

Batch Requests: Where possible, batch requests to the OpenAI API. This can help to reduce the number of individual requests and stay within rate limits.

Monitoring and Alerts: Set up monitoring and alerting for API usage. This can help to identify when usage is approaching limits, allowing proactive measures to be taken.

Cost Management: Regularly review API usage to identify potential cost-saving opportunities. OpenAI provides usage dashboards that can be monitored to ensure that costs remain within budget.

## Conclusion

By implementing these strategies, the Coding Assignment Auto-Review Tool can be effectively scaled to handle a high volume of review requests and large repositories. Additionally, careful management of API usage will help to maintain performance while controlling costs.