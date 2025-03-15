from pydantic import BaseModel
from typing import Union

class noukriResumeUpdateRequest(BaseModel):

    login_email: str=None
    login_password: str=None