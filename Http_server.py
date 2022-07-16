from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import codecs
import cgi
import base64
hostName = "localhost"
serverPort = 7878


class MyServer(BaseHTTPRequestHandler):
    
    def do_GET(self):
        if self.path.endswith("/home"):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            output=""
            output+="<html><head><title>Task</title></head>"
            output+='<p><h1>Given Hex-Code</h1>(0x38 0x39 0x20 0x35 0x30 0x20 0x37 0x30 0x20 0x34 0x38 )</p>'
            output+="<body>"
            output+='<form action="/success" method="POST" enctype="multipart/form-data">'
            output+='<input type="text" name="name" id="name" placeholder="Enter your name" style="height:200px;font-size:14pt; margin:10px ; border: 2px solid red;border-radius: 25px;padding:60pxs;">'
            output+='<input type="submit" value="Decode the Hexa-Value" style="background-color: white;height:50px;font-size:14pt;border: 2px solid #4CAF50;">'
            output+="</form>"
            self.wfile.write(output.encode("utf-8"))
    def do_POST(self):
        if self.path == '/success':
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                name = fields.get("name")[0]
                self.a=''
            self.hex_code=['0x38','0x39','0x20','0x35','0x30','0x20','0x37','0x30','0x20','0x34','0x38']
            for i in self.hex_code:
                self.a+=bytes.fromhex(i[2:]).decode('utf-8')
            self.a=self.a.split(" ")
            self.c=""
            self.b=[chr(int(j)) for j in self.a]
            for k in self.b:
                self.c+=k
            print(type(self.c))
            self.base64_string =self.c
            self.base64_bytes =self.base64_string.encode("ascii")
            self.sample_string_bytes = base64.b64decode(self.base64_bytes)
            self.sample_string = self.sample_string_bytes.decode("ascii")
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html><head><title>Task</title></head>", "utf-8"))
            self.wfile.write(bytes("<p><h1>Given Hex-Code</h1>(0x38 0x39 0x20 0x35 0x30 0x20 0x37 0x30 0x20 0x34 0x38 )</p>" , "utf-8"))
            self.wfile.write(bytes("<body><h1>Hi  "+name+"</h1>", "utf-8"))
            self.wfile.write(bytes("<h4>Decode Vlue: </h4><h1 style='color:red;'>" +str(self.sample_string)+"</h1>", "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))
if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
