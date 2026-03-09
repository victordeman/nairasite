# NAIRA - African AI & XR Excellence Hub

NAIRA (NBU Artificial Intelligence Research & Advancement Institute) is a full-stack FastAPI application dedicated to transforming education and innovation through immersive XR experiences and agentic AI architectures.

## Project Structure

```
.
├── app/
│   ├── models/          # Pydantic schemas
│   ├── routers/         # API and Page routers
│   ├── static/          # CSS, JS, and image files
│   ├── templates/       # HTML templates (Jinja2)
│   ├── __init__.py
│   ├── database.py      # Database configuration and seeding
│   └── main.py          # FastAPI application entry point
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

## Setup and Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

Start the FastAPI server using `uvicorn`:

```bash
uvicorn app.main:app --reload
```

The application will be available at `http://127.0.0.1:8000`.

## AI Agent Configuration

The NAIRA AI Assistant supports multiple models, including Gemini 1.5 Pro and Llama 3 (via Hugging Face). To enable these models, set the following environment variables:

- `GOOGLE_API_KEY`: Your Google AI Studio API key (required for Gemini and RAG embeddings).
- `HF_TOKEN`: Your Hugging Face Access Token (required for Llama 3).

If no keys are provided, the agent will operate in **Local Mode**, using keyword-based search for its knowledge base.

## API Endpoints

- **GET /**: Home page (Template rendered)
- **GET /healthz**: Health check endpoint
- **GET /api/pillars**: Get all strategic pillars
- **GET /api/architecture**: Get all architecture layers
- **GET /api/revenue-streams**: Get all revenue streams
- **POST /api/contact**: Submit a contact form
- **POST /api/newsletter**: Subscribe to the newsletter

For full API documentation, visit `http://127.0.0.1:8000/docs` or `http://127.0.0.1:8000/redoc`.

## Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: SQLite with `aiosqlite`
- **Frontend**: Tailwind CSS, Feather Icons, Jinja2 Templates
- **Icons**: Feather Icons
