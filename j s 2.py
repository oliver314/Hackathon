from http.server import *
import socketserver
import socket

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        print("hi")
        try:
            if self.path == "/":
                self.send_file("index.html", "text/html")
            else:
                self.send_file(self.path[1:])

            if self.path == "/"
            
        except Exception as e:
            print(e)

    def do_POST(self):
        print("Hi")
        self.send_response(200)
        length = int(self.headers["content-length"])
        data = self.rfile.read(length)
        print(data)
        #database.insertValues(data)

    def send_file(self, filename, encoding=None):
        with open(filename, "rb") as file:
            self.send_response(200)
            if not encoding:
                self.send_header("Content-type", encoding)
            self.end_headers()
            self.wfile.write(file.read())


if __name__ == "__main__":
    with socketserver.TCPServer(("", 8080), Handler) as httpd:
        print("HTTP server running on port 8080")
        print("Your IP address is: ", socket.gethostbyname(socket.gethostname()))
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(" Recieved Shutting Down")
