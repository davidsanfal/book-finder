import os
from bookfinder.errors import EnvironmentException


def get_environment_variable(name, default=None):
    var = os.environ.get(name, default)
    if var is None:
        raise EnvironmentException('Define the API Key: %s' % name)
    return var

ISBNDB_API_KEY = get_environment_variable('ISBNDB_API_KEY')
LIBRARYTHING_API_KEY = get_environment_variable('LIBRARYTHING_API_KEY')
