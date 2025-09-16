# QuantLeaves Customer Support Chatbot

A modern, AI-powered customer support chatbot built using **RAG (Retrieval-Augmented Generation)** technology. This project combines a powerful FastAPI backend with a sleek Next.js frontend to deliver intelligent, context-aware responses based on your knowledge base.

## ⚡ Quick Start (Docker Compose - Recommended)

```bash
# 1. Clone the repository
git clone <repo-url>
cd saas-analytics-customer-support-chatbot

# 2. Configure backend environment
cd backend
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 3. Run knowledge base ingestion (one-time setup)
UV_CACHE_DIR=../.uv-cache uv venv && source .venv/bin/activate
UV_CACHE_DIR=../.uv-cache uv sync
uv run python -m ingest

# 4. Start all services with Docker Compose
cd ..
docker-compose up

# 5. Open http://localhost:3000 and try the chat widget!
```

**Services will be available at:**
- 🌐 **Frontend**: http://localhost:3000
- 🔌 **Backend API**: http://localhost:8000
- 🗄️ **PostgreSQL**: localhost:5433

## 🚀 Alternative: Manual Setup

For development or if you prefer running services individually:

```bash
# 1. Clone and setup
git clone <repo-url>
cd saas-analytics-customer-support-chatbot

# 2. Start database only
docker-compose up postgres -d

# 3. Setup backend
cd backend
UV_CACHE_DIR=../.uv-cache uv venv && source .venv/bin/activate
UV_CACHE_DIR=../.uv-cache uv sync
cp .env.example .env  # Add your OPENAI_API_KEY
uv run python -m ingest  # Setup knowledge base
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &

# 4. Setup frontend
cd ../frontend
pnpm install
pnpm run dev

# 5. Open http://localhost:3000 and click "Try the Chat Widget"
```

## 🚀 Features

### 🤖 Intelligent Chat Widget
- **Modal Widget Interface** - Compact, embeddable chat widget with modern design
- **Landing Page** - Professional homepage with widget demonstration
- **Real-time Responses** - Instant AI-powered responses to customer queries
- **Typing Indicators** - Visual feedback during response generation
- **Message Citations** - Shows sources and references for transparency

### 📚 RAG Technology
- **Document Processing** - Supports PDF and Markdown documents via Docling
- **Vector Search** - Uses Qdrant for fast semantic search
- **Hybrid Retrieval** - Combines structured and vector-based search
- **OpenAI Integration** - Leverages GPT models for response generation

### ⚙️ Admin Features
- **Knowledge Base Management** - Refresh corpus through admin panel
- **Error Handling** - Comprehensive error boundaries and user feedback
- **Health Monitoring** - Built-in health checks and logging

### 🎨 Modern UI/UX
- **Dark Theme** - Professional dark mode interface
- **Responsive Design** - Works on desktop and mobile
- **Tailwind CSS** - Modern, utility-first styling
- **TypeScript** - Full type safety throughout

## 🛠 Tech Stack

### Backend
- **FastAPI** - High-performance Python web framework
- **LangChain** - Framework for building LLM applications
- **Qdrant** - Vector database for semantic search
- **Docling** - Document processing and parsing
- **OpenAI API** - GPT models for response generation
- **PostgreSQL** - Primary database with pgvector extension
- **SQLAlchemy** - ORM for database operations

### Frontend
- **Next.js 15** - React framework with App Router
- **React 19** - Latest React with concurrent features
- **TypeScript** - Static type checking
- **Tailwind CSS 4** - Utility-first CSS framework
- **Geist Font** - Modern typography

## 📋 Prerequisites

Before running this project, ensure you have:

### Required for Docker Compose (Recommended)
- **Docker** and **Docker Compose** installed
- **OpenAI API key** for GPT access
- **Git** for version control
- **Python 3.11+** (for initial knowledge base ingestion)
- **uv** Python package manager (`pip install uv`)

### Additional for Manual Setup
- **Node.js 18+** and **pnpm** installed
- **PostgreSQL** (or use Docker for database only)

## 🚀 Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/AbdullahKhanASI/quant-leaves-customer-support-chatbot-using-qdrant-openaiapi-docling-fastapi-nextjs.git
cd quant-leaves-customer-support-chatbot-using-qdrant-openaiapi-docling-fastapi-nextjs
```

### 2. Start PostgreSQL Database

```bash
# Start PostgreSQL with pgvector using Docker Compose
docker-compose up postgres -d

# Verify database is running
docker ps | grep quantleaves-postgres
```

This will start a PostgreSQL container with:
- **Port**: 5433 (mapped to container's 5432)
- **Database**: quantleaves
- **Username/Password**: postgres/postgres
- **Extensions**: pgvector enabled

### 3. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment using uv
UV_CACHE_DIR=../.uv-cache uv venv
source .venv/bin/activate

# Install dependencies
UV_CACHE_DIR=../.uv-cache uv sync

# Copy environment file and configure
cp .env.example .env
```

**Configure your `backend/.env` file:**
```bash
# Required: OpenAI API configuration
OPENAI_API_KEY=your_openai_api_key_here

# Required: Database configuration (using Docker container)
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5433/quantleaves

# Optional: Other settings
OPENAI_CHAT_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-large
LOG_LEVEL=INFO
```

### 4. Ingest Knowledge Base

```bash
# Run ingestion pipeline (requires valid .env configuration)
uv run python -m ingest
```

This will:
- Parse documents from the `corpus/` directory
- Generate embeddings using OpenAI
- Store data in PostgreSQL with vector indexing
- Create all necessary database tables

### 5. Start Backend Server

```bash
# Start FastAPI server with auto-reload
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: http://localhost:8000

### 6. Frontend Setup

Open a new terminal:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
pnpm install

# Copy environment file
cp .env.local.example .env.local
```

**Configure `frontend/.env.local`:**
```bash
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

### 7. Start Frontend Server

```bash
# Start Next.js development server
pnpm run dev
```

Frontend will be available at: http://localhost:3000

## 🎯 Usage

### Chat Widget Interface

1. **Open the Application**: Navigate to http://localhost:3000
2. **Try the Widget**: Click "Try the Chat Widget" button on the landing page
3. **Start Chatting**: Type your questions in the modal chat interface
4. **View Responses**: Get AI-powered responses with citations and sources
5. **Review Citations**: See source references from the knowledge base
6. **Close Widget**: Click the X button or click outside the modal

### Admin Interface

1. **Access Settings**: Click "Admin Settings" button on the landing page
2. **Refresh Knowledge Base**: Use the "Refresh Knowledge Base" button when adding new documents
3. **Monitor Status**: Check system information and ingestion status

### Adding New Documents

1. **Add Files**: Place PDF or Markdown files in the `backend/corpus/` directory
2. **Refresh Corpus**: Use the admin panel to trigger re-ingestion
3. **Test Knowledge**: Ask questions about the new content

## 📁 Project Structure

```
quant-leaves-customer-support-chatbot/
├── backend/                    # FastAPI backend
│   ├── app/                   # Application package
│   │   ├── api/              # API routes
│   │   ├── core/             # Configuration and utilities
│   │   ├── db/               # Database models and sessions
│   │   ├── ingestion/        # Document processing pipeline
│   │   ├── retrieval/        # Search and retrieval logic
│   │   ├── services/         # Business logic services
│   │   └── models/           # Pydantic schemas
│   ├── corpus/               # Knowledge base documents
│   ├── tests/                # Test suite
│   ├── .env.example          # Environment template
│   ├── pyproject.toml        # Python dependencies
│   └── README.md             # Backend documentation
├── frontend/                  # Next.js frontend
│   ├── src/
│   │   ├── app/              # Next.js App Router
│   │   ├── components/       # React components
│   │   └── types/            # TypeScript definitions
│   ├── public/               # Static assets
│   ├── package.json          # Node.js dependencies
│   └── README.md             # Frontend documentation
├── docs/                     # Additional documentation
├── .gitignore               # Git ignore rules
├── docker-compose.yml       # Docker services
└── README.md               # This file
```

## 🔧 Configuration Options

### Backend Configuration

Key environment variables in `backend/.env`:

- `OPENAI_API_KEY`: Required for AI responses
- `DATABASE_URL`: PostgreSQL connection string
- `QDRANT_URL`: Vector database URL (optional)
- `LOG_LEVEL`: Logging verbosity (DEBUG, INFO, WARNING, ERROR)
- `CORS_ORIGINS`: Allowed frontend origins

### Frontend Configuration

Environment variables in `frontend/.env.local`:

- `NEXT_PUBLIC_BACKEND_URL`: Backend API endpoint

## 🧪 Testing

### Backend Tests

```bash
cd backend
uv run pytest
```

### Frontend Tests

```bash
cd frontend
pnpm run test
```

## 🏗 Building for Production

### Backend

```bash
cd backend
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
pnpm run build
pnpm start
```

## 🐳 Docker Compose Setup

### Full Stack (Recommended)

Start all services with a single command:

```bash
# Start all services (postgres, backend, frontend)
docker-compose up

# Start in background (detached mode)
docker-compose up -d

# View logs for all services
docker-compose logs -f

# View logs for specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres

# Stop all services
docker-compose down

# Rebuild and start (after code changes)
docker-compose up --build
```

**Service Details:**
- **PostgreSQL**: ankane/pgvector:latest with vector extensions
- **Backend**: FastAPI with uv dependency management
- **Frontend**: Next.js with pnpm package manager
- **Networking**: Services communicate internally via Docker network

### Database Only (For Development)

If you prefer to run backend and frontend manually:

```bash
# Start PostgreSQL database only
docker-compose up postgres -d

# View database logs
docker-compose logs postgres

# Stop database
docker-compose stop postgres
```

## 📈 Monitoring and Logging

### Health Checks

- Backend health: http://localhost:8000/health
- Frontend status: http://localhost:3000

### Logs

- Backend logs: `backend.log`
- Uvicorn logs: `backend_uvicorn.log`
- Frontend logs: Browser console

## 🤝 Contributing

1. **Fork the Repository**
2. **Create Feature Branch**: `git checkout -b feature/amazing-feature`
3. **Commit Changes**: `git commit -m 'Add amazing feature'`
4. **Push to Branch**: `git push origin feature/amazing-feature`
5. **Open Pull Request**

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Troubleshooting

### Common Issues

**1. Database Connection Errors**
- Ensure PostgreSQL container is running: `docker ps | grep quantleaves-postgres`
- Restart database if needed: `docker-compose up postgres -d`
- Verify DATABASE_URL uses port 5433: `postgresql+asyncpg://postgres:postgres@localhost:5433/quantleaves`
- Check that pgvector extension is enabled (done automatically by container)

**2. OpenAI API Errors**
- Verify OPENAI_API_KEY is valid
- Check API quota and billing
- Ensure network connectivity

**3. Frontend Connection Issues**
- Verify backend is running on port 8000
- Check NEXT_PUBLIC_BACKEND_URL configuration
- Review CORS settings in backend

**4. Ingestion Failures**
- Ensure documents are in supported formats (PDF, MD)
- Check file permissions in corpus directory
- Verify OpenAI API key for embeddings

### Getting Help

- **Issues**: Open an issue on GitHub
- **Discussions**: Use GitHub Discussions for questions
- **Documentation**: Check individual README files in backend/ and frontend/

## 🔮 Future Enhancements

- [ ] Multi-language support
- [ ] Voice chat integration
- [ ] Advanced analytics dashboard
- [ ] Custom embedding models
- [ ] Integration with external knowledge bases
- [ ] Real-time collaboration features

---

Built with ❤️ using modern AI and web technologies.