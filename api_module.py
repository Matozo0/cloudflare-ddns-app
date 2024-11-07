from requests import get, request
from json import dump, load
import sys
from pathlib import Path

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return Path(sys._MEIPASS) / relative_path
    return Path(__file__).parent / relative_path

ActualIP = ""

def updateDomain(IP, DNS_RECORD_ID, ZONE_ID, COMMENT, DOMAIN, PROXY_TYPE, TTL_TIME, TYPE, EMAIL_TOKEN, GLOBAL_KEY):
    url_cloudflare = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/{DNS_RECORD_ID}"

    payload = {
    "comment": COMMENT,
    "name": DOMAIN,
    "proxied": PROXY_TYPE,
    "settings": {},
    "tags": [],
    "ttl": TTL_TIME,
    "content": IP,
    "type": TYPE
    }
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Email": EMAIL_TOKEN,
        "X-Auth-Key": GLOBAL_KEY
    }

    response = request("PATCH", url_cloudflare, json=payload, headers=headers)
    return response.status_code 

def getExternalIP():
    response = get("https://api.ipify.org")
    if response.status_code == 200:
        return response.text
    else:
        print("Erro")

def saveData(key, value, type, file_path='config.json'):
    try:
        with open(resource_path(file_path), 'r') as f:
            data = load(f)
    except FileNotFoundError:
        data = {"ip": "", "interval": "", "globalkey": "", "notifications": "", "domains": []}

    if type == "update":
        data[key] = value
    elif type == "append":
        data[key].append(value)
    data.update(data)

    try:
        with open(resource_path(file_path), 'w') as f:
            dump(data, f, indent=4)
        return 1
    except Exception as e:
        return 0

def loadData(key, file_path='config.json'):
    try:
        with open(resource_path(file_path), 'r') as f:
            data = load(f)
            return data[key]
    except Exception as e:
        print(f"Erro ou carregar parametro: {e}")

def loadDomainsandUpdate(icon):
    try:
        ActualIP = getExternalIP()
        newIP = False
        notifications_enable = loadData("notifications")
        updated = []
        not_updated = []
        with open(resource_path('config.json')) as f:
            data = load(f)

            if ActualIP != data['ip']:
                newIP = True
                for domain in data['domains']:
                    if domain["ENABLE"]:
                        status_code = updateDomain(
                            IP=ActualIP,
                            DNS_RECORD_ID=domain['DNS_RECORD_ID'],
                            ZONE_ID=domain['ZONE_ID'],
                            COMMENT=domain['COMMENT'],
                            DOMAIN=domain['DOMAIN'],
                            PROXY_TYPE=domain['PROXY_TYPE'] == 'True',
                            TTL_TIME=domain['TTL_TIME'],
                            TYPE=domain['TYPE'],
                            EMAIL_TOKEN=domain['EMAIL_TOKEN'],
                            GLOBAL_KEY=data["globalkey"]
                        )
                        if status_code == 200:
                            updated.append(domain['DOMAIN'])
                        elif status_code != 200:
                            not_updated.append(domain['DOMAIN'])
        if updated != [] and notifications_enable:
            icon.notify(f"{updated}: domains updated successfully!", "DNS Updater")
        if not_updated != [] and notifications_enable:
            icon.notify(f"{not_updated}: domains not updated!", "DNS Updater")
        if newIP:
            saveData("ip", ActualIP, "update")           
        else:
            print("Sem alteracoes no ip")
                          
    except Exception as e:
        print(f"Erro ao atualizar domínio: {e}")