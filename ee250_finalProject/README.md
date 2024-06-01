## Bed Frame Motion-Activated Lighting System

LED is attached to the bed frame and a PIR signal controls the strip. PIR data and time are recorded and sent to a flask server and rendered with the html. 

## Authors

- [Valeria Gamez](https://github.com/ValeriaGamez)
- [Supriya Subramian]()

## Setup and Run 
1. Install requirements
```bash
pip install flask
```
```bash
pip install RPi.GPIO
```
2. Run the server
```bash
export FLASK_APP=light_server.py
flask run
```
3. In another terminal
```bash
python groove_relay.py
```