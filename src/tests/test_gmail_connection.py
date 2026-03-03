import os
import json
from composio import Composio
# from utils import getDateTimestamp
from src.tests.utils.util import getDateTimestamp

timestamp = getDateTimestamp()
print(f">>>>> " + timestamp)

# Initialize with your API Key (get it from the Composio Dashboard)
composio_api_key = os.environ.get("COMPOSIO_API_KEY")

print(">>>>> Creating composio using api_key=" + composio_api_key)
composio = Composio(api_key=composio_api_key)


result = {
    "result": "NULL"
}


def send_mail():
    print(f">>>>> send_mail() using user_id=rnemzek_composio_poc")
    # Execute the send email action
    # 'user_id' is your stable identifier for the authenticated Gmail account
    try:
        result = composio.tools.execute(
            user_id="rnemzek_composio_poc",
            slug="GMAIL_SEND_EMAIL",
            arguments={
                "to": "rnemzek+composio-poc@gmail.com",
                "subject": "Composio 0.11.1 test: " + timestamp,
                "body": "This message was sent using the simplified Composio SDK.",
                "is_html": False,
                "from_email": "Composio Bot <rnemzek+composio-poc@gmail.com>"
            },
            version="20260227_00"
        )
        print(f">>>>> SENT EMAIL")
        return result
    except Exception as e:
        print(f">>>>> Error: {e}")


send_mail()
output = json.dumps(result)


if output is not None:
    print(f">>>>> output: " + output)

else:
    print(f">>>>> output is NULL!")


