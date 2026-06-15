from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class DebugWebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        print("\n" + "="*50)
        print("🚨 WEBHOOK RECEIVED! 🚨")
        print("="*50)
        print(f"Headers:\n{self.headers}")
        try:
            payload = json.loads(post_data.decode('utf-8'))
            print(f"Payload:\n{json.dumps(payload, indent=2)}")
        except Exception as e:
            print(f"Raw Data (Could not parse JSON): {post_data.decode('utf-8')}")
        print("="*50 + "\n")
        
        # Send a clean 200 OK back to Vikunja
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(b'{"status":"success"}')

def run(port=5000):
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, DebugWebhookHandler)
    print(f"🟢 Isolated debug server listening on port {port}...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping debug server.")

if __name__ == '__main__':
    run()