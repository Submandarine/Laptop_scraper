import re
import numpy as np
import sys
from typing import Literal

deb = False


def _debug(message):
    if deb:
        print(message)


def p_tuple_count():
    tuple_def = [
        (
            " active tuples min-mean-max : 21168776,21168776,21168777",
            ["21168776", "21168776", "21168777"],
            np.int32,
        ),
    ]


digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
allowed_chars = {
    "int": digits + ["-"],
    "float": digits + ["-", "."],
    "float_german": digits + ["-", ","],
    "float_exp": digits + ["-", ".", "e", "E", "+"],
    "float_exp_german": digits + ["-", ",", "e", "E", "+"],
    "time": digits + [":"],
}


def parse_relative_to(
    input: str,
    search_term: str,
    v_offset: int,
    h_offset: int,
    type: Literal["int", "float", "float_exp", "float_german", "float_exp_german", "time", "custom"],
    on_error: Literal["die, warn, ignore, fill"] = "warn",
    error_fill=None,
    custom_delim=None,
    parse_start=None,
    parse_end=None,
):
    """
    Parses values near a search_term \n
    E.g. parse_relative_to(log_file, "Performance (FLOPS)", 2, 18, "float")
    searches for "Performance (FLOPS)", sets the position of "P" as anchor,
    then parses a float two lines below and 18 chars to the right of the anchor.\n
    This process is repeated for all occurrences of "Performance (FLOPS)"

    Args:
        input: String to parse
        search_term: anchor of the search
        h_offset: how many lines to go down or up from the anchor
        v_offset: how many characters to go left or right from the anchor
        type: type of the value to parse, supports int, float, float in exponential notation, time in format xx:xx:xx

    Returns:
        A List of parsed values for each occurrence of search_term
    """
    if parse_start != None and parse_end != None:
        input = input[input.index(parse_start) : input.index(parse_end)]
    elif parse_start != None:
        input = input[input.index(parse_start) :]
    elif parse_end != None:
        input = input[: input.index(parse_end)]

    input_lines = input.splitlines()
    anchors = []  # list of (line, index) tuples
    for i in range(len(input_lines)):
        occ = re.finditer(re.escape(search_term), input_lines[i])
        for o in occ:
            anchors.append((i, o.start()))

    _debug(f"{anchors=}")

    if len(anchors) == 0:
        _debug(f"the search_term was not discovered in input")
        return []

    search_indices = [(line + v_offset, ind + h_offset) for line, ind in anchors]
    values = []
    for line, ind in search_indices:
        try:
            value = _find_value_at(input_lines[line], ind, type, custom_delim)
            values.append(value)
            _debug(f"found value {value}")
        except RuntimeError:
            if on_error == "ignore":
                continue
            elif on_error == "fill":
                values.append(error_fill)
            elif on_error == "die":
                sys.exit(
                    f'for input line {line} index {ind} points to region {input[ind-3: ind+3]} where no part of type "{type}" was found'
                )
            elif on_error == "warn":
                raise RuntimeWarning(
                    f'for input line {line} index {ind} points to region {input[ind-3: ind+3]} where no part of type "{type}" was found"'
                )
    _debug(f"{values=}")
    return values


def _find_value_at(
    input: str,
    index: int,
    type: Literal["int", "float", "float_german", "float_exp", "float_exp_german", "time", "custom"],
    custom_delim: None,
):
    """
    Given an input string and an index of a value of type this returns the value no matter where the position in the value
    e.g. for string "example 142.3233", index 9 and type float it will return 142.3233 even though the index didn't point to the start of the value

    Args:
        input: a line to search in
        index: index to search for a value
        type: value to search for
    Returns:
        Detected value
    """
    if type == "custom":
        if input[index] in custom_delim:
            raise RuntimeError("start char is delimiter")
        start = end = index
        while start > 0 and input[start - 1] not in custom_delim:
            start -= 1
        while end < len(input) and input[end] not in custom_delim:
            end += 1
    else:
        if not type in allowed_chars.keys():
            sys.exit(f'type not defined: "{type} choose from {allowed_chars.keys()}"')

        chars = allowed_chars[type]
        if input[index] not in chars:
            raise RuntimeError("no value found")

        start = end = index
        while start > 0 and input[start - 1] in chars:
            start -= 1
        while end < len(input) and input[end] in chars:
            end += 1
    return input[start:end]


def time_to_seconds(time):
    hours = int(time[0:2])
    minutes = int(time[3:5])
    seconds = float(time[6:12].replace(",", "."))
    return hours * 60 * 60 + minutes * 60 + seconds


def conv_german_to_float(input: str):
    for c in input:
        if c not in allowed_chars.get("float_german"):
            sys.exit(f'input "{input}" has invalid character: "{c}"')

    return float(input.replace(",", "."))


# returns a list corresponding to the deltas between values (used for timestamp -> duration)
def list_to_deltas(lis: list):
    return [lis[i] - lis[i - 1] for i in range(1, len(lis))]
