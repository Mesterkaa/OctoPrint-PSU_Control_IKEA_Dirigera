import dirigera
import time

dirigera_hub = dirigera.Hub(
    token="eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjJiYjJiZTc0ZTFkNWY5ZGMwNDMwNWNjZjI0YTA3YmNmMTU5YTc0ZTg5YTIxYTE5MzYwZmVjN2ZhNmU1ZmE0YzYifQ.eyJpc3MiOiJhZWU3MTA2Ny1hMTI1LTQ5ZjYtYmRlNy1jODkzN2JlMWEyZWIiLCJ0eXBlIjoiYWNjZXNzIiwiYXVkIjoiaG9tZXNtYXJ0LmxvY2FsIiwic3ViIjoiNWI2YzMyM2ItMGRjZS00ZWI1LWJlZjEtNzNhN2UzOWEwY2Y0IiwiaWF0IjoxNzI2ODM5NjY3LCJleHAiOjIwNDI0MTU2Njd9._R1I8v6vY4CABO6YTngotroQO_sbejw3u9DeuX7gTLM7MHaxYg8vbZuiOL4rYSN-ny3r5Pp7RgvZMfeaGWVcIA",
    ip_address="192.168.1.82"
)

""" lights = dirigera_hub.get_lights()

office_light_1 = dirigera_hub.get_light_by_name("Office light 1")

office_light_1.set_light(lamp_on=True)
time.sleep(2)
office_light_1.set_light(lamp_on=False)
time.sleep(2)
office_light_1.set_light(lamp_on=True)
time.sleep(2)
office_light_1.set_light(lamp_on=False)

print(lights) """

smart_plug = dirigera_hub.get_outlet_by_name("3D Printer")
isOn = smart_plug.attributes.is_on()

i = 1
