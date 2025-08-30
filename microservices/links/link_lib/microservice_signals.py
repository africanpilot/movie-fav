# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import signal
import os
import sys

class MicroserviceSignalHandlerUtil:
    data = {}

    @staticmethod
    def set_var(key, val):
        MicroserviceSignalHandlerUtil.data[key] = val

    @staticmethod
    def get(key):
        p = MicroserviceSignalHandlerUtil.data
        if key in p:
            return p[key]
        return None

    @staticmethod
    def get_links():
        return MicroserviceSignalHandlerUtil.get('links')

    @staticmethod
    def log_message(links, signal_number, msg):
        if links:
            named = signal.Signals(signal_number).name
            links.log.critical(f"Received signal {named} ({signal_number}) {msg}")
    
#
# Note: can't use decorators with signal handlers
#
def shutdown_links(mode, signal_number):
    links = MicroserviceSignalHandlerUtil.get('links')
    if links:
        if hasattr(links, 'is_multiprocess_controller'):
            links.shutdown(mode, signal_number)
        else:
            links.shutdown(mode)

def signal_handler_graceful_shutdown(signal_number, frame):
    p = MicroserviceSignalHandlerUtil
    p.log_message(p.get_links(), signal_number, 'Graceful Shutdown')
    shutdown_links('graceful', signal_number)
    sys.exit(0)
        
def signal_handler_immediate_shutdown(signal_number, frame):
    p = MicroserviceSignalHandlerUtil
    p.log_message(p.get_links(), signal_number, 'Immediate Shutdown')
    shutdown_links('immediate', signal_number)
    sys.exit(0)

def signal_handler_reload_config(signal_number, frame):
    p = MicroserviceSignalHandlerUtil
    p.log_message(p.get_links(), signal_number, 'SIGHUP Ignoring')

def signal_handler_broken_pipe(signal_number, frame):
    p = MicroserviceSignalHandlerUtil
    links = p.get_links()
    if links:
        p.log_message(links, signal_number, 'SIGPIPE')
        if hasattr(links, 'is_multiprocess_controller'):
            return
    sys.exit(0)
        
class MicroservciceSignalHandler:
    def __init__(self, links):
        if not MicroserviceSignalHandlerUtil.data:
            MicroserviceSignalHandlerUtil.set_var('links', links)
            todo = {
                'healthy process needs to die' : {
                    'signal_handler' : signal_handler_graceful_shutdown,
                    'signals' : [
                        signal.SIGTERM,
                        signal.SIGQUIT,
                        signal.SIGINT,
                    ]
                },
                'sick process needs to die' : {
                    'signal_handler': signal_handler_immediate_shutdown,
                    'signals': [
                        signal.SIGILL,
                        signal.SIGXFSZ,
                        signal.SIGXCPU,
                        signal.SIGBUS,
                        signal.SIGSEGV,
                        signal.SIGSYS,
                   ]
                },
                'broken_pipe' : {
                    'signal_handler' : signal_handler_broken_pipe,
                    'signals' : [
                        signal.SIGFPE,
                    ]
                },
                'reload config' : {
                    'signal_handler' : signal_handler_reload_config,
                    'signals' : [
                        signal.SIGHUP,
                    ]
                }
            }
            for signal_group_description in todo.keys():
                record = todo[signal_group_description]
                for sig in record['signals']:
                    signal.signal(sig, record['signal_handler'])
