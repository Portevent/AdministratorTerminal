from escpos.printer import Usb


def init_printer():
    return Usb(0x04b8, 0x0202, 0, profile="TM-T88V")


def ola():
    p.set_with_default(bold=True)
    p.image("logo.png", center=True)

    p.text("\n")
    p.text("\n")

    p.text(" ------ Transmission ------ ")
    p.text("\n  Source: ola\n  Dest: bite\n\n  Title: olaaaa")




def custom_center(buff, width=42, border=0, dash="-"):
    # 123456789012345678901234567890123456789012
    #  ---------------- bonjour -------------- 
    #                  -- bLen--
    bLen = len(buff) + 2 

    rWidth = width - 2*border
    nDash = rWidth - bLen

    rPad = nDash // 2
    lPad = rPad + nDash % 2

    return " "*border + dash*rPad + " " + buff + " " + dash*lPad


def print_center(p, buff, width=42, border=0, dash='-'):
    p.set_with_default(align="center")
    p.text(custom_center(buff, width=width, border=border, dash=dash) + "\n")

    p.set_with_default()


import pdf417

def print_pdf417(p, buff):
    code = pdf417.encode(buff, columns=4)
    image = pdf417.render_image(code)

    im = image #._im.convert("RGB")

    p.text("\n")
    p.image(im, center=True)
    p.text("\n")

def format_long(buff, maxLen=42, firstLen=42):
    i = 0
    out = [""]

    for word in buff.split(" "):
        if (len(out[i]) + len(word) + 1 > maxLen and i > 0) or (len(out[i]) + len(word) + 1 > firstLen and i == 0) :
            out.append("")
            i += 1

        if len(out[i]) > 0:
            out[i] += " "

        out[i] += word

    # print(out)
    # print("************\n"+"\n".join(out)+"\n************")

    return " " + "\n ".join(out)

def print_mission_order(p, date, sourceName, sourceStatus, sourceDpt, destName, subject, location, desc):
    p.set_with_default()

    print_center(p, "Debut de transmission")
    p.text("\n")
    p.image("logo.png", center=True)

    p.text("\n\n")
   
    def print_long_field(name, value, end=""):
        p.set_with_default(bold=False) ; p.text(" "+name+" :")
        p.set_with_default(bold=True) ; p.text(format_long(value, maxLen=41, firstLen=41-(len(name)+2)) + end)


    def print_short_field(name, value, end=""):
        p.set_with_default(bold=False) ; p.text(" " + name + ":" + (" " * (19-len(name))))
        p.set_with_default(bold=True) ; p.text(value + end)

    def print_double_field(name1, value1, name2, value2, end=""):
        p.set_with_default(bold=False) ; p.text(" " + name1 + ": ")
        p.set_with_default(bold=True) ; p.text(value1 + " " * (18-len(name1)-len(value1)))
        p.set_with_default(bold=False) ; p.text(name2 + ": ")
        p.set_with_default(bold=True) ; p.text(value2 + end)


    print_short_field("Filling date", date, end="\n\n")
    print_short_field("Full source ID", sourceName, end="\n")
    print_double_field("Status", sourceStatus, "Dpt", sourceDpt, end="\n\n")
    print_short_field("Full dest ID", destName, end="\n\n\n")

    print_long_field("Service Object", subject, end="\n")
    print_long_field("Location", location, end="\n\n\n")
    
    print_long_field("Description", desc, end="\n\n\n")
    
    p.set_with_default(bold=False)
    p.text(" [ ] Read   [ ] Kuisining   [ ] Done\n\n\n")

    # p.barcode("37862964", "EAN8", height=12, force_software=False, pos="OFF")

    print_pdf417(p, "oid.17649,s.PPORTE-E-0972D,d.STAR-L6904")
    p.set_with_default(bold=True)

    # p.text(custom_center("fin de transmission"))
    print_center(p, "Fin de transmission")

    p.cut()


class Test:
    def _text(self, buff):
        for i, c in enumerate(buff):
            if i != 0 and i % 42 == 0:
                print("")

            print(c, end="")

    def text(self, buff):
        print(buff, end="")

    def image(self, *args, **args2):
        print(" ### IMG ###")

    def set_with_default(self, *args, **args2):
        pass

    def set(self, *args, **args2):
        pass

    def cut(self, **args2):
        pass

# p = init_printer()

# p = Test()
# print_mission_order(p, date="09.01.2025", sourceName="STAR-L6904", sourceStatus="Sub", sourceDpt="Staff", destName="PPORTE-E-0972D", subject="Je t'aime <7 et meme que ca marche sur plusieurs lignes normalement", location="ton coeur sur plusieurs lignes aussi normalement ig???", desc="Je t\'aime vraiment beaucoup d'amour de love de sucre a la menthe et j'espere qu'on va avoir une longue et belle vie ensemble")
# print_mission_order(p, date="123456789012345678901", sourceName="123456789012345678901", sourceStatus="12345678901", sourceDpt="12345678901234567", destName="", subject="", location="", desc="")

# print_pdf417(p, "olaaaa")
