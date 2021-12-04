import os
import requests
import json
from requests.exceptions import HTTPError
from dotenv import load_dotenv


load_dotenv('.env')
API_SELECT_URL = os.environ.get('API_SELECT_URL')


def select_from_all(di: int = 0, ai: int = 0, do: int = 0, ao: int = 0):
    try:
        response = requests.post(
            f"{API_SELECT_URL}/dcCtrlSelect",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"di": di, "ai": ai, "do": do, "ao": ao}))

        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        selected = response.json()['results']
        for s in selected:
            print(s['name'])


# select_from_all(6, 2, 3, 3)
