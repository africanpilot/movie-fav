import importlib
import os

# Determine the environment we want to load, default is dev.py
# update globals of this module (i.e. settings) with imported.

APP_DEFAULT_ENV = os.getenv("APP_DEFAULT_ENV", "dev")

if importlib.util.find_spec("." + APP_DEFAULT_ENV, package="link_config.config"):
    link_module = importlib.import_module("." + APP_DEFAULT_ENV, package="link_config.config")
    globals().update(vars(link_module))

# IMPORTANT: service_module must get added last so that it can overwrite vars if a microservice has specific needs
if importlib.util.find_spec("." + APP_DEFAULT_ENV, package="shows.src.app_lib.config"):
    service_module = importlib.import_module("." + APP_DEFAULT_ENV, package="shows.src.app_lib.config")
    globals().update(vars(service_module))
