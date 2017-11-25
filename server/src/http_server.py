from http.server import *
import socketserver
import ssl

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path == "/":
                self.send_file("index.html", "text/html")
            else:
                self.send_file(self.path[1:])

        except Exception as e:
            print(e)

    def send_file(self, filename, encoding=None):
        with open(filename, "rb") as file:
            self.send_response(200)
            if not encoding:
                self.send_header("Content-type", encoding)
            self.end_headers()
            self.wfile.write(file.read())

    def do_POST(self):
        self.send_response(200)
        length = int(self.headers["content-length"])
        data = self.rfile.read(length)
        print(data)
        #database.insertValues(data)


if __name__ == "__main__":
    server = socketserver.TCPServer(("", 8080), Handler)
    server.socket = ssl.wrap_socket(
        server.socket,
        certfile="cert.pem",
        keyfile="key.pem",
        server_side=True)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print(" Recieved Shutting Down")

