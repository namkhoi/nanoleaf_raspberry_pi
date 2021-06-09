import RPi.GPIO as GPIO
import time
import requests
import json
import spidev
import time

spi = spidev.SpiDev()  # create spi object
spi.open(0, 0)  
spi.max_speed_hz = 1000000
auth_token = "xxxxxxxxxxxxxxxxxxxxxxxxxxx"

def readadc(adcnum):
    if ((adcnum > 7) or (adcnum < 0)):
        return -1
    r = spi.xfer2([1, (8 + adcnum) << 4, 0])
    time.sleep(0.000005)
    adcout = ((r[1] & 3) << 8) + r[2]
    return adcout

brightness_start = 0
on = True
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)
GPIO.setup(18, GPIO.IN)
GPIO.setup(4, GPIO.IN)
url = "http://192.168.0.219:16021/api/v1/{}/state".format(auth_token)
try:
    while True:
        # Enable/disable lights 
        if GPIO.input(17) == 1:
            print("Turn on/off")

            url_get_on = "http://192.168.0.219:16021/api/v1/{}/state/on"
            payload = ""
            headers = {}
            response = requests.request("GET", url_get_on, headers=headers, data=payload)
            response_json = json.loads(response.text)
            if response_json["value"]:
                print("passeert")
                payload = '{"on": {"value": false}}'
                headers = {
                    'Content-Type': 'text/plain'
                }
                response = requests.request("PUT", url, headers=headers, data=payload)
                on = False
            else:
                payload = '{"on": {"value": true}}'
                headers = {
                    'Content-Type': 'text/plain'
                }
                response = requests.request("PUT", url, headers=headers, data=payload)
                on = True
            time.sleep(0.1)
        # Change to the next color
        if GPIO.input(18) == 1:
            print("Change color")

            url = "http://192.168.0.219:16021/api/v1/{}/state/"

            payload = ""
            headers = {}

            response = requests.request("GET", url, headers=headers, data=payload)
            response_json = json.loads(response.text)
            hue = response_json["hue"]["value"]

            if hue <= 300:
                hue = hue + 60
            else:
                hue = hue - 360 + 60
            #Saturatie is set to 100%
            # color temperature is set to 1200
            payload = '{"sat": {"value": 100}, "ct": {"value":1200}, "hue":{"value":%s}}' % (hue)
            headers = {
                'Content-Type': 'text/plain'
            }
            response = requests.request("PUT", url, headers=headers, data=payload)
        # Go back to previous color
        if GPIO.input(4) == 1:
            print("Reverse change color")

            url = "http://192.168.0.219:16021/api/v1/{}/state/"

            payload = ""
            headers = {}

            response = requests.request("GET", url, headers=headers, data=payload)
            response_json = json.loads(response.text)
            hue = response_json["hue"]["value"]

            if hue >= 60:
                hue = hue - 60
            else:
                hue = hue + 360 - 60
            # Saturatie is set to 100%
            # Color temperature is set to 1200
            payload = '{"sat": {"value": 100}, "ct": {"value":1200}, "hue":{"value":%s}}' % (hue)
            headers = {
                'Content-Type': 'text/plain'
            }
            response = requests.request("PUT", url, headers=headers, data=payload)
        # Change the brightness of the lights
        if on:
            brightness = readadc(0)
            print(brightness)
            brightness_percent = round((brightness / 1023) * 100)
            if brightness_start != brightness_percent:
                payload = "{\"brightness\" : {\"value\":%s}}" % brightness_percent
                headers = {
                    'Content-Type': 'text/plain'
                }
                requests.request("PUT", url, headers=headers, data=payload)
                time.sleep(0.2)
                print("Brightness: "+ str(brightness_percent) +"%")
                brightness_start = brightness_percent
except KeyboardInterrupt:
    GPIO.cleanup()
    print("program executed")
