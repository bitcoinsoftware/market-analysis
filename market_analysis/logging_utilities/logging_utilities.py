import json
import logging.config
import os


def setup_logging(defaultPath="resources/logging/logging.json", relativeRootPath="./", defaultLevel=logging.INFO,
                  envKey="LOG_CFG"):
    path = relativeRootPath + defaultPath
    value = os.getenv(envKey, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=defaultLevel)
