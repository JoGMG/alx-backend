#!/usr/bin/env python3
"""
A class `LFUCache` that inherits from `BaseCaching` and is
a caching system:

- You must use `self.cache_data` - dictionary from the parent
  class `BaseCaching`
- You can overload `def __init__(self):` but don't forget to
  call the parent init: `super().__init__()`
- `def put(self, key, item):`
  • Must assign to the dictionary `self.cache_data` the
    `item` value for the key `key`.
  • If `key` or `item` is `None`, this method should not do
    anything.
  • If the number of items in `self.cache_data` is higher than
    `BaseCaching.MAX_ITEMS`:
    - you must discard the least frequency used item (LFU algorithm).
    - if you find more than 1 item to discard, you must use the LRU
      algorithm to discard only the least recently used.
    - you must print `DISCARD:` with the `key` discarded and following
      by a new line.
- `def get(self, key):`
  • Must return the value in `self.cache_data` linked to `key`.
  • If `key` is `None` or if the `key` doesn't exist in
    `self.cache_data`, return `None`.
"""
from base_caching import BaseCaching
from collections import defaultdict


class LFUCache(BaseCaching):
    """
    Inherits from BaseCaching and is a caching system.
    Implements the LFU caching replacement algorithm.
    """
    def __init__(self):
        """
        Initializes the cache.
        """
        super().__init__()
        self.cache_data = {}
        self.freq_map = defaultdict(list)
        self.min_freq = 0
        self.key_freq = {}

    def put(self, key, item):
        """
        Stores an `item` in the cache.

        Arguments:
            - `key`: The key of the item to store.
            - `item`: The item to store.
        """
        if key is None or item is None:
            return
        if key not in self.cache_data:
            if len(self.cache_data) + 1 > BaseCaching.MAX_ITEMS:
                lfu_key = self.freq_map[self.min_freq].pop(0)
                self.cache_data.pop(lfu_key)
                self.key_freq.pop(lfu_key)
                print("DISCARD:", lfu_key)
            self.cache_data[key] = item
            self.key_freq[key] = 1
            self.freq_map[1].append(key)
            self.min_freq = 1
        else:
            self.cache_data[key] = item
            self.__update(key)

    def get(self, key):
        """
        Retrieves an `item` by `key` from cache.

        Arguments:
            - `key`: The key of the stored item.
        """
        if key is not None and key in self.cache_data:
            self.__update(key)
        return self.cache_data.get(key, None)

    def __update(self, key):
        """
        Updates the frequency of a key.

        Argument:
            - `key`: The key to update frequency.
        """
        freq = self.key_freq[key]
        self.freq_map[freq].remove(key)
        if not self.freq_map[freq]:
            self.freq_map.pop(freq)
            if self.min_freq == freq:
                self.min_freq += 1
        self.key_freq[key] += 1
        self.freq_map[self.key_freq[key]].append(key)
