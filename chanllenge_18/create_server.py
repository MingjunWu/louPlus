import requests

def create_server(name, host):
    data = {'name': name,
            'host' : host}
    resp = requests.post('http://127.0.0.1:5000/servers/',json=data)
    return resp.json()



