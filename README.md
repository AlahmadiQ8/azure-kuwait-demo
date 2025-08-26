# Kuwait Fine Dining

A restaurant directory for Kuwait with a culinary theme, highlighting local dining spots ranging from traditional Kuwaiti kitchens to modern fusion concepts. Built with modern web technologies to provide an elegant dining discovery experience.

![Kuwait Fine Dining](https://img.shields.io/badge/Kuwait-Fine_Dining-blue)
![Flask](https://img.shields.io/badge/Flask-API-green)
![Astro](https://img.shields.io/badge/Astro-Frontend-orange)
![Svelte](https://img.shields.io/badge/Svelte-Components-red)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-Styling-blue)

## 🚀 Technology Stack

### Backend
- **Flask** - Python web framework for the API
- **SQLAlchemy** - ORM for database interactions
- **Flask-OpenAPI3** - OpenAPI documentation
- **Flask-CORS** - Cross-origin resource sharing
- **Pydantic** - Data validation

### Frontend
- **Astro** - Static site generator for page routing and content
- **Svelte** - Interactive components and reactive programming
- **Tailwind CSS** - Utility-first CSS styling with dark mode theme
- **TypeScript** - Type-safe JavaScript

### Testing & Development
- **Playwright** - End-to-end testing for the frontend
- **unittest** - Python unit testing for backend
- **Custom scripts** - Development automation

## 📋 Prerequisites

Before running this project, ensure you have:

- **Python 3.8+** installed
- **Node.js 18+** and **npm** installed
- **Git** for version control

## 🛠️ Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/AlahmadiQ8/azure-kuwait-demo.git
cd azure-kuwait-demo
```

### 2. Run the Application
We provide a convenience script that handles all setup and starts both servers:

```bash
./scripts/start-app.sh
```

This script will:
- Create and activate a Python virtual environment
- Install Python dependencies
- Install Node.js dependencies
- Start the Flask API server on `http://localhost:5100`
- Start the Astro frontend server on `http://localhost:4321`

### 3. Access the Application
- **Frontend**: Navigate to [http://localhost:4321](http://localhost:4321)
- **Backend API**: Available at [http://localhost:5100](http://localhost:5100)

## 🏗️ Project Structure

```
azure-kuwait-demo/
├── server/                 # Flask backend
│   ├── models/            # SQLAlchemy ORM models
│   ├── routes/            # API endpoints (Flask blueprints)
│   ├── tests/             # Backend unit tests
│   ├── utils/             # Utility functions
│   ├── app.py             # Flask application entry point
│   └── requirements.txt   # Python dependencies
├── client/                # Astro/Svelte frontend
│   ├── src/
│   │   ├── components/    # Reusable Svelte components
│   │   ├── layouts/       # Astro layout templates
│   │   ├── pages/         # Astro page routes
│   │   └── styles/        # CSS and Tailwind configuration
│   ├── e2e-tests/        # Playwright end-to-end tests
│   └── package.json       # Node.js dependencies
├── scripts/               # Development automation scripts
│   ├── setup-env.sh       # Environment setup
│   ├── start-app.sh       # Start both servers
│   └── run-server-tests.sh # Run backend tests
├── data/                  # Database files
└── docs/                  # Additional documentation
```

## 🔧 Development Scripts

| Script | Description | Usage |
|--------|-------------|-------|
| `setup-env.sh` | Install all Python and Node.js dependencies | `./scripts/setup-env.sh` |
| `start-app.sh` | Setup environment and start both servers | `./scripts/start-app.sh` |
| `run-server-tests.sh` | Setup environment and run backend tests | `./scripts/run-server-tests.sh` |

## 🧪 Running Tests

### Backend Tests (Python)
```bash
# Run all backend tests
./scripts/run-server-tests.sh

# Or run tests manually after setup
cd server
python -m unittest discover -s tests
```

### Frontend Tests (Playwright E2E)
```bash
cd client
# Install Playwright browsers (first time only)
npx playwright install
# Run the tests
npm run test:e2e
```

## 🏃‍♂️ Manual Development Setup

If you prefer to set up the environment manually:

### Backend Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
cd server
pip install -r requirements.txt

# Start Flask server
export FLASK_DEBUG=1
export FLASK_PORT=5100
python app.py
```

### Frontend Setup
```bash
cd client
npm install
npm run dev  # Starts on http://localhost:4321
```

## 🏗️ Building for Production

### Backend
The Flask application can be deployed using a production WSGI server like Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5100 server.app:app
```

### Frontend
```bash
cd client
npm run build    # Build static files
npm run preview  # Preview production build
```

## 🎨 Design & Styling

- **Theme**: Dark mode with modern UI/UX
- **Styling**: Tailwind CSS utility classes
- **Components**: Reusable Svelte components
- **Layout**: Responsive design with rounded corners and clean interfaces

## 📚 API Documentation

The Flask backend uses OpenAPI3 for automatic API documentation. When the server is running, visit:
- OpenAPI docs: `http://localhost:5100/openapi.json`

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Before Contributing
1. Run backend tests: `./scripts/run-server-tests.sh`
2. Run frontend build: `cd client && npm run build`
3. Run e2e tests: `cd client && npm run test:e2e`
4. Follow our code formatting requirements (type hints, docstrings)

## 🔒 Security & Support

- **Security**: See [SECURITY.md](SECURITY.md)
- **Support**: See [SUPPORT.md](SUPPORT.md)
- **Code of Conduct**: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

## 📄 License

This project is licensed under the terms specified in [LICENSE](LICENSE).

---

**Enjoy exploring Kuwait's finest dining experiences! 🍽️**

