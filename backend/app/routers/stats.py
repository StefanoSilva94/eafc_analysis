from .. import models, schemas, utils
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter
from ..database import get_db
from datetime import datetime, timedelta, timezone
from sqlalchemy import func




router = APIRouter(
    prefix="/stats",
    tags=['Stats']
)


@router.get("/pack-items")
def get_pack_items_over_time_period(time_period: str, db: Session = Depends(get_db)):

    now = datetime.now(timezone.utc)
    if time_period == "1d":
        start_date = now - timedelta(days=1)
    elif time_period == "7d":
        start_date = now - timedelta(days=7)
    elif time_period == "30d":
        start_date = now - timedelta(days=30)
    elif time_period == "1y":
        start_date = now - timedelta(days=365)
    else:
        raise HTTPException(status_code=400, detail="Invalid time period")

    total_packs = db.query(
        func.count(func.distinct(models.PlayerPick.pack_id))).filter(models.Pack.created_at >= start_date).scalar()

    return {"total_packs": total_packs}


@router.get("/player-picks")
def get_player_picks_over_time_period(time_period: str, db: Session = Depends(get_db)):
    now = datetime.now(timezone.utc)
    if time_period == "1d":
        start_date = now - timedelta(days=1)
    elif time_period == "7d":
        start_date = now - timedelta(days=7)
    elif time_period == "30d":
        start_date = now - timedelta(days=30)
    elif time_period == "1y":
        start_date = now - timedelta(days=365)
    else:
        raise HTTPException(status_code=400, detail="Invalid time period")

    total_picks = db.query(
        func.count(func.distinct(models.PlayerPick.pack_id))).filter(models.PlayerPick.created_at >= start_date).scalar()
    return {"total_picks": total_picks}