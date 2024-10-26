import smtplib
import re
import requests
import config as secret

email = secret.GMAIL_ADDRESS

def main():
    recipient_email = input("What is your email? ")
    recipient_email = verify(recipient_email)
    report = weather()
    print(send(recipient_email, report))

def verify(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

    while True:
        if re.fullmatch(regex, email):
            return email
        else:
            email = input("The previously entered email is invalid. Please re-enter a valid email address: ")

def weather():
    response = requests.get("https://api.weather.gov/points/40.5236,-74.4350")
    dict = response.json()
    fresponse = requests.get(dict["properties"]["forecastHourly"])
    forecast = fresponse.json()

    h3 = forecast["properties"]["periods"][3]

    temp = h3["temperature"]
    humidity = h3["relativeHumidity"]["value"]
    precipitation = h3["probabilityOfPrecipitation"]["value"]
    windspeed = h3["windSpeed"]
    winddir = h3["windDirection"]
    short = h3["shortForecast"]
    clothes = ""

    if winddir == "E":
        winddir = "east"
    elif winddir == "N":
        winddir = "north"
    elif winddir == "S":
        winddir = "south"
    else:
        winddir = "west"

    short = short.lower()

    if temp > 75:
        clothes = "I recommend you wear shorts and a light breathable t-shirt."
    elif temp > 70:
        clothes = "I recommend you wear shorts and a lightweight button up shirt."
    elif temp > 65:
        clothes = "I recommend you wear sweatpants and a longsleeve tshirt."
    elif temp > 60:
        clothes = "I recommend you wear sweatpants and a sweatshirt."
    elif temp > 50:
        clothes = "I recommend you wear a sweatpants and a thick hoodie."
    else:
        clothes = "I recommend you wear a thick pair of pants and a burly coat."

    if precipitation > 35:
        clothes += "I recommend you also pack an umbrella."

    subject = "Your Daily Weather Report"
    body = f"Hello! This is your daily weather report. \n\n\nAs of where you live, it is {temp} degrees fahrenheit. \n\n"
    body += f"The sky is {short} and there is a {precipitation}% chance of precipitation. \n\n"
    body += f"The windspeed is {windspeed} traveling {winddir}. The relative humidity is {humidity}%. \n\n"
    body += f"As for today, {clothes} \n\n\nHave an amazing day!"

    message = f"Subject: {subject}\n\n{body}"
    return message

def send(reciever, text):
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(email, secret.GMAIL_KEY)
    server.sendmail(email, reciever, text)
    return("The weather report has been sent to " + reciever)

if __name__ == "__main__":
    main()
