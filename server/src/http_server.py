from http.server import *
import socketserver
import ssl

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            self.homepage()
        except Exception as e:
            print(e)

    def homepage(self):
        with open("index.html", "rb") as file:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(file.read())



if __name__ == "__main__":
    server = socketserver.TCPServer(("", 80), Handler)
    server.socket = ssl.wrap_socket(
        server.socket,
        certfile="cert.pem",
        keyfile="key.pem",
        server_side=True)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print(" Recieved Shutting Down")

