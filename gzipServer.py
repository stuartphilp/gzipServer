#!/c/mozilla-build/python/python.exe
#
# Usage: gzipServer.py [port number to listen on]
#
# Default port number is 80
#
import time
import sys
import BaseHTTPServer
import gzip
import simplejson as json
import argparse

HOST_NAME = '127.0.0.1'

gPort = 80
gReportCount = 0

class HTTPHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    #
    # Boilerplate web server, for testing with browser
    #
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
        global gArgs
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write("<html>")
        s.wfile.write("  <head><title>Success</title></head>")
        s.wfile.write("  <body>")
        s.wfile.write("    <p>The server is working correctly. Firefox should send a POST request on port %d</p>" % gArgs.port)
        s.wfile.write("  </body>")
        s.wfile.write("</html>")

    def do_POST(s):
      global gReportCount
      global gArgs
      gReportCount += 1

      length = int(s.headers["Content-Length"])
      postData = s.rfile.read(length)
      plainData = ""
      if "Content-Encoding" in s.headers and s.headers["Content-Encoding"] == "gzip":
        gzData = postData
        gzFile = open('temp.gz', 'wb')
        gzFile.write(gzData)
        gzFile.close()
        unzippedFile = gzip.open('temp.gz', 'rb')
        plainData = unzippedFile.read()
        unzippedFile.close()
      else:
        plainData = postData

      filename = "report" + str(gReportCount) + ".json"
      plainFile = open(filename, "w")
      if gArgs.saveRawPings:
        plainFile.write(plainData)
      else:
        jsonData = json.loads(plainData)
        json.dump(jsonData, plainFile, sort_keys = False, indent = 2)
      plainFile.close()

      s.send_response(200)
      s.send_header("Content-type", "text/html")
      s.end_headers()

      print time.asctime() + "\tReceived submission #" + str(gReportCount) + ":", str(length), "bytes. Saved in", filename

parser = argparse.ArgumentParser(description="Telemetry test server.")
parser.add_argument("-p", "--port", dest="port", default=80, type=int,
                    help="The port to listen on.")
parser.add_argument("-r", "--raw-pings", dest="saveRawPings", action="store_true",
                    help="Store the raw pings instead of pretty formatting.")
gArgs = parser.parse_args()

server_class = BaseHTTPServer.HTTPServer
httpd = server_class((HOST_NAME, gArgs.port), HTTPHandler)
print "%s\tServer started - %s:%s" % (time.asctime(), HOST_NAME, gArgs.port)
httpd.serve_forever()
