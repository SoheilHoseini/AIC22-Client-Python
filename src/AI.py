from asyncio.windows_events import NULL
from operator import le
from random import randint, random, seed
from tkinter import Pack
from src.GraphController import GraphController
from src.client import GameClient
from src.model import GameView, Agent, AgentType,Path


def get_thief_starting_node(gameView: GameView) -> int:
    node_count = len(gameView.config.graph.nodes)
    return randint(1,node_count)


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

    def thief_move_ai(self, gameView: GameView) -> int:
        
        if self.graph_controller == NULL:
            self.graph_controller = GraphController(gameView.config.graph)
            
        me:Agent
        me = gameView.viewer
        adjacentPath = self.graph_controller.get_adjacent_path(me.node_id)
        enemyPolices = []
        
        agent:Agent
        for agent in gameView.visible_agents:
            if( agent.team != me.team and agent.agent_type == AgentType.POLICE and agent.is_dead == False):
                enemyPolices.append(agent.id)
        
        next = me.node_id
        path:Path
        for path in adjacentPath:
            adjacentNode = me.node_id ^ path.first_node_id ^ path.second_node_id
            if (self.graph_controller.get_score(next, enemyPolices) < self.graph_controller.get_score(adjacentNode, enemyPolices)):
                next = adjacentNode

        # message = ''
        # for m in range(len(view.visible_agents)):
        #     message = message  + '0'
        # self.phone.send_message(message)
        return next

    def police_move_ai(self, gameView: GameView) -> int:
        #self.phone.send_message('00101001')
        
        if self.graph_controller == NULL:
            self.graph_controller = GraphController(gameView.config.graph)
        
        me:Agent
        me = gameView.viewer
        visibleTurns = gameView.config.visible_turns
        if gameView.turn.turn_number in visibleTurns:
            self.update_thief(gameView)
        
        my_paths = self.graph_controller.get_adjacent_path(me.node_id)
        adj_path: Path
        if len(self.thiefs) == 0:
            for adj_path in my_paths:
                if adj_path.first_node_id != me.node_id:
                    return adj_path.second_node_id
                else:
                    return adj_path.first_node_id
            # dest_node_id = randint(1, len(gameView.config.graph.nodes) - 1)
            # return self.graph_controller.get_next_on_path(me.node_id, dest_node_id)
        
        closestThief:Agent
        thief:Agent
        closestThief = NULL
        for thief in self.thiefs:
            if closestThief == NULL or self.graph_controller.get_distance(me.node_id, thief.node_id) < self.graph_controller.get_distance(me.node_id, closestThief.node_id):
                closestThief = thief
                
                #if randint(0,4) < 2:
                    
                    
        if closestThief != NULL:
            return self.graph_controller.get_next_on_path(me.node_id, closestThief.node_id)
        
        return me.node_id
                                           
            
        #return 1

    def update_thief(self, gameView: GameView):
        me = gameView.viewer
        
        agent: Agent
        for agent in gameView.visible_agents:
            if agent.team != me.team and agent.agent_type == AgentType.THIEF and agent.is_dead == False:
                self.thiefs.append(agent)
        
    