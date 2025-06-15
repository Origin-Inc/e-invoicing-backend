# E-Invoicing Backend API

A modern, secure FastAPI-based backend for e-invoicing systems with PostgreSQL and Redis integration.

## 🚀 Features

- **FastAPI Framework**: Modern, fast web framework with automatic API documentation
- **Security First**: Configurable CORS, rate limiting, and secure authentication patterns
- **Database Integration**: PostgreSQL with connection pooling
- **Caching**: Redis for session management and caching
- **Docker Support**: Multi-stage Docker builds with non-root user
- **Testing**: Comprehensive test coverage with pytest
- **Task Management**: Integrated with Task Master for project management

## 🏗️ Architecture

- **API Layer**: FastAPI with versioned endpoints (`/v1/`)
- **Database**: PostgreSQL for persistent data storage
- **Cache**: Redis for session management and rate limiting
- **Containerization**: Docker Compose for development environment

## 🛠️ Tech Stack

- **Backend**: Python 3.11, FastAPI, Uvicorn
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **Testing**: pytest, pytest-asyncio
- **Dependency Management**: Poetry
- **Containerization**: Docker, Docker Compose

## 📋 Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- Poetry (for dependency management)

## 🚀 Quick Start

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/jlitecia/e-invoicing-backend.git
cd e-invoicing-backend
```

2. Start the services:
```bash
docker-compose up --build
```

3. The API will be available at:
   - **API**: http://localhost:8000
   - **API Docs**: http://localhost:8000/docs
   - **Health Check**: http://localhost:8000/v1/health

### Local Development

1. Install dependencies:
```bash
poetry install
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Start the development server:
```bash
poetry run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## 🧪 Testing

Run the test suite:
```bash
# Using Docker
docker-compose exec api pytest

# Local development
poetry run pytest
```

## 📁 Project Structure

```
├── src/
│   ├── main.py              # FastAPI application entry point
│   ├── routers/             # API route handlers
│   │   └── v1/              # Version 1 API endpoints
│   │       └── health.py    # Health check endpoints
│   └── utils/               # Utility modules
│       └── rate_limiting.py # Rate limiting configurations
├── tests/                   # Test files
├── docker-compose.yml       # Docker services configuration
├── Dockerfile              # Multi-stage Docker build
├── pyproject.toml          # Poetry configuration
└── .env                    # Environment variables
```

## ⚙️ Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Database Configuration
POSTGRES_DB=e_invoicing
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres123
DATABASE_URL=postgresql://postgres:postgres123@db:5432/e_invoicing

# Redis Configuration
REDIS_URL=redis://redis:6379

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001

# Environment
ENVIRONMENT=development
```

### Rate Limiting

The API includes configurable rate limiting:

- **Health endpoints**: No rate limiting (for monitoring)
- **General endpoints**: 100 requests per minute
- **Authentication endpoints**: 5 requests per minute (when implemented)

## 🔒 Security Features

- **CORS Protection**: Configurable allowed origins
- **Rate Limiting**: Flexible rate limiting by endpoint type
- **Input Validation**: Automatic request/response validation
- **Error Handling**: Graceful error handling and logging

## 📊 API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔄 Development Workflow

This project uses [Task Master](https://github.com/taskmaster-ai/taskmaster) for project management:

1. View current tasks: Check `.taskmaster/tasks/` directory
2. Track progress: Tasks are organized by priority and dependencies
3. Implementation notes: Detailed in individual task files

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/jlitecia/e-invoicing-backend/issues) page
2. Create a new issue with detailed information
3. Include logs and error messages when applicable

## 🗺️ Roadmap

- [ ] User Authentication & Authorization (Task 3)
- [ ] Invoice Management System
- [ ] PDF Generation
- [ ] Email Notifications
- [ ] API Rate Limiting Enhancements
- [ ] Comprehensive Logging
- [ ] Performance Monitoring

---

**Status**: ✅ Task 1 & 2 Complete - Basic FastAPI structure with security improvements implemented