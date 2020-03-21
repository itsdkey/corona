import os
import sys
sys.path.append(os.getcwd())
from app.application import get_app  # noqa

application = get_app().server
