from enum import Enum, auto


class Error(Enum):
    FILETYPE = ("Invalid File Type")

    TOOFEWINSTANCES = ("You May Have Multiple Sheets in Your Excel File")

    NOXCOL = ("Please Choose an X Column")

    NOYCOL = ("Please Choose a Y column")

    def __init__(self, message):
        self.message = message
