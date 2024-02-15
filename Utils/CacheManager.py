import json
import os
from typing import Any

from platformdirs import user_cache_dir


class CacheManager:
    def __init__(self, name: str, author: str) -> None:
        """
        Creates a cache object that can read and write JSON files to the standard cache directory \n
        Access using the indexing operator [] as a dict \n
        will automatically store all contained information on application exit
        :param name: name of the Application
        :param author: Application Author to determine cache path
        """
        print("loading cache for " + author + ", " + name)

        self.data = {}

        self.path = None

        self.load(name, author)

    def __del__(self):
        """
        saves cache on object delete
        """
        self.save()

    def __getitem__(self, key: str) -> object:
        """
        Index function for cache object todo
        :param key: key of requested dataset
        :return: returns object of indeterminate type from dict
        """
        try:
            return self.data[key]
        except KeyError:
            return None

    def __setitem__(self, key: str, value):
        self.data[key] = value

    def load(self, name: str, author: str) -> None:
        """
        loads cache object from file manually, will replace any previous contents!
        
        :param name: name of the Application
        :param author: Application Author to determine cache path
        """
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

    def save(self) -> None:
        """
        saves cache to file
        """
        print("storing cache at " + self.path + "\n")
        json.dump(self.data, open(self.path + "/settings.json", mode="w", encoding="utf-8"))
