from forms.form import Form
from forms.report_form import IncidentReportForm
from printer.templates.mission_template import MissionTemplate
from printer.templates.report_template import IncidentReportTemplate
from printer.templates.template import Template

from forms.mission_form import MissionForm

class Filter:
    @staticmethod
    def templateFromDocument(document: Form) -> Template:
        match document:
            case MissionForm():
                return MissionTemplate(document)
            case IncidentReportForm():
                return IncidentReportTemplate(document)
            case _:
                raise NotImplementedError
