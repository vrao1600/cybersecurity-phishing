from flask import Flask, request, render_template, redirect
import mysql.connector
import datetime

# Flask app setup
app = Flask(__name__)

# MySQL Database Configuration
db_config = {
    'user': 'root',
    'password': 'password',
    'host': 'localhost',
    'database': 'phishing_simulation'
}

# Establishing MySQL connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Phishing route
@app.route('/phish')
def phish():
    user_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Log interaction to the MySQL database
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO interactions (ip, user_agent, timestamp) VALUES (%s, %s, %s)"
    cursor.execute(query, (user_ip, user_agent, timestamp))
    conn.commit()
    cursor.close()
    conn.close()

    # Display a fake login page
    return render_template('phishing_page.html')

# Admin route to view logs (for internal use)
@app.route('/admin')
def admin():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM interactions")
    logs = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('admin.html', logs=logs)

# Initialize the MySQL database
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            ip VARCHAR(50),
            user_agent VARCHAR(255),
            timestamp DATETIME
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

# Start the Flask application
if __name__ == '__main__':
    init_db()
    app.run(host='127.0.0.1', port=5000)
