"""remote_controlled_soccer_player controller."""

from controller import Robot
from server import run_aplication_server
import socket
import sys
import threading
# Create a TCP/IP socket

functions = {
    "echo" : (lambda s: s),
}

robot = Robot()

com_thread = threading.Thread(target=run_aplication_server, args = (functions,))
com_thread.start()

"""
while robot.step(timestep) != -1:
    pass
"""
