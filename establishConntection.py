import requests

def status_code(response):
    if response.status_code == 200:
        print("connection established")
        return True
    elif response.status_code == 404:
        print("Website not found")
        return False