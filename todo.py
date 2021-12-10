import json
import os
import sys

import msal
import requests as requests

from config import MICROSOFT_ENDPOINT
from notification import Notification


class ToDo:
    def __init__(self):
        try:
            self.token = None
            results = ToDo.obtain_bearer()
            if 'error' in results:
                Notification.send_notification(
                    f"Failed to obtain Bearer token for Microsoft ToDo \n- {results['error_description']}", True, 10)
            if "access_token" in results:
                self.token = results['access_token']
                # Calling graph using the access token
                graph_data = requests.get(  # Use token to call downstream service
                    MICROSOFT_ENDPOINT,
                    headers={'Authorization': 'Bearer ' + self.token}, ).json()
                Notification.send_notification(
                    f"Connected to Microsoft ToDo - " + json.dumps(graph_data, indent=2))
            else:
                Notification.send_notification(
                    f"Failed to connect to Microsoft ToDo - " + results.get("error_description"))
        except KeyError:
            sys.exit("Failed to obtain Bearer token")

    @staticmethod
    def obtain_bearer():
        app = msal.ConfidentialClientApplication(
            os.getenv('AZURE_ID'), authority=f"https://login.microsoftonline.com/{os.getenv('AZURE_TENET_ID')}",
            client_credential=os.getenv('AZURE_SECRET'),
        )
        return app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])

    def add_task(self, text, task_list_id):
        body = {
            "title": text,
        }
        res = requests.post(f"https://graph.microsoft.com/v1.0/me/todo/lists/{task_list_id}/tasks",
                            json.dumps(body, indent=4), headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.token}"
            })
        print(res.json())
