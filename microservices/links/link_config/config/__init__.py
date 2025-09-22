import importlib
import os

# Determine the environment we want to load, default is development.py
APP_DEFAULT_ENV = os.environ.get("APP_DEFAULT_ENV", "dev")

module = importlib.import_module("." + APP_DEFAULT_ENV, package="link_config.config")

# update globals of this module (i.e. settings) with imported.
globals().update(vars(module))
