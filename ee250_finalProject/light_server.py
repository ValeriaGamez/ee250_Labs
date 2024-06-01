from typing import Dict, List, Optional
from flask import Flask, request, jsonify, render_template
import pathlib
import json
import time


app = Flask(__name__)
thisdir = pathlib.Path(__file__).parent.absolute() # path to directory of this file


timestamps = []
pir_data = []
data = {"timestamps": [], "pir_data": []}


@app.route("/", methods=["POST", "GET"])  # define a route for the root URL accepting POST requests
def index():
    if request.method == "POST":
        content = request.json  # get JSON data from the request
        timestamps = content.get("timestamps")
        pir_data = content.get("pir_data")
        
        if timestamps and pir_data:  # if data is present
            new_timestamps = [ts for ts in timestamps if ts not in data["timestamps"]]
            data["timestamps"].extend(new_timestamps)  # add timestamps to global data
            data["pir_data"].extend(pir_data)  # add pir_data to global data
            
            return jsonify({"status": "success"})  # return success status
        else:
            return jsonify({"status": "error", "message": "Invalid data"}), 400  # return error status if data is missing
    else: # handle GET request
        current_time = time.strftime("%H:%M", time.localtime())
        curr_hour = int(current_time[0])
        if curr_hour >= 00 and curr_hour < 12:
            meridian = "am"
        elif curr_hour >= 12 and curr_hour <= 23:
            meridian = "pm"
        current_time += meridian
        
        return render_template("index.html", data=data, time=current_time)


if __name__ == '__main__':
    app.run(port=5000, debug=True)