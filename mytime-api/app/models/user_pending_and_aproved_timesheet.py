from pydantic import BaseModel


class UserPendingAndAprovedTimesheet(BaseModel):
    ApprovedHrs: int
    PendingHrs: int
