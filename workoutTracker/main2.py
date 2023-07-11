# Print exercise stats for text input
import auth, requests
import datetime as dt

NUTRIONIX_API_KEY = auth.NUTRITIONIX_API_KEY
NUTRIONIX_APP_ID = auth.NUTRIONIX_APP_ID
EXERCISE_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
SHEETS_ENDPOINT = auth.SHEETS_ENDPOINT
BEARER_TOKEN = auth.BEARER_TOKEN
GENDER = "male" # values may be adjusted, these are placeholders
WEIGHT_KG = 100
HEIGHT_CM = 180
AGE = 30

headers = {
    "x-app-id" : NUTRIONIX_APP_ID,
    "x-app-key" : NUTRIONIX_API_KEY,
}

bearer_headers = {
    "Authorization" : f"Bearer {BEARER_TOKEN}"
}

def process_query():
    query = input("What exercises did you do today? ")
    parameters = {
        "query" : query,
        "gender" : GENDER,
        "weight_kg" : WEIGHT_KG,
        "height_cm" : HEIGHT_CM,
        "age" : AGE
    }
    response = requests.post(url=EXERCISE_ENDPOINT, json=parameters, headers=headers)
    response.raise_for_status()
    return response.json()['exercises']
    
def post_to_sheet(data):
    # need to post for every exercise in data
    # date time exercise duration calories
    for exercise_data in data:
        # generate a new row from sheety api
        parameters = {
            "workout" : {
                "date" : dt.datetime.now().strftime("%d/%m/%Y"),
                "time" : dt.datetime.now().strftime("%X"),
                "exercise" : exercise_data['name'].title(),
                "duration" : exercise_data['duration_min'],
                "calories" : exercise_data['nf_calories'],
            }
        }
        response = requests.post(url=SHEETS_ENDPOINT, json=parameters, headers=bearer_headers)
        response.raise_for_status()
        print("Complete")

if __name__ == "__main__":
    post_to_sheet(process_query())
