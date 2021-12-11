import os

import requests as requests
from win32gui import GetWindowText, GetForegroundWindow

from config import TODOIST_API, TODOIST_PROJECT, TODOIST_DEFAULT_DUE
from notification import Notification


class ToDo:
    def __init__(self):
        if os.getenv('TODOIST_TOKEN') == "":
            Notification.send_notification(f"Missing Todoist api token", True, 10)
        self.project = ToDo.get_project(TODOIST_PROJECT)
        Notification.send_notification(f"Connected to Todoist - Project {TODOIST_PROJECT}")

    @staticmethod
    def get_project(requested_project):
        projects = requests.get(f"{TODOIST_API}/projects", headers={
            "Authorization": f"Bearer {os.getenv('TODOIST_TOKEN')}"
        }).json()
        for project in projects:
            if project["name"].lower() == requested_project.lower():
                return project["id"]

        # Project not found - will create new one
        result = requests.post(f"{TODOIST_API}/projects", data={"name": requested_project}, headers={
            "Authorization": f"Bearer {os.getenv('TODOIST_TOKEN')}"
        }).json()
        if "id" in result:
            return result["id"]
        Notification.send_notification("failed to obtain project ID for Todoist", True)

    @staticmethod
    def get_title():
        title = GetWindowText(GetForegroundWindow())
        title = title.replace(" - Google Chrome", "")
        return title

    def add_task(self, text):

        result = requests.post(f"{TODOIST_API}/tasks", data={
            "content": f"{ToDo.get_title()}: {text[0:80]}",
            "description": text,
            "project_id": self.project,
            "due_string": TODOIST_DEFAULT_DUE
        }, headers={
            "Authorization": f"Bearer {os.getenv('TODOIST_TOKEN')}"
        }).json()
        if "id" in result:
            Notification.send_notification(f"New task added - \n {text}")
        else:
            Notification.send_notification(f"Failed to add task")
