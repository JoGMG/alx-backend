"""
A function named `index_range` that takes two integer arguments
`page` and `page_size`. The function should return a tuple of size
two containing a start index and an end index corresponding to the
range of indexes to return in a list for those particular pagination
parameters. Page numbers are 1-indexed, i.e. the first page is page 1.
"""

def index_range(page :int, page_size :int) -> tuple:
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
