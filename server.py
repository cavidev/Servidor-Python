__author__ = 'Carlos Mario'
import web

urls = (
  '/', 'index'    )

class index:
    def GET(self):
        print ("Hello, world!")

if __name__ == "__main__": web.run(urls, globals())



# from http.server import  BaseHTTPRequestHandler, HTTPServer
#
# class http_server:
#     def __init__(self):
#         server = HTTPServer(('', 5050), myHandler)
#         server.serve_forever()
#
# class myHandler(BaseHTTPRequestHandler):
#     def do_GET(self):
#         self.send_response(200)
#         self.send_header('Content-type','text/html')
#         self.end_headers()
#         # Hacer lo que queramos con la petición
#         return
#
# class main:
#     def __init__(self):
#         self.server = http_server()
#
#
# if __name__ == '__main__':
#     m = main()