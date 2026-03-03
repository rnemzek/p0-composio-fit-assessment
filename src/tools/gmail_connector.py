import logging
#import json

logger = logging.getLogger("agent_logger")

#class FauxGmailConnector:
#    def send_log_email(self, payload):
#        # Just logging the 'send' action for the visualizer
#        logger.info(f"GMAIL_TOOL: Sending email summary for {len(payload)} items...")
#        return {"status": "success", "meta": payload}

class GmailConnector:
    def send_mail(self, subject, body):
        # Just logging the 'send' action for the visualizer
        logger.info(f"GMAIL_TOOL: Sending email | summary: " + subject + " body: " + body)
#        return {"status": "success", "meta": payload}

# NEW IMPL BELOW
        # necessary imports
        import os
        import json
        from composio import Composio
        from src.tests.utils.util import getDateTimestamp

        # get the following:
        #    1) date/timestamp
        #    2) get COMPOSIO_API_KEY
        #    3) create composio object
        #    4) get account_user_id
        #    5) get slug
        #    6) get "to" 
        #    7) get "from" 
        #    8) get "bot version" 
        timestamp = getDateTimestamp()
        logger.info("GMAIL_TOOL: timestamp=" + timestamp)
        composio_api_key = os.environ.get("COMPOSIO_API_KEY")
        logger.info("GMAIL_TOOL: composio_api_key=%s", composio_api_key)
#        composio = Composio(api_key=composio_api_key)
        composio = Composio(
            api_key="ak_NguOTc4AwH4s0Qu_KUQ7",
            toolkit_versions={"gmail": "20260227_00"}
        )

        if composio is not None:
            logger.warning("GMAIL_TOOL: composio is not None")
        else:
            logger.warning("GMAIL_TOOL: composio is None")
        logger.info("get: GMAIL_ACCOUNT_USER_ID")
#        account_user_id = os.environ.get("GMAIL_ACCOUNT_USER_ID")
        account_user_id = "rnemzek_composio_poc"
        logger.info(f"got: %s", account_user_id)
        logger.info("GMAIL_TOOL: account_user_id=" + account_user_id)
        gmail_slug = os.environ.get("GMAIL_SLUG")
        logger.info("GMAIL_TOOL: gmail_slug=" + gmail_slug)
        gmail_to = os.environ.get("GMAIL_TO")
        logger.info("GMAIL_TOOL: gmail_to=" + gmail_to)
        gmail_from = os.environ.get("GMAIL_FROM")
        logger.info("GMAIL_TOOL: gmail_from=" + gmail_from)
        gmail_bot_version = os.environ.get("GMAIL_BOT_VERSION")
        logger.info(f"GMAIL_TOOL: gmail_bot_version=" + gmail_bot_version)

#        logger.info(f"GMAIL_TOOL: timestamp=" + timestamp +
#                    " composio_api_key: " + composio_api_key +
#                    " account_user_id: " + account_user_id +
#                    " gmail_slug: " + gmail_slug +
#                    " gmail_to: " + gmail_to +
#                    " gmail_from: " + gmail_from +
#                    " gmail_bot_version: " + gmail_bot_version)

        # Execute the send email action
        # 'user_id' is your stable identifier for the authenticated Gmail account
        try:
#            result = composio.tools.execute(
#                user_id="rnemzek_composio_poc",
#                user_id=account_user_id,
#                slug="GMAIL_SEND_EMAIL",
#                user_id=account_user_id,
#                entity_id=account_user_id,
#                arguments={
#                    "to": "rnemzek+composio-poc@gmail.com",
#                    "to": gmail_to,
#                    "subject": "Composio 0.11.1 test: " + timestamp,
#                    "subject": subject,
#                    "body": "This message was sent using the simplified Composio SDK.",
#                    "body": body,
#                    "is_html": False,
#                    "from_email": "Composio Bot <rnemzek+composio-poc@gmail.com>",
#                    "from_email": gmail_from
#                },
#                version=gmail_bot_version
#            )

            result = composio.tools.execute(
                user_id=account_user_id,
#                entity_id=account_user_id,
                slug=gmail_slug,
                arguments={
                    "to": gmail_to,
                    "subject": subject,
                    "body": body,
                    "is_html": False,
                    "from_email": gmail_from,
                },
                version=gmail_bot_version
            )
            return result
        except Exception as e:
            logger.warn(f"GMAIL_TOOL: Sending email errored. Exception: {e}")
            return

#send_mail()
#output = json.dumps(result)
