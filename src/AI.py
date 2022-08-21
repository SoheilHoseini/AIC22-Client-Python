from operator import xor
from src.client import GameClient
from src.model import GameView,AgentType
import random
from  src.GraphController import GraphController

def get_thief_starting_node(view: GameView) -> int:
    node_count = len(view.config.graph.nodes)
    return random.randint(0,node_count)


class Phone:
    def __init__(self, client: GameClient):
        self.client = client

    def send_message(self, message):
        self.client.send_message(message)


class AI:
    
    def __init__(self, view: GameView, phone: Phone):
        self.graph_controller = GraphController(view.config.graph)
        self.phone = phone

    def thief_move_ai(self, view: GameView) -> int:
        # write your code here
        me = view.viewer
        adjacentPath = self.graph_controller.get_adjacent_path(me.id)
        police = []
        for agent in view.visible_agents:
            if( agent.team != me.team and agent.agent_type == AgentType.POLICE):
                police.append(agent.id)
        
        next = me.id

        for path in adjacentPath:
            adj = me.id ^ path.first_node_id ^ path.second_node_id
            if (self.graph_controller.get_score(next, police) <= self.graph_controller.get_score(adj, police)):
                next = adj

        # message = ''
        # for m in range(len(view.visible_agents)):
        #     message = message  + '0'
        # self.phone.send_message(message)
        return next

    def police_move_ai(self, view: GameView) -> int:
        # write your code here
        self.phone.send_message('00101001')
        return 1
