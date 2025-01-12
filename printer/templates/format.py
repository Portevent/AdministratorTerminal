from printer.driver import ThermalPrinter

import pdf417


class DefaultFormat:
    @staticmethod
    def custom_center(buff: str, width: int = 42, border: int = 0, dash:str = "-"):
        """
        Centers the buffer within equal sized dashed lines
        :param buff: Buffer to center
        :param width: Width of the page
        :param border: Border left and right of the lines
        :param dash: Dash character
        """

        # 123456789012345678901234567890123456789012
        #  ---------------- bonjour -------------- 
        #                  -- bLen--
        b_len = len(buff) + 2

        r_width = width - 2 * border
        n_dash = r_width - b_len

        r_pad = n_dash // 2
        l_pad = r_pad + n_dash % 2

        return " " * border + dash * r_pad + " " + buff + " " + dash * l_pad


    @staticmethod
    def format_long(buff: str, max_len: int = 42, first_len: int = 42):
        """
        Formats a long text by splitting it into multiple lines according to a fixed wisth so that no words are cut
        :param buff: Buffer to format
        :param max_len: Max length of the output
        :param first_len: First length of the output (In case of set title, with different format)
        """
        line_index = 0
        out = [""]

        for word in buff.split(" "):
            if (len(out[line_index]) + len(word) + 1 > max_len and line_index > 0) or (len(out[line_index]) + len(word) + 1 > first_len and line_index == 0):
                out.append("")
                line_index += 1

            if len(out[line_index]) > 0:
                out[line_index] += " "

            out[line_index] += word

        # print(out)
        # print("************\n"+"\n".join(out)+"\n************")

        return " " + "\n ".join(out)

    @staticmethod
    def print_center(printer: ThermalPrinter, buff: str, width: int = 42, border: int = 0, dash: str = '-'):
        """
        Prints a text in the center, falling back to default settings
        :param printer: Printer
        :param buff: Buffer to print
        :param width: Width of the page
        :param border: Border left and right of the lines
        :param dash: Dash character
        """

        printer.set_with_default(align="center")
        printer.text(DefaultFormat.custom_center(buff, width=width, border=border, dash=dash) + "\n")

        printer.set_with_default()


    @staticmethod
    def print_pdf417(printer: ThermalPrinter, buff: str):
        """
        Print a formatted pdf417 barcode
        :param printer: Printer
        :param buff: Buffer to print
        """
        code = pdf417.encode(buff, columns=4)
        image = pdf417.render_image(code)

        printer.text("\n")
        printer.image(image, center=True)
        printer.text("\n")

    @staticmethod
    def print_long_field(printer: ThermalPrinter, name: str, value: str, end: str=""):
        """
        Print a field that takes the whole width
        :param printer: Printer
        :param name: Name of the field
        :param value: Value of the field
        :param end: End of the print sequence
        """
        printer.set_with_default(bold=False)
        printer.text(" " + name + " :")
        printer.set_with_default(bold=True)
        printer.text(DefaultFormat.format_long(value, max_len=41, first_len=41 - (len(name) + 2)) + end)

    @staticmethod
    def print_short_field(printer: ThermalPrinter, name: str, value: str, end=""):
        """??????"""
        printer.set_with_default(bold=False)
        printer.text(" " + name + ":" + (" " * (19 - len(name))))
        printer.set_with_default(bold=True)
        printer.text(value + end)

    @staticmethod
    def print_double_field(printer: ThermalPrinter, name1: str, value1: str, name2: str, value2: str, end: str = ""):
        """
        Prints a double field that takes the whole width
        :param printer: Printer
        :param name1: Name of the first field
        :param value1: Value of the first field
        :param name2: Name of the second field
        :param value2: Value of the second field
        :param end: end if custom
        """
        printer.set_with_default(bold=False)
        printer.text(" " + name1 + ": ")
        printer.set_with_default(bold=True)
        printer.text(value1 + " " * (18 - len(name1) - len(value1)))
        printer.set_with_default(bold=False)
        printer.text(name2 + ": ")
        printer.set_with_default(bold=True)
        printer.text(value2 + end)