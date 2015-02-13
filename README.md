# gzipServer
Web server that receives gzip'd POST requests and saves them uncompressed locally

To force Firefox to send a Telemetry payload to this server:

1. Start the server: ./gzipServer.py
2. change the toolkit.telemetry.server Firefox pref in about:config to http://127.0.0.1
3. Restart Firefox to have Telemetry pick up the above pref change
4. Open about:telemetry (it has the Telemetry namespaces nicely set up) and open the DevTools console
5. Paste the following into the console: TelemetrySession.observe(null, "idle", null);
6. The script will save the request it receives to "report1.txt" in the script's working directory

Note: The above will send an idle-daily ping. These will go away soon.
