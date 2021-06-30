from typing import Any, List, Optional

# Globals (ugly I know)
table_char = "│─┌┬┐├┼┤└┴┘"
SIDE, TOP, TOP_LEFT, TOP_T, TOP_RIGHT, SIDE_LEFT, SIDE_T, SIDE_RIGHT, BOTTOM_LEFT, BOTTOM_T, BOTTOM_RIGHT = range(
    11)


def make_table(rows: List[List[Any]], labels: Optional[List[Any]] = None, centered: bool = False) -> str:
    # Prep table of data for table
    table = ""

    # get number of rows and number of cols
    num_of_rows = len(rows)
    num_of_cols = len(rows[0])

    """
    Pre-calculate max-width for rows
    """

    max_length = calculate_max_padding(rows, labels, num_of_rows, num_of_cols, centered)

    """
    Parse table display
    """

    for i in range(num_of_rows + 3):
        if i == 0:
            # Add top line
            table += (line_break(max_length) + "\n")
        elif i == 1:
            # check for labels and add if any
            if labels:
                line = table_char[SIDE]
                for j in range(num_of_cols):
                    padded_word = padded_text(labels[j], max_length[j], centered)
                    line += padded_word
                    line += table_char[SIDE]
                table += (line + "\n")
                table += (line_break(max_length, "middle") + "\n")
        elif i < num_of_rows + 2:
            # Add the rest of the rows
            line = table_char[SIDE]
            for j in range(num_of_cols):
                padded_word = padded_text(rows[i - 2][j], max_length[j], centered)
                line += padded_word
                line += table_char[SIDE]
            table += (line + "\n")
        else:
            # Add bottom line
            table += (line_break(max_length, "bottom"))

    return table


def calculate_max_padding(rows, labels, num_of_rows, num_of_cols, centered):
    """
    Calculates max padding based on factors such as centering and biggest words in columns
    """

    max_length = [0] * num_of_cols

    if centered:
        padding_l = 2
    else:
        padding_l = 2

    if labels:
        for l in range(len(labels)):
            max_length[l] = len(str(labels[l])) + padding_l

    for i in range(num_of_rows):
        for j in range(num_of_cols):
            len_curr_word = len(str(rows[i][j])) + padding_l
            if len_curr_word > max_length[j]:
                max_length[j] = len_curr_word
    return max_length


def line_break(max_length, align="top"):
    """
    Creates the line break whether it be for the top, middle or bottom of table
    and returns it as string
    """
    if align == "top":
        left, middle, right = TOP_LEFT, TOP_T, TOP_RIGHT
    elif align == "bottom":
        left, middle, right = BOTTOM_LEFT, BOTTOM_T, BOTTOM_RIGHT
    else:
        left, middle, right = SIDE_LEFT, SIDE_T, SIDE_RIGHT

    lb = table_char[left]
    for i in range(len(max_length)):
        if i == 0:
            lb += table_char[TOP] * max_length[i]
        else:
            lb += table_char[middle] + table_char[TOP] * max_length[i]
    lb += table_char[right]
    return lb


def padded_text(word, max_length, centered):
    """
    Returns padded text with spaces (centered or not)
    """

    word_str = str(word)
    len_word = len(word_str)

    if centered:
        len_pad = max_length - len_word
        if len_pad % 2 == 0:
            pad = int(len_pad / 2)
            l, r = pad, pad
        else:
            l = int(len_pad / 2)
            r = len_pad - l
        return (" " * l) + word_str + (" " * r)
    return " " + word_str + " " * (max_length - len_word - 1)
