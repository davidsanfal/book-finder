import os
import sys
from bookfinder.errors import EnvironmentException

sys.path.append(os.path.join(os.path.dirname(__file__)))


if __name__ == '__main__':
    try:
        from bookfinder.server.finder_server import app
        app.run(debug=True)
    except EnvironmentException as e:
        print e.message
