"""simulation_controller controller."""

from controller import Robot, Camera, Node, Supervisor, Field
from server import run_aplication_server
import threading

"""
    Classe Score (mantem placar e o escreve na tela)
"""
class Score():
    def __init__(self, supervisor, team_b = 'Blue', team_y = 'Yellow'):
        self.team_b = team_b
        self.team_y = team_y
        self.score = {
            self.team_b : 0,
            self.team_y : 0
        }
        self.supervisor = supervisor
     
    def print_score(self):
        self.supervisor.setLabel(0, str(self.score[self.team_b]) + " " + self.team_b, 0.80, 0.01, 0.1, 0x0000ff, 0.0, "Arial")
        
        self.supervisor.setLabel(1, self.team_y + " " + str(self.score[self.team_y]), 0.1, 0.01, 0.1, 0xffff00, 0.0, "Arial")
        
    def goal(self, team):
        self.score[team] += 1
        self.print_score()
    
    def set_score(self, score_team_b, score_team_y):
        self.score[self.team_b] = score_team_b
        self.score[self.team_y] = score_team_y
        self.print_score()

"""
    Classe de objetos da simulação : Bola e robôs
"""
class sim_object():
    def __init__(self, obj_node):
        self.obj_node = obj_node
        self.initial_translation = self.get_translation()
        self.initial_rotation = self.get_rotation()
    
    def get_translation(self):
        obj_translation_field = self.obj_node.getField("translation")
        return obj_translation_field.getSFVec3f()
    
    def get_rotation(self):
        obj_rotation_field = self.obj_node.getField("rotation")
        return obj_rotation_field.getSFRotation()
    
    def reset_translation(self):
        self.obj_node.resetPhysics()
        self.obj_node.getField("translation").setSFVec3f(self.initial_translation)
      
    def reset_rotation(self):
        self.obj_node.getField("rotation").setSFRotation(self.initial_rotation)    
    
     

"""
    Inicialização do robô e suas partes
"""
supervisor = Supervisor()
camera = Camera("camera")
timestep = int(supervisor.getBasicTimeStep())
camera.enable(timestep)

team_b = 'Blue'
team_y = 'Yellow'

objetos = {
    team_b : [
        sim_object(supervisor.getFromDef("B1")),
        sim_object(supervisor.getFromDef("B2")),
        sim_object(supervisor.getFromDef("B3")),        
    ],
    team_y : [],
    "ball" : sim_object(supervisor.getFromDef("BALL")),
}

goal_limits = 0.745


"""
    Cria objeto score
"""
score = Score(supervisor, team_b = team_b, team_y = team_y)
score.print_score()

"""
    controle de jogo
"""
time = 10*60 # partida de 10 minutos
ball_reset_timer = 3
andamento_partida = True


"""
    Funções que serão ofertadas via TCP/IP JSON-RPC
"""
def stop_sim():
    global andamento_partida
    andamento_partida = False

def start_sim():
    global andamento_partida
    andamento_partida = True

def reset_sim():
    global time, supervisor, score, objetos
    time = 10*60
    time_string = str(int(time / 60)).zfill(2) + ":" + str(int(time % 60)).zfill(2)
    supervisor.setLabel(2, time_string, 0.45, 0.01, 0.1, 0x000000, 0.0, "Arial")
    score.set_score(0,0)
    reset_objects()
    stop_sim()
        
def reset_objects():
    global objetos, supervisor
    objetos["ball"].reset_translation()
    for player in objetos[team_b]:
        player.reset_translation()
        player.reset_rotation()

def get_state():
    global objetos, score
    ball_translation = objetos["ball"].get_translation()
    ball_velocity = objetos["ball"].obj_node.getVelocity()
    
    mensagem = { "score" : [ score.score[team_y], score.score[team_b]] } 
    
    mensagem["ball"] = { "position" : [ball_translation[0], ball_translation[2] ],
                         "rotation" : objetos["ball"].get_rotation() ,
                         "speed" : [ball_velocity[0], ball_velocity[2], ball_velocity[3] , ball_velocity[5] ], 
                       }
    
    teams = [team_b, team_y]
    for team in teams:
        mensagem[team] = [ ]
        for player in objetos[team]:
            position = player.get_translation()
            player_info = { "position" : [ position[0], position[2] ], } 
            player_info["rotation"] = player.get_rotation()
            velocity = player.obj_node.getVelocity()
            player_info["speed"] = [ velocity[0], velocity[2], velocity[3], velocity[5] ]
            mensagem[team].append(player_info)
        
    return mensagem
    
functions = {
    "echo" : (lambda s: s),
    "reset_sim" : reset_sim,
    "stop_sim" : stop_sim,
    "start_sim" : start_sim,
    "reset_objects" : reset_objects,
    "get_state" : get_state,
}   

com_thread = threading.Thread(target=run_aplication_server, args = (functions,))
com_thread.start()

while supervisor.step(timestep) != -1:
    imagem = camera.getImage()
    if (andamento_partida):
        """ 
            Avança o tempo de partida
        """
        time -= timestep / 1000.0;
        if time < 0:
          time = 10 * 60
          andamento_partida = False
          continue
        time_string = str(int(time / 60)).zfill(2) + ":" + str(int(time % 60)).zfill(2)
        supervisor.setLabel(2, time_string, 0.45, 0.01, 0.1, 0x000000, 0.0, "Arial")
                
        """
            checa se há gol
        """
        ball_translation = objetos["ball"].get_translation()
        if ball_reset_timer == 0:
            if ball_translation[0] > goal_limits:
                score.goal(team_y)
                ball_reset_timer = 3
            elif ball_translation[0] < -goal_limits:
                score.goal(team_b)
                ball_reset_timer = 3
        else:
            ball_reset_timer -= timestep / 1000.0
            if ball_reset_timer <= 0:
                ball_reset_timer = 0
                reset_objects()
            
            

# Enter here exit cleanup code.
