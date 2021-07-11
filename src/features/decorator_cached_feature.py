from functools import wraps
# import os.path
# from src.features.read_feature_dictionary import read_feature_dictionary as rdict
# from src.features.read_feature_dataframe import read_feature_dataframe as rdf
# import logging
# import inspect
# from src.data import data


def cached_feature(func):

    @wraps(func)
    def func_wrapper(*args, **kwargs):
        """To be applied to the features we compute once and cache in develop mode.
           Read the cached value from the saved file, if in develop mode.

           It makes a number of assumptions, which are compatible with what array_feature assumes:

           - The feature function has just one return value
           - The first parameter is loaded from a df which have:
                - as first column the index of the new feature we are going to create
                - as second column the values in which the first parameter ranges

           This method works also in demo mode: if it cannot find the value on the second column of
           the dataframe, then it means that the actual value of the feature was not computed,
           i.e. we are in demo mode.

           Ideally, we could think of saving the values which were not known, so that we can increase
           our database of known values and avoid to recompute them if happen again

        Returns:
            ? -- feature value
        """
        # if not 'recreate' in kwargs:
        #     if os.path.exists(f"{data.feature_path}/{func.__name__}.npy"):
        #         params = list(inspect.signature(func).parameters.keys())
        #         df_index = rdf(params[0])
        #         if params[0] in kwargs:
        #             param_value = kwargs[params[0]]
        #         else:
        #             param_value = args[0]
        #         row = df_index[df_index.iloc[:, 1] == param_value]
        #         if len(row) > 0:
        #             # Develop mode
        #             if len(row) > 1:
        #                 logging.getLogger('root.features').warning(
        #                     f"Incoherence, with a value of the first arg I should be able to slice just one row of the index dataframe. \
        #                                     This means that there are more than one {params[0]} with the index value {param_value}")
        #                 row = row.head(1)

        #             id = row.iloc[0, 0]
        #             assert id in rdict(
        #                 func.__name__), f"Incoherence, this id should be into the dictionary by design"
        #             return_value = rdict(func.__name__)[id]

        #             logging.getLogger('root.features').warning(
        #                 f"Reading cached value of {func.__name__} with the index value {param_value[0:50] if type(param_value) == str else param_value}: {return_value[0:50] if type(return_value) == str else return_value}")

        #             return return_value
        # else:
        #     assert kwargs['recreate'] == True, "The recreate value should be used only in case we want to recreate the feature"

        # Either we want to recreate the feature or we were not able to retrieve the cached value
        kwargs.pop('recreate', None)
        r = func(*args, **kwargs)
        return r

    return func_wrapper
