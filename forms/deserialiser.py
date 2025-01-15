import base64
from typing import Type

from forms.errors import WrongFormVersionError, WrongFormError
from forms.form import Form
from forms.mission_form import MissionForm
from forms.report_form import IncidentReportForm
from mission import format_long


def deserialiseFromEncoded(buff: str) -> Form:
    decoded_buff = base64.b64decode(buff)

    res, form_id, form_ver, _ = Form.tryGetSignature(buffer=decoded_buff)

    if not res:
        raise Exception

    match form_id:
        case IncidentReportForm.form_id:
            match form_ver:
                case IncidentReportForm.form_ver:
                    return IncidentReportForm.deserialiseFromBytes(decoded_buff)
                case _:
                    raise WrongFormVersionError
        case MissionForm.form_id:
            match form_ver:
                case MissionForm.form_ver:
                    return MissionForm.deserialiseFromBytes(decoded_buff)
                case _:
                    raise WrongFormVersionError

        case _:
            raise WrongFormError