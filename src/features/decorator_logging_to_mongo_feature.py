import datetime
from src.log.log_mongo import log_mongo
import time
from functools import wraps
import logging


def logging_to_mongo_feature(func):

    @wraps(func)
    def func_wrapper(*args, **kwargs):
        start = time.time()
        r = func(*args, **kwargs)
        time_elampsed = str(datetime.timedelta(seconds=time.time()-start))

        if r is None:
            outcome = False
        else:
            outcome = True

        to_save = {
            "args": args,
            "kwargs": kwargs,
            "result": r,
            "outcome": outcome,
            "time_elampsed": time_elampsed,
            "timestamp": datetime.datetime.now()
        }

        logging.getLogger("root.features.timing").info(
            f"Feature {func.__name__} took {time_elampsed}s.")
        log_mongo(func.__name__, to_save, db_name="log_feature")

        return r

    return func_wrapper
