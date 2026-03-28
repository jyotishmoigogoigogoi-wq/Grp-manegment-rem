"""
˹ʀᴇᴍ˼ Bot Keep Alive Module
Flask server to prevent Render sleep
"""

from flask import Flask, jsonify
from threading import Thread
import logging

from config import RENDER_PORT, BOT_NAME, DEVELOPER_NAME

# Suppress Flask logs
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)


@app.route('/')
def home():
    """Home page - bot status"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{BOT_NAME} - Status</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                color: #fff;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                margin: 0;
            }}
            .container {{
                text-align: center;
                padding: 40px;
                background: rgba(255, 255, 255, 0.05);
                border-radius: 20px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
            }}
            h1 {{
                font-size: 3em;
                margin-bottom: 10px;
                background: linear-gradient(45deg, #ff6b6b, #feca57);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }}
            .status {{
                display: inline-flex;
                align-items: center;
                gap: 10px;
                padding: 10px 20px;
                background: rgba(0, 255, 0, 0.1);
                border-radius: 50px;
                margin: 20px 0;
            }}
            .status-dot {{
                width: 12px;
                height: 12px;
                background: #00ff00;
                border-radius: 50%;
                animation: pulse 2s infinite;
            }}
            @keyframes pulse {{
                0%, 100% {{ opacity: 1; }}
                50% {{ opacity: 0.5; }}
            }}
            .info {{
                margin-top: 30px;
                color: #888;
                font-size: 0.9em;
            }}
            .info a {{
                color: #feca57;
                text-decoration: none;
            }}
            .info a:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{BOT_NAME}</h1>
            <div class="status">
                <div class="status-dot"></div>
                <span>Online</span>
            </div>
            <p>Your ultimate anime & group management companion!</p>
            <div class="info">
                <p>Developed by <a href="https://t.me/YorichiiPrime" target="_blank">{DEVELOPER_NAME}</a></p>
                <p>Platform: Render.com | Database: Neon PostgreSQL</p>
            </div>
        </div>
    </body>
    </html>
    """


@app.route('/ping')
def ping():
    """Simple ping endpoint for uptime monitoring"""
    return jsonify({
        "status": "alive",
        "bot": BOT_NAME,
        "developer": DEVELOPER_NAME,
        "timestamp": __import__('time').time()
    })


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "bot": BOT_NAME,
        "services": {
            "web_server": "running",
            "bot": "running"
        }
    })


def run():
    """Run Flask server"""
    app.run(
        host='0.0.0.0',
        port=RENDER_PORT,
        debug=False,
        use_reloader=False
    )


def keep_alive():
    """Start keep-alive server in a thread"""
    server = Thread(target=run, daemon=True)
    server.start()
    print(f"[Keep Alive] Server started on port {RENDER_PORT}")
