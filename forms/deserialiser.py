from forms.errors import WrongFormVersionError, WrongFormError
from forms.form import Form
from forms.mission_form import MissionForm
from forms.report_form import IncidentReportForm


def deserialiseFromEncoded(buff: str) -> Form:
    res, fid, fver, _ = Form.tryGetSignature(buff)

    if not res:
        raise Exception

    match fid:
        case IncidentReportForm.form_id:
            match fver:
                case IncidentReportForm.form_ver:
                    return IncidentReportForm
                case _:
                    raise WrongFormVersionError
        case MissionForm.form_id:
            match fver:
                case MissionForm.form_ver:
                    return MissionForm
                case _:
                    raise WrongFormVersionError

        case _:
            raise WrongFormError