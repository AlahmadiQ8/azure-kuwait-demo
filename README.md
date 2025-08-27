# Kuwait Fine Dining

A modern restaurant directory web application for Kuwait, showcasing local dining spots from traditional Kuwaiti kitchens to modern fusion concepts. This application helps users discover and explore the vibrant culinary landscape of Kuwait.

## 🚀 Technology Stack

- **Backend**: Flask REST API with SQLAlchemy ORM and Flask-OpenAPI3 for automatic documentation
- **Frontend**: Astro with Svelte components for interactivity
- **Styling**: Tailwind CSS with dark mode theme
- **Database**: SQLite with SQLAlchemy ORM
- **Testing**: Python unittest for backend, Playwright for end-to-end frontend tests
- **Development**: Python virtual environment and Node.js

## 📋 Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Python 3.8+**: For the Flask backend
- **Node.js 18+**: For the Astro/Svelte frontend
- **npm**: Comes with Node.js installation
- **Git**: For version control

## 🛠️ Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/AlahmadiQ8/azure-kuwait-demo.git
cd azure-kuwait-demo
```

### 2. Automatic Setup and Launch

We provide a convenient script that sets up the entire environment and launches both servers:

```bash
./scripts/start-app.sh
```

This script will:
- Create and activate a Python virtual environment
- Install all Python dependencies
- Install all Node.js dependencies
- Start the Flask API server on port 5100
- Start the Astro development server on port 4321

After running the script, navigate to:
- **Frontend**: [http://localhost:4321](http://localhost:4321)
- **API Documentation**: [http://localhost:5100](http://localhost:5100)

### 3. Manual Setup (Alternative)

If you prefer to set up manually:

```bash
# Setup environment and dependencies
./scripts/setup-env.sh

# Activate virtual environment (if not already active)
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Start backend server
cd server
python app.py

# In a new terminal, start frontend server
cd client
npm run dev
```

## 📁 Project Structure

```
azure-kuwait-demo/
├── server/                 # Flask backend application
│   ├── models/            # SQLAlchemy ORM models
│   │   ├── restaurant.py  # Restaurant data model
│   │   ├── category.py    # Category data model
│   │   └── base.py        # Base model configuration
│   ├── routes/            # API endpoints organized by resource
│   │   ├── restaurants.py # Restaurant CRUD endpoints
│   │   └── publishers.py  # Publisher endpoints
│   ├── tests/             # Unit tests for the API
│   ├── utils/             # Utility functions and database helpers
│   ├── app.py             # Flask application entry point
│   └── requirements.txt   # Python dependencies
├── client/                # Astro/Svelte frontend application
│   ├── src/
│   │   ├── components/    # Reusable Svelte components
│   │   ├── layouts/       # Astro layout templates
│   │   ├── pages/         # Astro page routes
│   │   └── styles/        # CSS and Tailwind configuration
│   ├── e2e-tests/         # Playwright end-to-end tests
│   ├── package.json       # Node.js dependencies and scripts
│   └── playwright.config.ts # Playwright test configuration
├── scripts/               # Development and deployment scripts
│   ├── setup-env.sh       # Environment setup script
│   ├── start-app.sh       # Launch both servers script
│   └── run-server-tests.sh # Run backend tests script
├── data/                  # Database files
└── docs/                  # Project documentation
```

## 🧪 Testing

### Backend Tests

Run all Python unit tests:

```bash
./scripts/run-server-tests.sh
```

Or manually:

```bash
source venv/bin/activate
cd server
python -m unittest discover tests/
```

### Frontend Tests

Run end-to-end tests with Playwright:

```bash
cd client
npm run test:e2e
```

Build the frontend to check for issues:

```bash
cd client
npm run build
```

## 🔧 Development Workflow

### Before Making Changes

1. **Run tests** to ensure everything is working:
   ```bash
   ./scripts/run-server-tests.sh
   cd client && npm run build && npm run test:e2e
   ```

2. **Start development servers** for testing:
   ```bash
   ./scripts/start-app.sh
   ```

### Code Standards

- **Python**: Use type hints, docstrings, and follow PEP 8
- **Frontend**: Use Svelte for interactive components, Astro for pages
- **Styling**: Use Tailwind CSS classes, maintain dark mode theme
- **API**: Follow RESTful design principles
- **Database**: Use SQLAlchemy models and migrations when needed

### Available Scripts

| Script | Purpose |
|--------|---------|
| `./scripts/setup-env.sh` | Install all Python and Node.js dependencies |
| `./scripts/start-app.sh` | Launch both backend and frontend development servers |
| `./scripts/run-server-tests.sh` | Run Python unit tests |

### Making API Changes

1. Update or create models in `server/models/`
2. Update routes in `server/routes/`
3. Add/update tests in `server/tests/`
4. Run tests to ensure functionality works
5. API documentation is automatically generated via Flask-OpenAPI3

## 🌐 API Documentation

The API uses Flask-OpenAPI3 for automatic documentation. When the backend server is running, visit:

- **Swagger UI**: [http://localhost:5100](http://localhost:5100)

Current API endpoints:
- `GET /restaurants` - List all restaurants
- `GET /restaurants/{id}` - Get restaurant by ID  
- `POST /restaurants` - Create new restaurant
- `PUT /restaurants/{id}` - Update restaurant
- `DELETE /restaurants/{id}` - Delete restaurant

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes following the code standards
4. Run tests and ensure they pass
5. Commit your changes: `git commit -m 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

For detailed contributing guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md).

## 📄 Additional Documentation

- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Security Policy](SECURITY.md)
- [Support](SUPPORT.md)
- [Development Guidelines](.github/copilot-instructions.md)

## 🐛 Troubleshooting

### Common Issues

**Port conflicts**: If ports 4321 or 5100 are in use, the scripts will show an error. Stop any running services on these ports.

**Permission errors**: On Unix systems, you may need to make scripts executable:
```bash
chmod +x scripts/*.sh
```

**Python virtual environment**: If you encounter Python import errors, ensure the virtual environment is activated:
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**Node.js dependencies**: If npm install fails, try clearing the cache:
```bash
cd client
npm cache clean --force
npm install
```

## 📞 Support

If you encounter issues or have questions:

1. Check the [troubleshooting section](#-troubleshooting) above
2. Search existing [GitHub issues](https://github.com/AlahmadiQ8/azure-kuwait-demo/issues)
3. Create a new issue with detailed information about your problem

## 📜 License

This project is licensed under the terms of the [LICENSE](LICENSE) file.

