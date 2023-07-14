import itertools


def slice_dict(start_dict: dict[str, str], num_elements: int) -> tuple [dict[int, dict[str, str]], int]:
    result_dict: dict[int, dict[str, str]] = {}
    cursor = 0
    num_pages = len(start_dict) // num_elements
    add_pager = len(start_dict) % num_elements

    for i in range(num_pages):
        temp_dict: dict[str: str] = dict(itertools.islice(start_dict.items(), cursor, cursor + num_elements))
        result_dict.update({i: temp_dict})
        cursor += num_elements


    if add_pager != 0:
        temp_dict: dict[str: str] = dict(itertools.islice(start_dict.items(), cursor, len(start_dict)))
        result_dict.update({num_pages: temp_dict})
        num_pages += 1


    return result_dict, num_pages
