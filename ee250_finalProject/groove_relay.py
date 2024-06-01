# NOTE: Relay is normally open. LED will illuminate when closed and you will hear a definitive click sound
import time
import RPi.GPIO as GPIO
import requests

# Relay
# SIG,NC,VCC,GND
blue = 14
red = 15
pir = 23

# set pins as I/O
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(blue, GPIO.OUT)
GPIO.setup(red, GPIO.OUT)
GPIO.setup(pir, GPIO.IN)

on_state = 0; # starts in off state

timestamps = []
pir_data = []


while True:
    try:
        
        timestamps.append(time.strftime("%H:%M:%S", time.localtime()))
        state = GPIO.input(pir)
        pir_data.append(state)
        
        curr_hour = int(time.strftime("%H", time.localtime()))

        payload = {
            "timestamps": timestamps, 
            "pir_data": pir_data, 
            }
        response = requests.post("http://localhost:5000/", json=payload)
        
        if on_state == 1:
            print ("ON")
            GPIO.output(blue, GPIO.LOW)
            print(GPIO.input(pir))
            if GPIO.input(pir):
                print("motion detected in on state")
                on_state = 0; 
                time.sleep(1)
        else: # off state
            print("OFF")
            GPIO.output(blue, GPIO.HIGH)
            print(GPIO.input(pir))                                      #c check if motion + time is valid + distance is valid
            if GPIO.input(pir) and (curr_hour > 18 or curr_hour < 8): #values will be changed for demo purposes 
                print ("motion detected in off state")
                on_state = 1 # if motion and time is valid -> ON 
                time.sleep(1) 
        time.sleep(0.5)

        # Calculate average activity per hour
        hourly_data = {}
        for t, p in zip(timestamps, pir_data):
            hour = t.split(":")[0]
            hourly_data[hour] = hourly_data.get(hour, []) + [p]
        
        for hour, data in hourly_data.items():
            avg_activity = sum(data) / float(len(data)) * 100
            print("Hour {}: Average activity = {}".format(hour, avg_activity))

         # Calculate average signal in last 1 hour
        if len(timestamps) > 3600:  # 3600 seconds in an hour
            avg_signal = sum(pir_data[-3600:]) / 3600.0
            print("Average PIR signal in last 1 hour: {:.2f}".format(avg_signal))

    except KeyboardInterrupt:
        # Turn off the relay and exit gracefully if Ctrl+C is pressed
        GPIO.cleanup()
        break