import os
import sys
from bookfinder.server.server_launcher import server_launcher

'''Application entry point, configure and launch the Book Finder Server'''

sys.path.append(os.path.join(os.path.dirname(__file__)))

if __name__ == '__main__':
    server_launcher(True)
