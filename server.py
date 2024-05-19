import http.server
import socketserver
import datetime

PORT = 8080

AUTHOR_NAME = "John Doe"

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    
    def do_GET(self):
        client_ip = self.client_address[0]
        
        message = "Witaj! Twój adres IP to: {}\n".format(client_ip)
        message += "Data i godzina w twojej strefie czasowej: {}\n".format(datetime.datetime.now())
        
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        self.wfile.write(bytes(message, "utf8"))
        return

log_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"Serwer uruchomiony przez: {AUTHOR_NAME}")
print(f"Data uruchomienia: {log_date}")
print(f"Serwer nasłuchuje na porcie: {PORT}")

with socketserver.TCPServer(("", PORT), MyHttpRequestHandler) as httpd:
    httpd.serve_forever()
