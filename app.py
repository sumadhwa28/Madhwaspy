from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from datetime import datetime

from database import init_db, get_db_connection
import market
import portfolio
import news

app = Flask(__name__, template_folder='templates')
CORS(app)

init_db()

@app.route('/')
def index():
    return render_template('index.html')

def validate_token():
    token = request.headers.get('Authorization')
    if not token: 
        return None
    conn = get_db_connection()
    user = conn.execute('SELECT username FROM users WHERE session_token = ?', (token,)).fetchone()
    conn.close()
    return user['username'] if user else None

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    hashed_pw = generate_password_hash(data['password'])
    try:
        conn = get_db_connection()
        conn.execute('INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)',
                     (data['username'], hashed_pw, datetime.now().isoformat()))
        conn.commit()
        return jsonify({"message": "User created"}), 201
    except:
        return jsonify({"error": "Username already exists"}), 400

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (data['username'],)).fetchone()
    
    if user and check_password_hash(user['password_hash'], data['password']):
        token = str(uuid.uuid4())
        conn.execute('UPDATE users SET session_token = ?, last_login = ? WHERE username = ?',
                     (token, datetime.now().isoformat(), data['username']))
        conn.commit()
        return jsonify({"token": token, "username": data['username']})
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/api/portfolio', methods=['GET'])
def get_portfolio():
    user = validate_token()
    if not user: return jsonify({"error": "Unauthorized"}), 401
    return jsonify(portfolio.calculate_metrics(user))

@app.route('/api/portfolio/add', methods=['POST'])
def add_transaction():
    user = validate_token()
    if not user: return jsonify({"error": "Unauthorized"}), 401
    
    data = request.json
    prices = market.get_live_prices()
    current_price = prices.get(data['asset_type'])
    total = current_price * data['grams']

    if data['type'] == 'sell':
        current_holdings = portfolio.calculate_metrics(user)
        asset_data = next((item for item in current_holdings['assets'] if item["asset"] == data['asset_type']), None)
        if not asset_data or asset_data['holdings_grams'] < data['grams']:
            return jsonify({"error": "Insufficient holdings"}), 400

    conn = get_db_connection()
    conn.execute('''INSERT INTO transactions 
                 (username, asset_type, grams, price_per_gram, total_invested_inr, type, timestamp)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''',
                 (user, data['asset_type'], data['grams'], current_price, total, data['type'], datetime.now().isoformat()))
    conn.commit()
    return jsonify({"message": "Transaction recorded", "total_inr": total})

@app.route('/api/portfolio/history', methods=['GET'])
def get_portfolio_history_api():
    user = validate_token()
    if not user: return jsonify({"error": "Unauthorized"}), 401
    return jsonify(portfolio.get_portfolio_history(user))

@app.route('/api/news', methods=['GET'])
def get_news():
    asset = request.args.get('asset', 'gold')
    return jsonify(news.get_market_news(asset))

if __name__ == '__main__':
    app.run(debug=True, port=5000)