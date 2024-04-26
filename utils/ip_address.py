import requests


def get_public_ip():
    try:
        ip = requests.get("https://api.ipify.org").content.decode("utf8")
        print("My public IP address is: {}".format(ip))
        return ip
    except requests.RequestException as e:
        print("Error:", e)
        return None
