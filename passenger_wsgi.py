import os
import sys

from app.application import get_app  # noqa

sys.path.append(os.getcwd())

application = get_app().server
