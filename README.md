# AI Assistant - Multi-Agent System with RAG & SQL

An AI assistant with a manager agent that orchestrates SQL querying, document Q&A (RAG), and data visualization. Built with FastAPI, React, LangChain, and Docker.

## 🌟 Features

- **SQL Agent** - Natural language to SQL queries on sales database
- **RAG Tool** - Upload documents (PDF, DOCX, TXT) and ask questions with source citations
- **Visualization** - Auto-generate charts (bar, line, pie, scatter) from query results
- **Conversation Memory** - Maintains context across sessions

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────┐
│              Nginx (Port 80)                      │
└─────────────┬─────────────────────┬──────────────┘
              │                     │
     ┌────────▼────────┐   ┌───────▼────────┐
     │   Frontend      │   │    Backend     │
     │   React + Vite  │   │    FastAPI     │
     └─────────────────┘   └───────┬────────┘
                                   │
              ┌────────────────────┼────────────────────┐
              │                    │                    │
     ┌────────▼────────┐  ┌───────▼───────┐  ┌────────▼────────┐
     │  Manager Agent  │  │  PostgreSQL   │  │  FAISS Vector   │
     │   (LangChain)   │  │   Database    │  │     Store       │
     └────────┬────────┘  └───────────────┘  └─────────────────┘
              │
    ┌─────────┼─────────┐
    │         │         │
┌───▼───┐ ┌───▼───┐ ┌───▼───┐
│ SQL   │ │  RAG  │ │ Viz   │
│ Agent │ │ Tool  │ │ Tool  │
└───────┘ └───────┘ └───────┘
```

## 📋 Prerequisites

- Docker & Docker Compose
- OpenAI API Key

## 🚀 Quick Start

### 1. Configure Environment

```bash
# Copy environment template
copy .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-key-here
```

### 2. Start Services

```bash
docker-compose up --build
```

### 3. Load Sales Data

**Important:** After the containers are running, load the CSV dataset into the database:

```bash
# Enter the backend container
docker exec -it ai_assistant_backend bash

# Run the data loading script
python load_sales_data.py
```

This loads the `Supermarket_Sales.csv` data into PostgreSQL.

### 4. Access the Application

Open your browser: **http://localhost**

## 💬 Usage Examples

**SQL Queries:**
- "What are the total sales by branch?"
- "Show me the top 5 products by revenue"

**Document Q&A:**
- "What does the document say about [topic]?"

**Visualizations:**
- "Visualize sales by branch"
- "Show me a chart of revenue by product"

## 🔐 Environment Variables

```env
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4
```

## 📊 Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | React, Vite, TailwindCSS, Recharts |
| Backend | FastAPI, Python 3.11, LangChain |
| AI | OpenAI GPT-4 |
| Database | PostgreSQL |
| Vector Store | FAISS |
| Containerization | Docker, Nginx |

## 🐛 Troubleshooting

```bash
# Rebuild containers
docker-compose down
docker-compose up --build

# View logs
docker-compose logs -f backend

# Reset database
docker-compose down -v
docker-compose up --build
```

## 📝 License

For educational and development purposces.

---

**Built with GPT-4, LangChain, FastAPI, and React**
