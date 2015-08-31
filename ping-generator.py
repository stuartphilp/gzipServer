import os
import errno
import optparse
import urllib2
import simplejson as json
from datetime import datetime

parser = optparse.OptionParser()

parser.add_option('-t', '--type',
    action="store", dest="type",
    help="Ping type", default="save-session")

parser.add_option('-c', '--count',
    action="store", dest="count",
    help="Numbers of pings to generate", default=1, type="int")

options, args = parser.parse_args()

print "Generating {0} pings of type {1}".format(options.count, options.type)

ping_dir = "{0}_{1}_{2}".format(datetime.strftime(datetime.now(), '%Y-%m-%d'), options.type, options.count)
if not os.path.exists(ping_dir):
  os.makedirs(ping_dir)

iteration = 1
while iteration <= options.count:
  with open("ping-template.json") as data_file:
    data = json.load(data_file)

    #TODO: modify properties to fuzz some real-world scenarios
    ping_info = data["payload"]["info"]

    #archive ping locally so we can resend or inspect
    #TODO: add option to clean up or archive (save storage space)
    filename = "{0}/{1}_{2}.json".format(ping_dir, options.type, iteration)
    ping_archive = open(filename, "w")
    json.dump(data, ping_archive, indent = 2)
    ping_archive.close()

    #submit ping to pipeline.incoming
    #TODO: generate id
    ping_id = "ce39b608-f595-4c69-b6a6-f7a436604648"
    #TODO: need env variable or param to switch between local/stage/whatever
    local_server = 'http://127.0.0.1:8080'
    stage_server = 'https://pipeline-incoming.stage.mozaws.net'
    pipeline_submit = '{0}/submit/telemetry/{1}/{2}/Firefox/38.0a1/nightly/20150125030202'.format(local_server, ping_id, options.type)
    req = urllib2.Request(pipeline_submit)
    req.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(req, json.dumps(data))
    print "Ping {0} submitted out of {1}".format(iteration, options.count)
  iteration += 1
