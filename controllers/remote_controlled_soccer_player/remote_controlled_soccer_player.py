"""remote_controlled_soccer_player controller."""

from controller import *
from server import run_aplication_server
import signal
import socket
import sys
import threading
import re
# Create a TCP/IP socket

class v4s_robot:
    def __init__(self, robot):
        # Pega informações do robô
        self.robot = robot
        self.name = robot.getName()
        # O nome precisa ter o formato ['B' || 'Y'](int), identificando ID e time do robô
        self.team = self.name[0]
        self.id = int(re.search(r'\d+', self.name).group())
        
        # Inicializa os motores do robô
        self.motor = {
            "direito" : robot.getMotor("right wheel motor"),
            "esquerdo" : robot.getMotor("left wheel motor"),
        }
        self.motor["direito"].setPosition(float('+inf'))
        self.motor["direito"].setVelocity(0.0)
        self.motor["esquerdo"].setPosition(float('+inf'))
        self.motor["esquerdo"].setVelocity(0.0)
    
    """ 
        Função que calcula a porta do robô a partir de seu nome
    """
    def get_port(self):
        port = 0
        if self.team is 'B':
            port = 40000
        elif self.team is 'Y':
            port = 30000
        else:
            raise Exception("Not valid team")
        return port + int(self.id)


"""
    Inicialização do robô e suas partes
"""
player = v4s_robot(Robot())
timestep = int(player.robot.getBasicTimeStep())

print("Inicializando jogador", player.name, "Do time", player.team, "e ID", player.id)


"""
    funções que serão fornecidas via tcp/ip
"""
functions = {
    "echo" : (lambda s: s),
}

com_thread = threading.Thread(target=run_aplication_server, args = (functions,'localhost', player.get_port(),))
com_thread.start()

# Teste: girar durante 5 segundos, depois girar ao lado contrário
dir = 10
esq = -10

def change_dir(signum, frame):
    global dir, esq
    esq = -esq
    dir = -dir
    signal.alarm(5)

signal.signal(signal.SIGALRM, change_dir)
signal.alarm(5)

while player.robot.step(timestep) != -1:
    player.motor["direito"].setVelocity(dir)
    player.motor["esquerdo"].setVelocity(esq)

