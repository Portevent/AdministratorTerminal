from printer.driver import ThermalPrinter
from printer.templates.format import DefaultFormat
from printer.templates.template import Template

from forms.report_form import IncidentReportForm



class IncidentReportTemplate[T: IncidentReportForm](Template[T]):
    document: T

    def _print(self, printer: ThermalPrinter, oid: int | None = None) -> None:
        """
        Prints the Mission
        """
        printer.set_with_default()

        DefaultFormat.print_center(printer, "Debut de transmission")
        printer.text("\n")
        printer.image("logo.png", center=True)

        printer.text("\n\n")

        DefaultFormat.print_short_field(printer, "Filling date", self.document.fillingDate, end="\n")
        DefaultFormat.print_short_field(printer, "Priority", self.document.getPriorityFromIndex(self.document.priority), end="\n\n")

        DefaultFormat.print_short_field(printer, "Full source ID", self.document.sourceID, end="\n")
        DefaultFormat.print_double_field(printer, "Status", self.document.sourceStatus, "Dpt", self.document.sourceDept, end="\n\n")
        DefaultFormat.print_short_field(printer, "Full dest ID", self.document.destID, end="\n\n\n")

        DefaultFormat.print_long_field(printer, "Issue Object", self.document.issueTitle, end="\n")
        DefaultFormat.print_long_field(printer, "Location", self.document.location, end="\n\n\n")

        DefaultFormat.print_long_field(printer, "Issue Description", self.document.issue, end="\n\n\n")

        if self.document.proposal is not None:
            DefaultFormat.print_long_field(printer, "Proposal", self.document.proposal, end="\n\n\n")

        if oid is None:
            printer.text("OrderID propagation failed, barcode incomplete\n")

        DefaultFormat.print_pdf417(printer, f"oid.{str(oid)},s.{self.document.source.getID()},d.{self.document.dest.getID()}")
        printer.set_with_default(bold=True)

        # printer.text(custom_center("fin de transmission"))
        DefaultFormat.print_center(printer, "Fin de transmission")

        printer.cut()