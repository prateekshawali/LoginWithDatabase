import http.server
import socketserver
import json
import mysql.connector
from mysql.connector import Error

PORT = 8000

# Database connection details
DB_CONFIG = {
    'user': 'root',        
    'password': 'prativk@2719', 
    'host': 'localhost',
    'database': 'login'
}

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = 'login.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        if self.path == '/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            response = self.handle_login(json.loads(post_data))
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        # else:
        #     self.send_response(405)
        #     self.end_headers()

    def handle_login(self, data):
        username = data.get('username')
        password = data.get('password')

        try:
            # Connect to the database
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()

            cursor.close()
            conn.close()

            if user:
                return {"status": "success", "message": "Login successful"}
            else:
                return {"status": "failure", "message": "Invalid credentials"}

        except Error as e:
            print(f"Error: {e}")
            return {"status": "error", "message": "An error occurred"}

Handler = MyRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
