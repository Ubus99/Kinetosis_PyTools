import json
import os

from platformdirs import user_cache_dir


class CacheHandler:
    def __init__(self, name: str, author: str) -> None:
        print("loading cash for " + author + ", " + name)

        self.data = {}
        self.path = None

        self.load(name, author)

    def __del__(self):
        self.save()

    def __getitem__(self, key: str):
        try:
            return self.data[key]
        except KeyError:
            return None

    def __setitem__(self, key: str, value):
        self.data[key] = value

    def load(self, name: str, author: str):
        self.path = user_cache_dir(name, author)
        os.makedirs(self.path, exist_ok=True)

        try:
            self.data = json.load(open(self.path + "/settings.json", mode="r", encoding="utf-8"))
            print("cache file found")
            print(self.data)

        except json.decoder.JSONDecodeError:
            # traceback.print_exc()
            print("creating new cache file")
            self.data = {}

    def save(self):
        print("storing cache at " + self.path + "\n")
        json.dump(self.data, open(self.path + "/settings.json", mode="w", encoding="utf-8"))
