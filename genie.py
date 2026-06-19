import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("DATABRICKS_SERVER_HOSTNAME")
TOKEN = os.getenv("DATABRICKS_TOKEN")
SPACE_ID = os.getenv("GENIE_SPACE_ID")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}


def ask_genie(question):

    start_url = (
        f"https://{HOST}"
        f"/api/2.0/genie/spaces/{SPACE_ID}/start-conversation"
    )

    response = requests.post(
        start_url,
        headers=HEADERS,
        json={"content": question}
    ).json()

    conversation_id = response["conversation_id"]

    messages_url = (
        f"https://{HOST}"
        f"/api/2.0/genie/spaces/{SPACE_ID}"
        f"/conversations/{conversation_id}/messages"
    )

    for _ in range(20):

        time.sleep(2)

        messages = requests.get(
            messages_url,
            headers=HEADERS
        ).json()

        if not messages.get("messages"):
            continue

        msg = messages["messages"][0]

        if msg.get("status") != "COMPLETED":
            continue

        answer_text = ""
        sql_query = None

        attachments = msg.get(
            "attachments",
            []
        )

        for item in attachments:

            if (
                "text" in item
                and "content" in item["text"]
            ):
                answer_text = item["text"]["content"]

            if (
                "query" in item
                and "query" in item["query"]
            ):
                sql_query = item["query"]["query"]

        return {
            "answer": answer_text,
            "sql": sql_query
        }

    return {
        "answer": "No answer returned.",
        "sql": None
    }