import os
import sys
import logging
import sqlite3
from datetime import datetime
from flask import Flask, request, render_template, session
from markupsafe import escape
from openai import OpenAI
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

# Database configuration
DATABASE_URL = os.environ.get("DATABASE_URL", "conversations.db")

def init_database():
    """Initialize the database and create tables if they don't exist"""
    try:
        conn = sqlite3.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")

def save_message_to_db(session_id, role, content):
    """Save a message to the database"""
    try:
        conn = sqlite3.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO conversations (session_id, role, content) VALUES (?, ?, ?)",
            (session_id, role, content)
        )
        
        conn.commit()
        conn.close()
        logger.debug(f"Message saved to database: {role}")
    except Exception as e:
        logger.error(f"Failed to save message to database: {e}")

def load_conversation_from_db(session_id):
    """Load conversation history from database"""
    try:
        conn = sqlite3.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT role, content FROM conversations WHERE session_id = ? ORDER BY timestamp",
            (session_id,)
        )
        
        messages = []
        for row in cursor.fetchall():
            messages.append({"role": row[0], "content": row[1]})
        
        conn.close()
        
        # Always start with system message if not present
        if not messages or messages[0]["role"] != "system":
            system_message = {"role": "system", "content": SYSTEM_PROMPT}
            messages.insert(0, system_message)
            save_message_to_db(session_id, "system", SYSTEM_PROMPT)
        
        return messages
    except Exception as e:
        logger.error(f"Failed to load conversation from database: {e}")
        return [{"role": "system", "content": SYSTEM_PROMPT}]

# Environment variable handling with error checking
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.error("OPENAI_API_KEY environment variable is not set")
    sys.exit(1)

# Model versioning - allow dynamic model selection
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o")
DEBUG_MODE = os.environ.get("DEBUG", "False").lower() in ("true", "1", "yes")

try:
    client = OpenAI(api_key=OPENAI_API_KEY)
    logger.info("OpenAI client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize OpenAI client: {e}")
    sys.exit(1)

SYSTEM_PROMPT = "You are a movie recommendation assistant. Recommend movies based on user requests."

# Initialize database on startup
init_database()

def validate_user_input(user_message):
    """Validate and sanitize user input"""
    if not user_message:
        return None
    
    # Basic sanitization - remove excessive whitespace and limit length
    user_message = user_message.strip()
    if len(user_message) > 1000:  # Reasonable limit for messages
        user_message = user_message[:1000]
    
    if not user_message:
        return None
        
    return escape(user_message)

def get_assistant_reply(user_message, session_id):
    """Get assistant reply with error handling and database persistence"""
    try:
        # Validate input
        validated_message = validate_user_input(user_message)
        if not validated_message:
            logger.warning("Invalid or empty user message received")
            return "Please provide a valid message."
        
        # Load conversation history from database
        conversation_history = load_conversation_from_db(session_id)
        
        # Add user message to conversation and database
        conversation_history.append({"role": "user", "content": validated_message})
        save_message_to_db(session_id, "user", validated_message)
        logger.info(f"User message added to conversation: {validated_message[:50]}...")
        
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=conversation_history
        )
        
        assistant_reply = response.choices[0].message.content
        
        # Add assistant reply to conversation and database
        conversation_history.append({"role": "assistant", "content": assistant_reply})
        save_message_to_db(session_id, "assistant", assistant_reply)
        
        logger.info(f"Assistant reply generated: {assistant_reply[:50]}...")
        return assistant_reply
        
    except Exception as e:
        error_msg = f"Error generating response: {str(e)}"
        logger.error(error_msg)
        error_response = "I'm sorry, I'm having trouble processing your request right now. Please try again later."
        
        # Save error response to database
        save_message_to_db(session_id, "assistant", error_response)
        
        return error_response

@app.route("/", methods=["GET", "POST"])
def chat():
    """Main chat route with error handling and session management"""
    try:
        # Generate session ID if not exists
        if "session_id" not in session:
            session["session_id"] = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.urandom(4).hex()}"
            logger.info(f"New session created: {session['session_id']}")
        
        session_id = session["session_id"]
        
        if request.method == "POST":
            user_input = request.form.get("message", "").strip()
            if user_input:
                logger.info(f"Processing POST request with user input for session {session_id}")
                assistant_reply = get_assistant_reply(user_input, session_id)
            else:
                logger.warning("Empty message received in POST request")
        
        # Load conversation history for display
        conversation_history = load_conversation_from_db(session_id)
        
        return render_template("chat.html", messages=conversation_history)
    
    except Exception as e:
        logger.error(f"Error in chat route: {e}")
        # Return error page or basic response
        error_message = {"role": "assistant", "content": "Sorry, there was an error processing your request."}
        conversation_history = [{"role": "system", "content": SYSTEM_PROMPT}, error_message]
        return render_template("chat.html", messages=conversation_history)

if __name__ == "__main__":
    logger.info(f"Starting Flask app in {'DEBUG' if DEBUG_MODE else 'PRODUCTION'} mode")
    logger.info(f"Using OpenAI model: {OPENAI_MODEL}")
    app.run(debug=DEBUG_MODE, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))




