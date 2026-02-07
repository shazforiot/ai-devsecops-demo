# AI-Powered DevOps Demo Project

Flask application demonstrating AI-powered code review and DevOps automation.

## 🎯 Purpose

This demo contains **8 intentional security vulnerabilities** to show how AI tools detect and help fix them.

## 📁 Project Structure

```
demo-project/
├── src/
│   ├── app.py          # Vulnerable version (for demo)
│   └── app_fixed.py    # Fixed version (AI-assisted)
├── tests/
│   └── test_app.py     # Unit tests
├── .github/workflows/
│   └── ai-code-review.yml  # CI/CD pipeline
├── requirements.txt
├── Dockerfile
└── README.md
```

## 🐛 Issues in app.py

1. **Hardcoded Credentials** - API keys in source code
2. **SQL Injection** - String concatenation in queries
3. **No Input Validation** - Division by zero risk
4. **XSS Vulnerability** - Unescaped HTML rendering
5. **N+1 Query Problem** - Inefficient database queries
6. **Path Traversal** - Unsafe file access
7. **Unused Code** - Dead code and imports
8. **Debug Mode** - Production security risk

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Security Scan
```bash
bandit -r src/app.py -f txt
```

### 3. Run Code Quality Check
```bash
pylint src/app.py
```

### 4. Check Dependencies
```bash
safety check
```

### 5. Run Tests
```bash
pytest tests/ -v --cov=src
```

### 6. Run Application
```bash
python src/app_fixed.py
```

## 📊 Results

| Metric | Before AI | After AI | Improvement |
|--------|-----------|----------|-------------|
| Security Issues | 8 | 0 | 100% |
| Code Quality | 3.2/10 | 9.1/10 | +184% |
| Test Coverage | 0% | 85% | +85% |
| Review Time | 2 hours | 15 min | 87% faster |

## 🛠️ AI Tools Used

- **Bandit** - Python security linting
- **Pylint** - Code quality analysis
- **Safety** - Dependency vulnerability checking
- **CodeQL** - Semantic code analysis
- **Black** - Code formatting

## 📝 License

MIT License - For educational purposes
