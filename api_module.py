import requests, json, api_module

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

    response = requests.request("PATCH", url_cloudflare, json=payload, headers=headers)
    return response.status_code 

def getExternalIP():
    response = requests.get("https://api.ipify.org")
    if response.status_code == 200:
        return response.text
    else:
        print("Erro")

def saveData(key, value, type, file_path='settings.json'):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"ip": "", "interval": "", "globalkey": "", "notifications": "", "domains": []}

    if type == "update":
        data[key] = value
    elif type == "append":
        data[key].append(value)
    data.update(data)

    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        print("Dados salvos com sucesso.")
    except Exception as e:
        print(f"Erro ao salvar os dados: {e}")

def loadData(key, file_path='settings.json'):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            return data[key]
    except Exception as e:
        print(f"Erro ou carregar parametro: {e}")

def loadDomainsandUpdate():
    try:
        ActualIP = getExternalIP()
        newIP = False
        with open('settings.json') as f:
            data = json.load(f)

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
                        return status_code
        if newIP:
            saveData("ip", ActualIP, "update")           
        else:
            print("Sem alteracoes no ip")
                          
    except Exception as e:
        print(f"Erro ao adicionar novo domínio: {e}")