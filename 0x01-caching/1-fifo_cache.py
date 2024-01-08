#!/usr/bin/env python3
"""
A class `FIFOCache` that inherits from `BaseCaching` and is
a caching system:

- You must use `self.cache_data` - dictionary from the parent
  class `BaseCaching`
- You can overload `def __init__(self):` but don't forget to
  call the parent init: `super().__init__()`
- `def put(self, key, item):`
  • Must assign to the dictionary `self.cache_data` the `item`
    value for the key `key`.
  • If `key` or `item` is `None`, this method should not do
    anything.
  • If the number of items in `self.cache_data` is higher than
    `BaseCaching.MAX_ITEMS`:
    - you must discard the first item put in cache (FIFO algorithm).
    - you must print `DISCARD:` with the `key` discarded and
      following by a new line.
- `def get(self, key):`
  • Must return the value in `self.cache_data` linked to `key`.
  • If `key` is `None` or if the `key` doesn't exist in
    `self.cache_data`, return `None`.
"""
from base_caching import BaseCaching
from collections import OrderedDict


class FIFOCache(BaseCaching):
    """
    Inherits from BaseCaching and is a caching system.
    Implements the FIFO caching replacement algorithm.
    """
    def __init__(self):
        """
        Initializes the cache.
        """
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """
        Stores an `item` in the cache.

        Arguments:
            - `key`: The key of the item to store.
            - `item`: The item to store.
        """
        if key is None or item is None:
            return
        self.cache_data[key] = item
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            first_key, _ = self.cache_data.popitem(False)
            print("DISCARD:", first_key)

    def get(self, key):
        """
        Retrieves an `item` by `key` from cache.

        Arguments:
            - `key`: The key of the stored item.
        """
        return self.cache_data.get(key, None)
