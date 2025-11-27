# AI Assistant - Multi-Agent System with RAG & SQL

A production-ready AI assistant featuring a manager agent that orchestrates multiple specialized tools: SQL querying, document Q&A (RAG), and data visualization. Built with FastAPI, React, LangChain, and Docker.

## 🌟 Features

### **Manager Agent**
- Intelligent routing between specialized tools
- Conversation memory across sessions
- GPT-4 powered decision making

### **SQL Agent Tool**
- Natural language to SQL queries
- Query sales database with conversational interface
- Automatic query optimization and error handling

### **RAG Tool**
- Upload multiple document formats (PDF, DOCX, TXT, MD)
- FAISS vector store for semantic search
- Source citations with every answer
- Document chunking and metadata tracking

### **Dashboard Tool**
- Auto-generate interactive charts from SQL results
- Plotly-powered visualizations (bar, line, pie, scatter)
- Real-time data from agent context (no re-querying)

### **Additional Features**
- Conversation history persistence
- Document management (upload, list, delete)
- Glassmorphism UI with gradient backgrounds
- Responsive design
- Docker containerization with nginx reverse proxy

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Nginx (Port 80)                      │
│                     Reverse Proxy Layer                      │
└────────────────┬────────────────────────┬───────────────────┘
                 │                        │
        ┌────────▼────────┐      ┌───────▼────────┐
        │   Frontend      │      │    Backend     │
        │   React + Vite  │      │    FastAPI     │
        │   Port 3000     │      │    Port 8000   │
        └─────────────────┘      └────────┬───────┘
                                           │
                    ┌──────────────────────┼──────────────────────┐
                    │                      │                      │
           ┌────────▼────────┐   ┌────────▼────────┐   ┌────────▼────────┐
           │  Manager Agent  │   │   PostgreSQL    │   │  FAISS Vector   │
           │   (LangChain)   │   │   Database      │   │     Store       │
           └────────┬────────┘   │   Port 5432     │   │  (File System)  │
                    │            └─────────────────┘   └─────────────────┘
        ┌───────────┼───────────┐
        │           │           │
┌───────▼──────┐ ┌──▼──────┐ ┌─▼──────────┐
│  SQL Agent   │ │ RAG Tool│ │ Dashboard  │
│    Tool      │ │         │ │    Tool    │
└──────────────┘ └─────────┘ └────────────┘
```

## 📋 Prerequisites

- Docker & Docker Compose
- OpenAI API Key
- 4GB RAM minimum
- 10GB disk space

## 🚀 Quick Start

### 1. Clone and Setup

```bash
cd AI_assistant
```

### 2. Configure Environment

```bash
# Copy environment template
copy .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-key-here
```

### 3. Start All Services

```bash
docker-compose up --build
```

This will start:
- **PostgreSQL** on port 5432
- **Backend API** on port 8000
- **Frontend** on port 3000
- **Nginx** on port 80

### 4. Access the Application

Open your browser to: **http://localhost**

## 📁 Project Structure

```
AI_assistant/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── agents/            # Agent implementations
│   │   │   ├── manager_agent.py      # Main orchestrator
│   │   │   ├── sql_agent_tool.py     # SQL queries
│   │   │   ├── rag_tool.py           # Document Q&A
│   │   │   └── dashboard_tool.py     # Visualizations
│   │   ├── api/               # API routes
│   │   ├── models/            # Database & Pydantic models
│   │   ├── services/          # Business logic
│   │   ├── config.py          # Configuration
│   │   ├── database.py        # DB connection
│   │   └── main.py            # FastAPI app
│   ├── uploads/               # Document storage
│   ├── vector_store/          # FAISS indices
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/                   # React Frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── ChatInterface.jsx
│   │   │   ├── MessageBubble.jsx
│   │   │   ├── DocumentPanel.jsx
│   │   │   └── Header.jsx
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── Dockerfile
│
├── database/                   # PostgreSQL
│   └── init.sql               # Schema & sample data
│
├── nginx/                      # Reverse Proxy
│   ├── nginx.conf
│   └── Dockerfile
│
├── docker-compose.yml
├── .env.example
└── README.md
```

## 🗄️ Database Schema

### Sales Table
```sql
- id: SERIAL PRIMARY KEY
- date: DATE
- branch: VARCHAR(50)          # A, B, C
- customer_type: VARCHAR(50)   # Member, Normal
- gender: VARCHAR(20)           # Male, Female
- product_line: VARCHAR(100)   # Product category
- unit_price: DECIMAL(10,2)
- quantity: INTEGER
- payment: VARCHAR(50)          # Cash, Credit card, Ewallet
- rating: DECIMAL(3,1)          # 1-10
- total: DECIMAL(10,2)          # Computed
```

### Documents Table
```sql
- id: SERIAL PRIMARY KEY
- filename: VARCHAR(255)
- original_filename: VARCHAR(255)
- file_path: VARCHAR(500)
- file_size: INTEGER
- file_type: VARCHAR(50)
- chunk_count: INTEGER
- upload_date: TIMESTAMP
- metadata: JSON
```

### Conversations Table
```sql
- id: SERIAL PRIMARY KEY
- session_id: VARCHAR(100)
- user_message: TEXT
- agent_response: TEXT
- tool_used: VARCHAR(50)
- metadata: JSON
- created_at: TIMESTAMP
```

## 💬 Usage Examples

### SQL Queries
```
"What are the total sales by branch?"
"Show me the top 5 product lines by revenue"
"What's the average rating for each payment method?"
"Compare sales between male and female customers"
```

### Document Q&A
```
"What does the document say about [topic]?"
"Summarize the key points from the uploaded files"
"Find information about [specific subject]"
```

### Visualizations
```
"Show me a chart of sales by branch"
"Visualize the top products"
"Create a graph of ratings over time"
```

### Combined Queries
```
"Query the database for branch sales and show me a bar chart"
"What are the payment methods and visualize their distribution"
```

## 🔧 API Endpoints

### Chat
```http
POST /api/chat
Content-Type: application/json

{
  "message": "Your question here",
  "session_id": "optional-session-id"
}
```

### Upload Document
```http
POST /api/upload
Content-Type: multipart/form-data

file: <file>
```

### List Documents
```http
GET /api/documents
```

### Delete Document
```http
DELETE /api/documents/{document_id}
```

### Health Check
```http
GET /api/health
```

## 🛠️ Development

### Backend Development

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run locally
uvicorn app.main:app --reload
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

### Database Access

```bash
# Connect to PostgreSQL
docker exec -it ai_assistant_db psql -U postgres -d ai_assistant

# View tables
\dt

# Query sales
SELECT * FROM sales LIMIT 10;
```

## 🔐 Environment Variables

### Backend (.env)
```env
OPENAI_API_KEY=your_key_here
DATABASE_URL=postgresql://postgres:postgres@database:5432/ai_assistant
OPENAI_MODEL=gpt-4
UPLOAD_DIR=/app/uploads
VECTOR_STORE_DIR=/app/vector_store
```

## 📊 Technology Stack

| Component | Technology |
|-----------|-----------|
| Frontend | React 18, Vite, TailwindCSS |
| Backend | FastAPI, Python 3.11 |
| AI/ML | OpenAI GPT-4, LangChain |
| Database | PostgreSQL 16 |
| Vector Store | FAISS |
| Visualization | Plotly.js |
| Containerization | Docker, Docker Compose |
| Reverse Proxy | Nginx |
| Document Processing | PyPDF2, python-docx |

## 🎨 UI Features

- **Glassmorphism Design**: Modern glass-effect cards with backdrop blur
- **Gradient Backgrounds**: Purple-to-pink gradients throughout
- **Responsive Layout**: Works on desktop, tablet, and mobile
- **Real-time Updates**: Instant message rendering
- **Chart Integration**: Interactive Plotly charts inline
- **Source Citations**: Expandable source cards for RAG responses
- **Document Management**: Drag-and-drop upload with progress
- **Tool Indicators**: Visual badges showing which tool was used

## 🐛 Troubleshooting

### Docker Issues
```bash
# Rebuild containers
docker-compose down
docker-compose up --build

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Database Connection
```bash
# Check database is running
docker ps | grep postgres

# Reset database
docker-compose down -v
docker-compose up -d database
```

### OpenAI API Errors
- Verify API key in `.env`
- Check API quota and billing
- Ensure GPT-4 access is enabled

## 📈 Performance Tips

1. **Vector Store**: FAISS indices are cached in memory
2. **Database**: Connection pooling enabled (10 connections)
3. **Frontend**: Static assets cached for 1 year
4. **Nginx**: Gzip compression enabled
5. **Agent**: Max 5 iterations to prevent infinite loops

## 🔄 Updates & Maintenance

### Update Dependencies
```bash
# Backend
cd backend
pip install --upgrade -r requirements.txt

# Frontend
cd frontend
npm update
```

### Backup Database
```bash
docker exec ai_assistant_db pg_dump -U postgres ai_assistant > backup.sql
```

### Clear Vector Store
```bash
# Remove all documents
rm -rf backend/vector_store/*
```

## 📝 License

This project is for educational and development purposes.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📧 Support

For issues and questions:
- Check the troubleshooting section
- Review Docker logs
- Verify environment variables
- Ensure OpenAI API key is valid

---

**Built with ❤️ using GPT-4, LangChain, FastAPI, and React**
