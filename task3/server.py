#!/home/ruslan/anaconda3/bin/python

import socket
import sys
import datetime
import configparser
import json
import xml.etree.ElementTree as ET
import requests
import dicttoxml

def parse(data: str):
    '''Parse user data'''
    ans = dict().fromkeys(["base", "count", "final", "format"])
    default = ["RUB", "1", False, False]
    keys = list(ans.keys())
    for i in range(len(keys)):
        if  data.find(keys[i]) == -1:
            ans[keys[i]] = default[i]
        elif i == 3:
            val = data[data.rfind('=') + 1:len(data)]
            ans[keys[i]] = val
        else:
            pos = data.find(keys[i]) + len(keys[i]) + 1
            val = data[pos:data.find("&", pos)]
            ans[keys[i]] = val
    if ans["format"] != "json" and ans["format"] != "xml":
        raise KeyError
    return ans

def req_hand(cur: list, user_data: dict):
    ans_dict = {}
    ans_dict["base_currency"] = user_data["base"]
    ans_dict["base_value"] = user_data["count"]
    ans_dict["final_currency"] = user_data["final"]
    ans_dict["final_value"] = int(user_data["count"]) * cur[0] / cur[1]
    if user_data["format"] == "json":
        return json.dumps(ans_dict, indent = 4).encode("utf-8")
    return dicttoxml.dicttoxml(ans_dict, custom_root='my_api')

def api():
    bank_xml = requests.get('http://www.cbr.ru/scripts/XML_daily.asp')
    root = ET.fromstring(str(bank_xml.text))
    response_dict = {}
    for child in root:
        value = [child.find("Value").text, child.find("Name").text]
        response_dict[child.find("CharCode").text] = value
    return response_dict

config = configparser.ConfigParser()
config.read(sys.argv[1])
log_path = config["LOG"]["Path"]
port = int(config["SERVER"]["Port"])
max_con = int(config["SERVER"]["Backlog"])
timeout = int(config["SERVER"]["Timeout"])
f = open(log_path, 'a')
now = None

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', port))
sock.listen(max_con)
print('server is running, please, press ctrl+c to stop')

try:
    while True:
        conn, addr = sock.accept()
        conn.settimeout(timeout)
        data = conn.recv(1024)
        data = data.decode("utf-8")
        now = datetime.datetime.now()
        f.write(str(now) + '\n')
        f.write('\t' + f"request: {data}" + '\n')
        api_res = api()
        user_in = parse(data)
        api_res['RUB'] = ['1', "Российский рубль"]
        if False in user_in.values():
            client_res = {}
            for key in api_res.keys():
                client_res[key] = api_res[key][1]
            json_res = json.dumps(client_res, ensure_ascii = False, indent = 4)
            conn.send(json_res)
            raise KeyError
        cur = [api_res[user_in["base"]][0], api_res[user_in["final"]][0]]
        cur = [float(i.replace(',', '.')) for i in cur]
        client_res = req_hand(cur, user_in)
        now1 = datetime.datetime.now()
        f.write('\t' + "time of process: " + str((now1-now).total_seconds()) + '\n')
        f.write('\t' + f"response_size: {len(client_res)}" + '\n')
        f.write(str(now1) + '\n\n')
        conn.send(client_res)

except socket.timeout:
    now1 = datetime.datetime.now()
    f.write('\t' + "time of process: " + str((now1-now).total_seconds()) + '\n')
    f.write('\t' + "Timeout error" + '\n')
    f.write(str(now1) + '\n\n')
    conn.send("Timeout interrupt\n".encode("utf-8"))
    conn.close()
    sys.exit(0)
except KeyboardInterrupt:
    conn.close()
    print("Server has stopped")
    sys.exit(0)
except KeyError:
    now1 = datetime.datetime.now()
    f.write('\t' + "time of process: " + str((now1-now).total_seconds()) + '\n')
    f.write('\t' + "Format error" + '\n\n')
    f.write(str(now1) + '\n')
    conn.send("\nWrong format:\n example: base=XXX&count=n&final=XXX&format=xml|json".encode("utf-8"))
    conn.close()
    sys.exit(0)
