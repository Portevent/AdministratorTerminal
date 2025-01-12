import form
from forms.form import Form


class MissionForm(form.Form):
    def serialise(self) -> str:
        pass

    @staticmethod
    def deserialise(serialised: str) -> Form:
        pass