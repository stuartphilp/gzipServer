import os
import pprint
import simplejson as json


ping_info = {}

for root,dirs,files in os.walk("."):
  for f in files:
    if f.startswith("report") and f.endswith(".json"):
      with open(f) as data_file:
        data = json.load(data_file)
        ping_info[f] = data["payload"]["info"]

last_profile_subession_counter = 0
last_session_id = ""
last_subsession_id = ""
last_profile_counter = 0
result = {}

for ping in ping_info:
  ping_state = {}
  #started a new session?
  if ping_info[ping]["sessionId"] != last_session_id:
    ping_state["session_id_valid"] = True
    ping_state["subsession_id_valid"] = (ping_info[ping]["subsessionId"] != last_subsession_id)
    ping_state["previous_session_id_valid"] = (ping_info[ping]["previousSessionId"] == last_session_id or ping_info[ping]["previousSessionId"] == "")
    last_session_id = ping_info[ping]["sessionId"]
  #started a new subsession?
  if ping_info[ping]["subsessionId"] != last_subsession_id:
    if last_profile_counter == 0:
      last_profile_counter = ping_info[ping]["profileSubsessionCounter"]
      ping_state["profile_counter_valid"] = True
    else:
      ping_state["profile_counter_valid"] = (ping_info[ping]["profileSubsessionCounter"] == (ping_info[ping]["profileSubsessionCounter"] + 1))


  # ping_state["profile_subession_counter_valid"] = True
  # ping_state["subsession_id_valid"] = True
  # ping_state["session_id_valid"] = True
  result[ping] = ping_state

print result
# check chaining
# check profilecounter++


# filename = "condensed.json"
# newFile = open(filename, "w")
# json.dump(ping_info, newFile, sort_keys = True, indent = 2)
# newFile.close()
# print("Reports combined into condensed.json")
