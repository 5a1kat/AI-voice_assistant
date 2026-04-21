import json
import webbrowser
import os

class WebsiteManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.websites = self.load_websites()

    def load_websites(self):
        if not os.path.exists(self.file_path):
            print("websites.json not found!")
            return {}

        with open(self.file_path, "r") as file:
            return json.load(file)

    def open_website(self, name):
        name = name.lower().strip()

        # remove .com, .in, .org in voice input
        for ext in [".com", ".in", ".org", ".net", ".co", ".co.in", ".co.uk"]:
            name = name.replace(ext, "")

        if name in self.websites:
            url = self.websites[name]
            webbrowser.open(url)
            return True
        else:
            return False