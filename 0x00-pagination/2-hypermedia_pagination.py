#!/usr/bin/env python3
"""
Implements a `get_hyper` method that takes the same arguments
(and defaults) as `get_page` and returns a dictionary containing
the following key-value pairs:
    - `page_size`: the length of the returned dataset page
    - `page`: the current page number
    - `data`: the dataset page (equivalent to return from previous task)
    - `next_page`: number of the next page, `None` if no next page
    - `prev_page`: number of the previous page, `None` if no previous page
    - `total_pages`: the total number of pages in the dataset as an integer
Make sure to reuse `get_page` in your implementation.
"""
import csv
import math
from typing import List, Dict


def index_range(page: int, page_size: int) -> tuple:
    """
    Returns a tuple containing the start and end index for
    a page based on the `page` and `page_size` parameters.

    Arguments:
        - `page`: page number
        - `page_size`: size of page
    """
    end_index = page * page_size
    start_index = end_index - page_size
    return start_index, end_index


class Server:
    """
    Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """
        Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Paginates and returns data results within the index start
        and end range.

        Arguments:
            - `page`: page number
            - `page_size`: size of page
        """
        assert (isinstance(page, int) and page > 0
                and isinstance(page_size, int) and page_size > 0)
        start, end = index_range(page, page_size)
        data = self.dataset()
        if start > len(data):
            return []
        return data[start:end]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict:
        """
        Paginates and returns data results within the index start
        and end range along with pagination parameters.

        Arguments:
            - `page`: page number
            - `page_size`: size of page
        """
        data = self.dataset()
        page_data = self.get_page(page, page_size)
        start, end = index_range(page, page_size)
        result = {
            "page_size": len(page_data),
            "page": page,
            "data": page_data,
            "next_page": page + 1 if end < len(data) else None,
            "previous_page": page - 1 if start > 0 else None,
            "total_pages": math.ceil(len(data) / page_size)
        }
        return result
