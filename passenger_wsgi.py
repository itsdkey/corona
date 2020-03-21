import os
import sys
sys.path.append(os.getcwd())
from manage import app  # noqa


if __name__ == '__main__':
    app.run_server()
