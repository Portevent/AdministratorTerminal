from printer.driver import ThermalPrinter
from printer.templates.format import DefaultFormat
from printer.templates.template import Template

from forms.mission_form import MissionForm



class MissionTemplate[T: MissionForm](Template[T]):
    document: T

    def _print(self, printer: ThermalPrinter) -> None:
        """
        Prints the Mission
        """
        printer.set_with_default()

        DefaultFormat.print_center(printer, "Debut de transmission")
        printer.text("\n")
        printer.image("logo.png", center=True)

        printer.text("\n\n")

        DefaultFormat.print_short_field(printer, "Filling date", "xx.xx.xxxx", end="\n")
        DefaultFormat.print_short_field(printer, "Priority", self.document.getPriorityFromIndex(self.document.priority), end="\n\n")

        DefaultFormat.print_short_field(printer, "Full source ID", "undefined", end="\n")
        DefaultFormat.print_double_field(printer, "Status", "undef", "Dpt", "undef", end="\n\n")
        DefaultFormat.print_short_field(printer, "Full dest ID", self.document.assigned_id, end="\n\n\n")

        DefaultFormat.print_long_field(printer, "Service Object", self.document.name, end="\n")
        DefaultFormat.print_long_field(printer, "Location", self.document.location, end="\n\n\n")

        DefaultFormat.print_long_field(printer, "Description", self.document.description, end="\n\n\n")

        printer.set_with_default(bold=False)
        printer.text(" [ ] Read   [ ] In progress   [ ] Done\n\n\n")


        printer.text("need to change barcode code xxxxxxxx\n")
        DefaultFormat.print_pdf417(printer, "oid.17649,s.PPORTE-E-0972D,d.STAR-L6904")
        printer.set_with_default(bold=True)

        # printer.text(custom_center("fin de transmission"))
        DefaultFormat.print_center(printer, "Fin de transmission")

        printer.cut()