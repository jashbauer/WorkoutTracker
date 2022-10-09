import requests
import datetime as dt
import os

# NUTRIOTINIX API INFO
# KEYS ARE ENVIRONMENT VARIABLES - USE YOUR INFORMATION INSTEAD
APP_ID = os.environ.get("APP_ID")
API_KEY = os.environ.get("API_KEY")


URL = "https://trackapi.nutritionix.com/v2/natural/exercise"

HEADERS = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY
}

# PARAMETERS CONSTANTS FOR NUTRITIONIX API
GENDER = "male"
WEIGHT_KG = 85.5
HEIGHT_CM = 170.0
AGE = "31"

# Get Text:
text = input("What did you do today? ")

PARAMS = {
    "query": text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

# FORMATTED TIME DATA
today = dt.datetime.now().strftime("%d/%m/%Y")
today_time = dt.datetime.now().strftime("%H:%M:%S")

# NUTRIOTIONIX API REQUEST
response = requests.post(url=URL, json=PARAMS,  headers=HEADERS)
response.raise_for_status()

content = response.json()


# SHEETY POST API DATA
SHEETY_URL = "https://api.sheety.co/9d4fa3e77f6e677c7c23142528417bec/myWorkouts/workouts"

# ANTHENTICATOR IS AN ENVIRONMENT VARIABLE - USE YOUR OWN INSTEAD
BEARER = os.environ.get("BEARER")

SHEETY_HEADER = {
    "Authorization": BEARER
}

# MANIPULATE EXERCISE DATA AND ADD ROWS TO SPREADSHEET
exercise_data = content["exercises"]

# EXTRACT RELEVANT DATA AND POST TO SPREADSHEET
for i in range(len(exercise_data)):
    date = today
    time = today_time
    exercise = exercise_data[i]["name"].title()
    duration = exercise_data[i]["duration_min"]
    calories = exercise_data[i]["nf_calories"]

    params = {
        "date": date,
        "time": time,
        "exercise": exercise,
        "duration": duration,
        "calories": calories
    }

    to_post = {
        "workout": params
    }

    response = requests.post(url=SHEETY_URL, json=to_post, headers=SHEETY_HEADER)
    response.raise_for_status()
