from asyncio.windows_events import NULL
from operator import le
from random import randint, random, seed
from src.GraphController import GraphController
from src.client import GameClient
from src.hide_and_seek_pb2 import THIEF, Agent
from src.model import *


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
        self.thiefs = list()
        self.graph_controller = NULL

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
        self.phone.send_message('00101001')
        
        # write your code here
        if self.graph_controller == NULL:
            self.graph_controller = GraphController(view.config.graph)
        
        me = view.viewer
        visibleTurns = view.config.visible_turns
        if view.turn.turn_number in visibleTurns:
            self.update_thief(view)
        
        if len(self.thiefs) == 0:
            dest = randint(0, len(view.config.graph.nodes) + 1)
            return self.graph_controller.get_next_on_path(me.node_id, dest)
        
        closestThief = NULL
        for thief in self.thiefs:
            if closestThief == NULL:
                if randint(0,5) < 2:
                    closestThief = thief
                    
            if type(closestThief) == Agent and self.graph_controller.get_distance(me.node_id, thief.node_id) < self.graph_controller.get_distance(me.node_id, closestThief.node_id):
                if randint(0,5) < 2:
                    closestThief = thief
                    
        if closestThief != NULL:
            return self.graph_controller.get_next_on_path(me.node_id, closestThief.node_id)
        
        return me.node_id
                                           
            
        #return 1

    def update_thief(self, gameView: GameView):
        me = gameView.viewer
        for agent in gameView.visible_agents:
            if agent.team != me.team and agent.agent_type == AgentType.THIEF and not agent.is_dead:
                self.thiefs.append(agent)
        
    