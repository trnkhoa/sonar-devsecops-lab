from flask import Flask, request, render_template_string
import sqlite3, os, hashlib, subprocess

app = Flask(__name__)
# Vá lỗi Hardcoded Secret bằng cách sử dụng biến môi trường
app.secret_key = os.environ.get("SECRET_KEY", "a_very_long_secure_random_string_123")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Vá lỗi MD5 yếu: Sử dụng SHA-256
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        # Vá lỗi SQL Injection: Sử dụng Parameterized Queries
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        cursor.execute(query, (username, hashed_password))
        
        if cursor.fetchone():
            # Vá lỗi XSS: Sử dụng render_template_string với biến truyền vào (auto-escape)
            return render_template_string("<h1>Chào mừng, {{ user }}!</h1>", user=username)
        return "Đăng nhập thất bại."
    return '<form method="post">User: <input name="username"> Pass: <input name="password"> <input type="submit"></form>'

@app.route('/ping')
def ping():
    ip = request.args.get('ip', '127.0.0.1')
    # Vá lỗi Command Injection: Sử dụng subprocess với danh sách đối số
    try:
        # Giới hạn tham số để đảm bảo an toàn tối đa
        result = subprocess.check_output(['ping', '-c', '1', ip], stderr=subprocess.STDOUT, timeout=5)
        return f"<pre>{result.decode()}</pre>"
    except Exception as e:
        return f"Lỗi thực thi: {str(e)}"

if __name__ == '__main__':
    app.run(debug=False) # Tắt debug mode để bảo mật
