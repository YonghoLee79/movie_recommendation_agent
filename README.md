# 🎬 Movie Recommendation Agent

A robust AI-powered Flask application that provides personalized movie recommendations using OpenAI's GPT models. The application features secure user input validation, conversation persistence, comprehensive error handling, and production-ready configuration.

## 🌟 Features

- **AI-Powered Recommendations**: Uses OpenAI GPT models for intelligent movie suggestions
- **Persistent Conversations**: SQLite database storage for conversation history across sessions
- **Secure Input Validation**: Sanitization and validation of user inputs to prevent injection attacks
- **Comprehensive Error Handling**: Graceful handling of API errors and edge cases
- **Structured Logging**: Detailed logging for monitoring and debugging
- **Environment-based Configuration**: Secure configuration management with environment variables
- **Production Ready**: Gunicorn configuration and deployment-ready setup
- **Responsive UI**: Modern Bootstrap-based chat interface with dark mode
- **Session Management**: Unique session IDs for tracking individual conversations

## 🛠️ Technical Improvements

This application includes several security and reliability enhancements:

1. **Environment Variable Validation**: Validates required API keys on startup
2. **Model Versioning**: Configurable OpenAI model selection via environment variables
3. **Database Persistence**: Conversation history stored in SQLite with proper error handling
4. **Input Sanitization**: User input is validated, escaped, and length-limited
5. **API Error Handling**: Graceful handling of OpenAI API failures and network issues
6. **Security Features**: Session management, debug mode control, and input validation
7. **Logging**: Structured logging with configurable levels
8. **Testing**: Comprehensive unit tests for core functionality

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key

### Installation

1️⃣ **Clone the repository**
```bash
git clone https://github.com/YonghoLee79/movie_recommendation_agent.git
cd movie_recommendation_agent
```

2️⃣ **Install dependencies**
```bash
pip install -r requirements.txt
```

3️⃣ **Configure environment**
```bash
# Copy the environment template
cp .env.template .env

# Edit .env file and add your OpenAI API key
# OPENAI_API_KEY=your_openai_api_key_here
```

4️⃣ **Run the application**
```bash
# Development mode
python app.py

# Production mode with Gunicorn
gunicorn -c gunicorn.conf.py app:app
```

## 🔧 Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | Yes | - | Your OpenAI API key |
| `OPENAI_MODEL` | No | `gpt-4o` | OpenAI model to use |
| `SECRET_KEY` | No | `dev-secret-key-change-in-production` | Flask session secret |
| `DATABASE_URL` | No | `conversations.db` | Database connection string |
| `DEBUG` | No | `False` | Enable debug mode |
| `PORT` | No | `5000` | Application port |

### Database Configuration

The application uses SQLite by default but can be configured for other databases:

- **SQLite**: `DATABASE_URL=conversations.db`
- **PostgreSQL**: `DATABASE_URL=postgresql://user:password@localhost/dbname`

## 🧪 Testing

Run the test suite to verify functionality:

```bash
# Run all tests
python -m unittest test_app.py -v

# Run specific test
python -m unittest test_app.TestMovieRecommendationApp.test_input_validation -v
```

## 🚀 Production Deployment

### Using Gunicorn

```bash
# Install gunicorn (included in requirements.txt)
pip install gunicorn

# Run with production configuration
gunicorn -c gunicorn.conf.py app:app
```

### Environment Setup for Production

1. Set a strong `SECRET_KEY`
2. Configure `DEBUG=False`
3. Use environment-specific `DATABASE_URL`
4. Set appropriate log levels
5. Configure reverse proxy (nginx recommended)

### Example Production Commands

```bash
# Set production environment
export OPENAI_API_KEY="your-production-api-key"
export SECRET_KEY="your-very-secure-secret-key"
export DEBUG=False
export PORT=8000

# Run with Gunicorn
gunicorn -c gunicorn.conf.py app:app
```

## 📁 Project Structure

```
movie_recommendation_agent/
├── app.py                 # Main Flask application
├── test_app.py           # Unit tests
├── requirements.txt      # Python dependencies
├── gunicorn.conf.py     # Gunicorn production configuration
├── .env.template        # Environment variables template
├── templates/
│   └── chat.html        # Chat interface template
├── static/
│   └── style.css        # Additional styles
└── README.md           # This file
```

## 🔒 Security Considerations

- **Input Validation**: All user inputs are sanitized and validated
- **API Key Protection**: API keys are loaded from environment variables
- **Session Security**: Flask sessions use configurable secret keys
- **Debug Mode**: Debug mode is disabled by default and configurable
- **Error Handling**: Detailed errors are logged but not exposed to users

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`python -m unittest test_app.py`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Troubleshooting

### Common Issues

**"OPENAI_API_KEY environment variable is not set"**
- Ensure you've created a `.env` file with your API key
- Check that the `.env` file is in the correct directory

**Database errors**
- Ensure the application has write permissions to create the SQLite database
- Check that the `DATABASE_URL` is correctly formatted

**Import errors**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version compatibility (3.8+)

### Getting Help

- Check the application logs for detailed error messages
- Review the test suite for expected behavior examples
- Open an issue on GitHub for bugs or feature requests
