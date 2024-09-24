from .. import models
from ..utils.stats_utils import get_start_date
from fastapi import Depends, APIRouter
from ..database import get_db
from sqlalchemy import func
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/stats",
    tags=['Stats']
)


@router.get("/pack-items/count")
def get_pack_items_over_time_period(time_period: str, user_id=None, db: Session = Depends(get_db)):

    # get start date of time period
    start_date = get_start_date(time_period)

    query = db.query(
        func.count(func.distinct(models.Item.pack_id))).filter(models.Item.created_at >= start_date)
    
    if user_id:
        user_id = int(user_id)
        query = query.filter(models.Item.user_id == user_id)

    total_packs = query.scalar()

    return {"total_packs": total_packs}


@router.get("/player-picks/count")
def get_player_picks_over_time_period(time_period: str, user_id=None, db: Session = Depends(get_db)):

    # get start date of time period
    start_date = get_start_date(time_period)

    query = db.query(
        func.count(func.distinct(models.PlayerPick.pack_id))).filter(
        models.PlayerPick.created_at >= start_date).scalar()
    
    if user_id:
        user_id = int(user_id)
        query = query.filter(models.PlayerPick.user_id == user_id)

    total_picks = query.scalar()
    return {"total_picks": total_picks}


@router.get("/player-picks/type-count")
def get_count_of_player_pick_type_over_time_period(time_period: str, user_id=None, db: Session = Depends(get_db)):
    """
    This will return a data dictionary of the top ten most opended packs. 
    Key: Pack_name
    Value: Number of packs opened
    """
    
    # get start date of time period
    start_date = get_start_date(time_period)

    print(f"this is user_id: {user_id}")
    query = db.query(
        models.PlayerPick.pack_name,
        func.count(func.distinct(models.PlayerPick.pack_id)).label('count')
    ).filter(
        models.PlayerPick.created_at >= start_date
    ).group_by(
        models.PlayerPick.pack_name
    ).order_by(
        func.count(func.distinct(models.PlayerPick.pack_id)).desc()
    )

    if user_id:
        user_id = int(user_id)
        query = query.filter(models.PlayerPick.user_id == user_id)
    
    results = query.limit(10).all()


    top_picks = {pack_name: count for pack_name, count in results}

    return top_picks


@router.get("/player-picks/type-count")
def get_count_of_player_pick_type_over_time_period(time_period: str, user_id=None, db: Session = Depends(get_db)):
    """
    This will return a data dictionary of the top ten most opended packs. 
    Key: Pack_name
    Value: Number of packs opened
    """
    
    # get start date of time period
    start_date = get_start_date(time_period)

    print(f"this is user_id: {user_id}")
    query = db.query(
        models.Item.pack_name,
        func.count(func.distinct(models.Item.pack_id)).label('count')
    ).filter(
        models.Item.created_at >= start_date
    ).group_by(
        models.Item.pack_name
    ).order_by(
        func.count(func.distinct(models.Item.pack_id)).desc()
    )

    if user_id:
        user_id = int(user_id)
        query = query.filter(models.Item.user_id == user_id)
    
    results = query.limit(10).all()


    top_picks = {pack_name: count for pack_name, count in results}

    return top_picks