from forms.form import Form
from printer.templates.mission_template import MissionTemplate
from printer.templates.template import Template

from forms.mission_form import MissionForm

class Filter:
    @staticmethod
    def templateFromDocument(document: Form) -> Template:
        match document:
            case MissionForm():
                return MissionTemplate(document)
            case _:
                raise NotImplementedError
