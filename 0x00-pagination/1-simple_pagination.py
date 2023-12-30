#!/usr/bin/env python3
"""
"""
import csv
import math
from typing import List


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
        Paginates data and returns the results within the index_range.

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
