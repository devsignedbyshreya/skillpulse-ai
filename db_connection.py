from databricks import sql
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():

    print("=" * 50)
    print("HOST:", repr(os.getenv("DATABRICKS_SERVER_HOSTNAME")))
    print("PATH:", repr(os.getenv("DATABRICKS_HTTP_PATH")))
    print("TOKEN PREFIX:", repr(os.getenv("DATABRICKS_TOKEN")[:20]))
    print("=" * 50)

    return sql.connect(
        server_hostname=os.getenv(
            "DATABRICKS_SERVER_HOSTNAME"
        ),
        http_path=os.getenv(
            "DATABRICKS_HTTP_PATH"
        ),
        access_token=os.getenv(
            "DATABRICKS_TOKEN"
        )
    )