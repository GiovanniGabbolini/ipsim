import datetime
import time
from functools import wraps
import logging


def timing_feature(func):

    @wraps(func)
    def func_wrapper(*args, **kwargs):
        start = time.time()
        r = func(*args, **kwargs)
        time_elampsed = str(datetime.timedelta(seconds=time.time()-start))

        logging.getLogger("root.features.timing").info(
            f"Feature {func.__name__} took {time_elampsed}s.")

        return r

    return func_wrapper
