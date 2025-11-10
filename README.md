# PNCT Container Query API

A FastAPI-based container tracking system that integrates with PNCT (Port Newark Container Terminal) to retrieve container details using AI-powered agents, MCP (Model Context Protocol) servers, and Temporal workflow orchestration.

## Project Overview

This application provides a REST API for querying container information from PNCT's TOS Inquiry system. It leverages Google's Gemini AI model to process natural language queries, uses Temporal for workflow orchestration, and implements the Model Context Protocol for structured AI interactions.

## Architecture

The system consists of several interconnected components:

- **FastAPI Server**: REST API endpoint for container queries
- **AI Agent**: Google Gemini-powered agent for query processing
- **MCP Server**: Model Context Protocol server for structured AI tool integration
- **Temporal Workflows**: Orchestrates container scraping tasks with retry logic
- **Web Scraper**: Extracts container details from PNCT TOS Inquiry portal

## Features

- Natural language container query processing
- Temporal workflow orchestration for reliable scraping
- Automatic retry mechanism for failed requests
- Docker containerization for easy deployment
- Health check monitoring
- Structured logging

## Prerequisites

- Docker and Docker Compose
- Python 3.11 or higher
- Google Gemini API key

## Environment Setup

Create a `.env` file in the root directory with the following variables:

```
GEMINI_API_KEY=your_gemini_api_key_here
WORK_FLOW_PORT=7233
WORKFLOW_URL=http://temporal:7233
```

## Installation

### Using Docker Compose (Recommended)

1. Clone the repository
2. Set up your `.env` file with required credentials
3. Build and start all services:

```bash
docker-compose up --build
```

This will start:

- Temporal server on port 7233
- Temporal UI on port 8080
- PostgreSQL database on port 5432
- FastAPI application on port 8000
- MCP server on port 8001

### Local Development

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Start the FastAPI server:

```bash
python main.py
```

3. In a separate terminal, start the Temporal worker:

```bash
python temporal_workflow/worker.py
```

4. In another terminal, start the MCP server:

```bash
python mcp_client_Server/mcp_server.py
```

## API Endpoints

### Health Check

```
GET /
```

Returns the health status of the API.

**Response:**

```json
{
  "status": "Healthy!"
}
```

### Query Container

```
POST /container/query
```

Process a natural language query about container information.

**Request Body:**

```json
{
  "query": "What are the details for container ABCD1234567?"
}
```

**Response:**

```json
{
  "status": "success",
  "data": "Container details here..."
}
```

## Project Structure

```
.
├── app/
│   ├── agent.py              # AI agent implementation
│   └── schemas.py            # Pydantic models
├── temporal_workflow/
│   ├── workflows.py          # Temporal workflow definitions
│   ├── activities.py         # Temporal activity functions
│   ├── pnct_scrape.py        # Web scraping logic
│   └── worker.py             # Temporal worker
├── mcp_client_Server/
│   └── mcp_server.py         # MCP server implementation
├── logs/                     # Application logs
├── docker-compose.yml        # Docker Compose configuration
├── Dockerfile                # Docker image definition
├── main.py                   # FastAPI application entry point
├── requirements.txt          # Python dependencies
└── start_services.sh         # Service startup script
```

## Dependencies

Key dependencies include:

- **fastapi** - Modern web framework for building APIs
- **uvicorn** - ASGI server for FastAPI
- **google-genai** - Google Gemini AI integration
- **pydantic-ai-slim** - AI agent framework
- **fastmcp** - Model Context Protocol implementation
- **temporalio** - Temporal workflow SDK
- **beautifulsoup4** - HTML parsing for web scraping
- **requests** - HTTP library for API calls

## Temporal Workflows

The application uses Temporal for orchestrating container scraping tasks:

- **ScrapePNCTWorkflow**: Main workflow that processes container IDs
- Automatically retries failed scraping attempts (up to 3 times)
- Implements exponential backoff for retry logic
- Task queue: `pnct-task-queue`

## Monitoring

- **Temporal UI**: Access at http://localhost:8080 to monitor workflows
- **FastAPI Docs**: Access at http://localhost:8000/docs for API documentation
- **Health Check**: Automated health monitoring via Docker healthcheck

## Development

To modify the scraping logic, update the `temporal_workflow/pnct_scrape.py` file with your implementation.

To add new API endpoints, edit `main.py` and add corresponding schemas in `app/schemas.py`.

To customize the AI agent behavior, modify `app/agent.py`.

## Error Handling

The application includes comprehensive error handling:

- HTTP 400 for invalid queries
- HTTP 500 for internal server errors
- Temporal retry policies for transient failures
- Graceful service shutdown handling

## Logging

Logs are stored in the `logs/` directory and include:

- Application events
- Workflow execution details
- Error traces
- API request/response information

## License

This project is provided as-is for container tracking purposes.

## Contributing

Contributions are welcome. Please ensure all tests pass and follow the existing code style.

## Support

For issues or questions, please refer to the project documentation or open an issue in the repository.
