***This is a fork of gzipServer intended for testing the telemetry pipeline. It will migrate in purpose and update over time, eventually changing the name if it gets far enough along.***

gzipServer is a Web server that receives gzip'd POST requests and saves them uncompressed locally, particularly useful for testing telemetry pings.

# Using gzipServer

To force Firefox to send a Telemetry payload to this server:

1. Start the server: ./gzipServer.py
2. change the toolkit.telemetry.server Firefox pref in about:config to http://127.0.0.1
3. Restart Firefox to have Telemetry pick up the above pref change
4. Open about:telemetry (it has the Telemetry namespaces nicely set up) and open the DevTools console
5. Paste the following into the console: TelemetrySession.observe(null, "idle", null);
6. The script will save the request it receives to "report1.txt" in the script's working directory

Note: The above will send an idle-daily ping. These will go away soon.

# Testing data-pipeline using ping-generator

* Start up a local [data-pipeline](https://github.com/mozilla-services/data-pipeline/) if you want to test locally, or use the staging environment. 
* Generate c pings of type t, ex.: ```python ping-generator.py -t saved-session -c 1000```
* Check server logs or kafka to ensure the data-pipeline received the pings
* Verify the correct number of pings were stored using heka-cat: 
```
build/heka/build/heka/bin/heka-cat data_raw.out
build/heka/build/heka/bin/heka-cat data_decoded.out
```
