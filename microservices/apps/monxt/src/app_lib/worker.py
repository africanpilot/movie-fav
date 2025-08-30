# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import link  # noqa: F401

from monxt.src.controller.controller_worker import WorkerController, worker

WorkerController()

if __name__ == "__main__":
    worker.start()
