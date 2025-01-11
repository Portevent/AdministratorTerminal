"""
Simple text formatter
"""

class TextFormater:
    """
    Simple Text Formatter helping class
    """

    @staticmethod
    def _get_line(left_txt: str = "", middle_txt: str = "", right_txt: str = "",
                  width: int = 10, space_between: bool = True, filling: str = "=") -> str:
        """
        Generate a line
        :param left_txt: Text on the left side
        :param middle_txt: Text in the middle
        :param right_txt: Text on the right side
        :param width: Width of the line
        :param space_between: Put space between the fillingchar
        :param filling: Character used to fill the line
        :return: String
        """
        first_half: int = int(width / 2) - int(len(middle_txt) / 2) - len(left_txt) - (2 if space_between else 0)
        second_half: int = width - len(left_txt + middle_txt + right_txt) - (4 if space_between else 0) \
                           - first_half - 1
        return left_txt + (" " if space_between else "") \
            + filling * first_half + (" " if space_between else "") \
            + middle_txt + (" " if space_between else "") \
            + filling * second_half + (" " if space_between else "") \
            + right_txt

    @staticmethod
    def override(first_str, second_str):
        """
        Override second str with first str
        ABC, 0123456 -> ABC3456
        :param first_str:
        :param second_str:
        :return:
        """
        return first_str + second_str[len(first_str):]