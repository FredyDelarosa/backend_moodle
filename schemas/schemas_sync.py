from pydantic import BaseModel
from typing import Optional

class SyncGroupRequest(BaseModel):
    grupo_id: int
    createIfMissing: Optional[bool] = True
    concurrencyLimit: Optional[int] = None
