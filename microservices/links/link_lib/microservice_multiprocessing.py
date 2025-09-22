# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.


# future must be the first instruction in the file!
from __future__ import print_function

import os
import sys
import time
from select import select
from subprocess import PIPE, Popen

from link_lib.microservice_generic_model import microservice_name
from link_lib.microservice_logger import MicroserviceLogger
from link_lib.microservice_signals import MicroservciceSignalHandler


class MicroserviceMultiprocessing:
    is_multiprocess_controller = True

    microservice_path = ""
    processes = []
    pid_to_role_map = {}
    old_pid_to_role_map = {}
    shutdown_mode = False

    def launch_one(self, role):
        route = "app.py" if role == "api" else "unary_server.py"
        args = ["python", self.microservice_path + f"/{route}"]
        proc = Popen(args, stdout=PIPE, bufsize=1, close_fds=True, universal_newlines=True)
        pid = proc.pid
        self.pid_to_role_map[pid] = role
        self.processes.append(proc)
        self.log.debug(f"Launching PID {pid} for process {role}")

    def launch_all(self):
        self.log.info("Launching all processes.")
        for role in {"api", "grpc"}:
            self.log.info(f"Launching {role}...")
            self.launch_one(role)
            if "api" == role:
                self.log.debug("Delaying start of non-api procs...")
                time.sleep(5)

            if "grpc" == role:
                self.log.debug("Delaying start of non-grpc procs...")
                time.sleep(5)

    def launch_all_with_nanny(self):
        self.launch_all()
        self.nanny()

    def __init__(self, path):
        self.microservice_path = path

        self.microservice_name = microservice_name()
        id = f"{self.microservice_name} controller"
        self.log = MicroserviceLogger.instance(id)
        self.signal_handler = MicroservciceSignalHandler(self)

        required_base = {
            f"/home/svc/microservices/apps/{self.microservice_name}/src/app_lib",
        }
        requested_base = self.microservice_path
        if requested_base not in required_base:
            print(f"Can only start in the app_lib {required_base}")
            self.log.debug(f"Can only start in the app_lib {required_base}")
            sys.exit(1)

        pid = os.getpid()
        self.log.debug(f"PID {pid}")
        self.launch_all_with_nanny()

    def message_from_child(self, message):
        print(message, end="")
        sys.stdout.flush()

    def health_check(self):
        pass

    def kill(self, proc, signal_number=0):
        pid = proc.pid
        self.log.debug(f"Killing PID {pid} with signal {signal_number}")
        self.processes.remove(proc)
        proc.stdout.close()

        if signal_number:
            os.kill(proc.pid, signal_number)

        self.old_pid_to_role_map[pid] = self.pid_to_role_map[pid]
        del self.pid_to_role_map[pid]

    def kill_all(self, signal_number=0):
        for p in self.processes[:]:
            self.kill(p, signal_number)

    def shutdown(self, mode, signal_number=0):
        self.shutdown_mode = True
        self.log.critical("Passing shutdown signal to children - in case they didn't receive it already")
        self.kill_all(signal_number)

    def restart(self, pid):
        if self.shutdown_mode:
            return True

        role = self.old_pid_to_role_map[pid]
        del self.old_pid_to_role_map[pid]

        self.log.critical(f"Process {role} PID {pid} died. Will restart...")

        # if 'api' == role:
        #     self.log.critical("Api died so I'm killing all dependent processes. Will restart after.")
        #     self.kill_all(signal.SIGTERM)

        #     n = 20
        #     self.log.debug(f"Sleeping for {n} seconds.")
        #     time.sleep(n)

        #     self.launch_all()
        #     return True

        self.launch_one(role)
        return False

    def nanny(self):
        health_check_interval = 100
        timeout = 0.01
        i = 0

        while self.processes:
            for p in self.processes[:]:
                todo = []
                exit_code = p.poll()
                if exit_code is not None:
                    self.message_from_child(p.stdout.read())
                    self.kill(p)
                    if exit_code != 0:
                        if self.restart(p.pid):
                            break
                else:
                    todo.append(p.stdout)

            ready = select(todo, [], [], timeout)[0]
            for fp in ready:
                self.message_from_child(fp.readline())

            if not (i % health_check_interval):
                self.health_check()
                i = 0
            i = i + 1
