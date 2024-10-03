import dirigera
import time
import requests

dirigera_hub = dirigera.Hub(
    token="eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjJiYjJiZTc0ZTFkNWY5ZGMwNDMwNWNjZjI0YTA3YmNmMTU5YTc0ZTg5YTIxYTE5MzYwZmVjN2ZhNmU1ZmE0YzYifQ.eyJpc3MiOiJhZWU3MTA2Ny1hMTI1LTQ5ZjYtYmRlNy1jODkzN2JlMWEyZWIiLCJ0eXBlIjoiYWNjZXNzIiwiYXVkIjoiaG9tZXNtYXJ0LmxvY2FsIiwic3ViIjoiNWI2YzMyM2ItMGRjZS00ZWI1LWJlZjEtNzNhN2UzOWEwY2Y0IiwiaWF0IjoxNzI2ODM5NjY3LCJleHAiOjIwNDI0MTU2Njd9._R1I8v6vY4CABO6YTngotroQO_sbejw3u9DeuX7gTLM7MHaxYg8vbZuiOL4rYSN-ny3r5Pp7RgvZMfeaGWVcIA",
    ip_address="192.168.1.82"
)
try:
    smart_plug = dirigera_hub.get_outlet_by_name("3D Printer")
except AssertionError as e:
    print(type(e))
    print(e.args[0])
    print("Could not get outlet")
    exit(1)
except requests.exceptions.ConnectTimeout as e:
    print(type(e))
    print(e.args[0].args[0])
    print("Timeout. Most likely the IP address is wrong")
    exit(1)
except requests.exceptions.HTTPError as e:
    print(type(e))
    if e.response.status_code == 401:
        print("Not authorized. Regenerate token")
    print(e)
    print("Could not get outlet")
    exit(1)

is_on = smart_plug.attributes.is_on
i = 1
