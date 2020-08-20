"""simulation_controller controller."""

from controller import Robot, Camera, Node, Supervisor, Field

"""
    Inicialização do robô e suas partes
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

class sim_object():
    def __init__(self, obj_node):
        self.obj_node = obj_node
    
    def getTranslation(self):
        obj_translation_field = self.obj_node.getField("translation")
        return obj_translation_field.getSFVec3f()
    
    def getRotation(self):
        obj_rotation_field = self.obj_node.getField("rotation")
        return obj_rotation_field.getSFRotation()
    
     
    


robot = Supervisor()
camera = Camera("camera")
timestep = int(robot.getBasicTimeStep())
camera.enable(timestep)
score = Score(robot)
score.print_score()

while robot.step(timestep) != -1:
    imagem = camera.getImage()

# Enter here exit cleanup code.
