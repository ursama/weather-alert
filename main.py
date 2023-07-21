import requests
from twilio.rest import Client

TWILIO_ACCOUNT_SID = "Your SID"
TWILIO_AUTH_TOKEN = "Your token"

api_key = "Your key to OWM API"
account_sid = TWILIO_ACCOUNT_SID
auth_token = TWILIO_AUTH_TOKEN

parameters = {
    "lat": 12.9124, # Random latitude, choose yours
    "lon": 128.071770, # Random longitude, choose yours
    "exclude": "current,minutely,daily",
    "appid": api_key
}

response = requests.get(url="https://api.openweathermap.org/data/2.5/onecall", params=parameters)
response.raise_for_status()
data = response.json()

conditions = []
temperatures = []

for _ in range(0, 12):
    weather_id = data["hourly"][_]["weather"][0]["id"]
    weather_description = data["hourly"][_]["weather"][0]["description"]
    temperatures.append(round(data["hourly"][_]['temp'] - 273.15))
    if weather_id < 800:
        if weather_description not in conditions:
            conditions.append(weather_description)

max_temp = max(temperatures)
min_temp = min(temperatures)

temperature_msg = f"Min temperature will be {min_temp}, and max {max_temp}."

client = Client(account_sid, auth_token)

if conditions:
    conditions = ", ".join(conditions)
    text = f"There will be {conditions} today. "
else:
    text = "Today will be calm. "

text += temperature_msg

message = client.messages.create(
    from_='whatsapp:Your twilio number',
    body=text,
    to='whatsapp:Your number'
)

print(message.status)
