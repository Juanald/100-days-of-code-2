import requests
import datetime as dt
import auth
USERNAME = "gavin123"
TOKEN = "hawhgowiaghoi"
GRAPH_ID = "graph1"

pixela_endpoint = "https://pixe.la/v1/users"
user_params = {
    "token" : TOKEN,
    "username" : USERNAME,
    "agreeTermsOfService" : "yes",
    "notMinor" : "yes"
}
# User creation
# response = requests.post(url=pixela_endpoint, json=user_params)
# print(response.text)

graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs"

graph_config = {
    "id" : GRAPH_ID,
    "name" : "Reading Graph",
    "unit" : "Minutes",
    "type" : "int",
    "color" : "sora"
}
headers = {
    "X-USER-TOKEN" : TOKEN  
}
 
 # graph creation
# response = requests.post(url=graph_endpoint, json=graph_config, headers=headers)
# print(response.text)

# Posting a value to the graph
def post_value(minutes):
    graph_post_endpoint = f"https://pixe.la/v1/users/{USERNAME}/graphs/{GRAPH_ID}"
    graph_post_config = {
        "date" : dt.datetime.now().strftime("%Y%m%d"),
        "quantity" : str(minutes) # this is variable amount that can be entered into a function
    }

    response = requests.post(url=graph_post_endpoint, json=graph_post_config, headers=headers)
    response.raise_for_status()
    print(response.text)

def update_value(minutes, date):
    graph_put_endpoint = f"https://pixe.la/v1/users/{USERNAME}/graphs/{GRAPH_ID}/{date}"

    put_params = {
        "quantity" : str(minutes),
     }
    
    response = requests.put(url=graph_put_endpoint, json=put_params, headers=headers)
    response.raise_for_status()
    print(response.text)

def delete_value(date):
    graph_delete_endpoint = f"https://pixe.la/v1/users/{USERNAME}/graphs/{GRAPH_ID}/{date}"

    response = requests.delete(url=graph_delete_endpoint, headers=headers)
    response.raise_for_status()
    print(response.text)

if __name__ == "__main__":
    pass
