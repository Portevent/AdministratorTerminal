from forms.form import Form
from printer.templates.mission import MissionTemplate
from printer.templates.template import Template

from forms.mission_form import MissionForm

class Filter:
    @staticmethod
    def templateFromDocument(document: Form) -> Template:
        match type(document):
            case MissionForm.__class__:
                return MissionTemplate(document)
            case _:
                raise NotImplementedError
