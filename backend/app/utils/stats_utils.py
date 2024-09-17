from datetime import datetime, timedelta, timezone
import logging


logger = logging.getLogger(__name__)


def get_start_date(time_period_in_days: str='7'):
    """
    Given a time period it will return the timestamp of now - time_period
    It will spli
    """
    now = datetime.now(timezone.utc)

    try:
        # cast time period to an int
        time_period = int(time_period_in_days)
        start_date = now - timedelta(days=time_period)

    except ValueError:
        # if an incorrect value is input default to 7 day time period

        logger.warning(f'An incorrect time period was input: {time_period_in_days}. time_period will be defaulted to 7')
        return now - timedelta(days=7) 
    
    return start_date
