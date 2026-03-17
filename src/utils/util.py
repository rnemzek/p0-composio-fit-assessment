import os
import json
import requests
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv


def loadenv():
    """Load .env from the project root into the environment."""
    env_path = Path(__file__).resolve().parent.parent.parent / ".env"
    load_dotenv(dotenv_path=env_path)


class Util:
    @staticmethod
    def getDateTimestamp():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def get_environ_variable_as_array(environ_key):
        my_string = os.getenv(environ_key)
        return my_string.split(",")

    def raiseError(self, v_name, v_value, env_variable):
        compare_value = os.getenv(v_name)
        if v_value is not None and v_value == compare_value:
            print(f"✅ Passed check: {v_name}")
        else:
            raise ValueError(f"❌ Failed check: {v_name}")

    def pretty_json(self, json_string):
        # 1. Parse string into a Python dictionary
        parsed = json.loads(json_string)

        # 2. Serialize back to a formatted string
        # 'indent' defines the number of spaces for each level
        pretty_json = json.dumps(parsed, indent=4)

        # 3. return pretty json
        return pretty_json

    def pretty_json(self, data):
        # If 'data' is already a dict, don't call json.loads()
        if isinstance(data, dict):
            return json.dumps(data, indent=4)

        # If it's a string, load it first then dump it
        parsed = json.loads(data)
        return json.dumps(parsed, indent=4)

    def dictify_json(self, data):
        if isinstance(data, dict):
            return data
        else:
            return json.loads(data)

    def fetch_url(self, url):
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text

    def json_contains_data_items(self, data):
        data_dict = self.dictify_json(data)
        inner_data = data_dict.get("data", {})
        if any(inner_data.values()):
            print("✅  Events found")
            return True
        else:
            print("☑️   No events found")
            return False
