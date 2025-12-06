from fastapi import APIRouter, Depends, HTTPException
from schemas.schemas import SyncGroupRequest
from db.database import database
from moodle.client import get_moodle_client
from services.sync_service import SyncService

router = APIRouter(prefix="/api")

@router.post("/sync/group")
async def sync_group(payload: SyncGroupRequest):
    db = database
    moodle = get_moodle_client()
    service = SyncService(db, moodle)
    result = await service.sync_group(payload.grupo_id, create_if_missing=payload.createIfMissing, concurrency_limit=payload.concurrencyLimit)
    return result
