"""
Created on Fri Mar 13 2020

@author Giovanni Gabbolini
"""


from src.features.read_feature_dataframe import read_feature_dataframe as rdf
import pandas as pd
from src.features.create_feature import create_feature
import inspect
from src.log.log_mongo import log_mongo
import time
import datetime
import concurrent.futures
from itertools import repeat
from tqdm import tqdm


def get_feature_signature_details(feature):
    feature_args_names = tuple(inspect.signature(feature).parameters.keys())
    feature_name = feature.__name__
    return feature_args_names, feature_name


def array_feature(feature, argument_values=None, mp=True, skip_until=0):
    """Given a feature function, it manage to save the feature for every entity

       In practice, automatize the creation of a method, for every feature file,
       which was needed to create the feature for the offline development

       It makes a number of assumption:

       - Feature arguments should be called in the same way as other features,
         and therefore, we expect that the arguments are just other features
       - The first arguments is the feature which will have the same index of
         our newly created one
       - The feature has just one return value

       Lastly, it assumes that all the features which have the same name of the argument values
       have the same length. If this is not the case, exploit the variable argument_values to
       provide personalized value argument_values and overcoming this requirement

      It saves the features with the same name of the method

    Arguments:
        argument_values {list} -- list of iterables to be passed to the function
        feature {func} -- feature
        mp {bool} -- whether to go multiprocessing or not
    """

    feature_args_names, feature_name = get_feature_signature_details(feature)

    dfs = [rdf(s) for s in feature_args_names]

    idx_values = dfs[0].iloc[:, 0].values
    idx_name = dfs[0].columns[0]
    ret = [None]*len(idx_values)

    if not argument_values:
        argument_values = [df.iloc[:, 1].values for df in dfs]

    # Provide the recreate keyword
    feature_args_names += 'recreate',
    argument_values.append([True]*len(idx_values))

    assert all(len(idx_values) == len(arg)
               for arg in argument_values), "Length mismatch, arrays should be of the same length"

    start = time.time()

    if mp:
        with concurrent.futures.ThreadPoolExecutor() as ex:
            ret = list(tqdm(ex.map(lambda a, b: feature(**dict(zip(b, a))),
                                   zip(*argument_values), repeat(feature_args_names))))
        count_found = sum(u is not None for u in ret)

    else:
        count_found = 0
        for i, t in enumerate(zip(*argument_values)):
            if i >= skip_until:
                argument = dict(zip(feature_args_names, t))
                r = feature(**argument)
                count_found += 1 if r is not None else 0
                ret[i] = r

                print(f"Processing element {i}, {t} ... Found {ret[i]}")

    time_elampsed = datetime.timedelta(seconds=time.time()-start)

    print('Found {} non-null value for the feature'.format(count_found))
    print('So a percentage of {} non-null values'.format(count_found/len(idx_values)))

    create_feature({idx_name: idx_values, feature_name: ret})

    d = {
        "tot_trials": len(idx_values),
        "count_found": count_found,
        "percentage_found": count_found/len(idx_values),
        "time_elampsed_total": str(time_elampsed),
        "time_elampsed_each": str(time_elampsed/len(idx_values)),
        "timestamp": datetime.datetime.now()
    }

    log_mongo(feature_name, d, db_name="log_feature_array")
