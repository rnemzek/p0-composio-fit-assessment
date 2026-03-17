import os
import sys
import json
from composio import Composio
from src.utils.util import Util, loadenv
loadenv()

USAGE = """
Usage:
    python -m src.tests.test_send_gmail <Repo> <Subject> <Body>

Arguments:
    Repo     The GitHub repository name (e.g., my-org/my-repo)
    Subject  The email subject line
    Body     The email body text

Example:
    python -m src.tests.test_send_gmail my-org/my-repo "Alert: PR opened" "A new pull request was opened in my-org/my-repo."
"""

def validate_args():
    if len(sys.argv) < 4:
        missing = []
        if len(sys.argv) < 2:
            missing.append("Repo")
        if len(sys.argv) < 3:
            missing.append("Subject")
        if len(sys.argv) < 4:
            missing.append("Body")
        print(f"ERROR: Missing required argument(s): {', '.join(missing)}")
        print(USAGE)
        sys.exit(1)

    repo    = sys.argv[1].strip()
    subject = sys.argv[2].strip()
    body    = sys.argv[3].strip()

    errors = []
    if not repo:
        errors.append("Repo cannot be empty")
    if not subject:
        errors.append("Subject cannot be empty")
    if not body:
        errors.append("Body cannot be empty")

    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        print(USAGE)
        sys.exit(1)

    return repo, subject, body


def send_mail(repo, subject, body):
    timestamp = Util().getDateTimestamp()
    composio_api_key = os.getenv("COMPOSIO_API_KEY")
    user_id          = os.getenv("GMAIL_COMPOSIO_CONNECTION_ACCOUNT_USER_ID")
    slug             = os.getenv("GMAIL_SLUG")
    to_email         = os.getenv("GMAIL_TO")
    from_email       = os.getenv("GMAIL_FROM")
    bot_version      = os.getenv("GMAIL_BOT_VERSION")

    missing_env = [k for k, v in {
        "COMPOSIO_API_KEY":                          composio_api_key,
        "GMAIL_COMPOSIO_CONNECTION_ACCOUNT_USER_ID": user_id,
        "GMAIL_SLUG":                                slug,
        "GMAIL_TO":                                  to_email,
        "GMAIL_FROM":                                from_email,
        "GMAIL_BOT_VERSION":                         bot_version,
    }.items() if not v]

    if missing_env:
        print(f"ERROR: Missing required environment variable(s): {', '.join(missing_env)}")
        sys.exit(1)

    print(f">>>>> {timestamp}")
    print(f">>>>> Creating Composio client (version={bot_version})")
    composio = Composio(api_key=composio_api_key)

    full_subject = f"{timestamp} : [{repo}] {subject}"

    print(f">>>>> send_mail() user_id={user_id} slug={slug}")
    print(f">>>>> To: {to_email} | From: {from_email}")
    print(f">>>>> Subject: {full_subject}")

    try:
        result = composio.tools.execute(
            user_id=user_id,
            slug=slug,
            arguments={
                "to":         to_email,
                "subject":    full_subject,
                "body":       body,
                "is_html":    False,
                "from_email": from_email,
            },
            version=bot_version,
        )
        print(f">>>>> EMAIL SENT")
        print(f">>>>> result: {json.dumps(result)}")
        return result
    except Exception as e:
        print(f">>>>> Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    repo, subject, body = validate_args()
    send_mail(repo, subject, body)
