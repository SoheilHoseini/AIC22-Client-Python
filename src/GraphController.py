from src.model import Graph, Path

class GraphController:
    """Config the graph charachteristics"""
    
    def __init__(self, graph: Graph):
        self.graph = graph
        self.nodes_cnt = len(graph.nodes)
        
        self.adjacent_paths:list
        self.adjacent_paths = [[] for i in range(self.nodes_cnt + 1)] # nodes' IDs are not zero based apparently :)
        self.shortest_path = self.floyd_warshall_algorithm()
        
        path:Path
        for path in graph.paths:
            self.adjacent_paths[path.first_node_id.id].append(path)
            self.adjacent_paths[path.second_node_id.id].append(path)
        
    def get_graph(self):
        """Returns the given graph"""
        return self.graph
    
    def get_adjacent_path(self, node_id: int):
        """Get all adjacent paths to the given node"""
        return self.adjacent_paths[node_id] 
     
    def get_distance(self, u: int, v: int):
        """Get the distence between node u and v"""
        return self.shortest_path[u][v]
    
    def bfs_algorithm(self, source):
        """"""
        pass
    
    def dijkstra_algorithm(self, source):
        pass
    
    def floyd_warshall_algorithm(self):
        """Implement floyd algorithm to calculate the shortest path"""
        
        row = [1 for i in range(self.nodes_cnt + 1)]
        sp = [row for i in range(self.nodes_cnt + 1)] # a 2D list to store shortest path between each two nodes
        
        for i in range(1, self.nodes_cnt + 1):
            for j in range(1, self.nodes_cnt + 1):
                sp[i][j] = self.nodes_cnt + 1
                
                
        for i in range(1, self.nodes_cnt + 1):
            sp[i][i] = 0
            
        path: Path
        for path in self.graph.paths:
            u = path.first_node_id.id
            v = path.second_node_id.id
            sp[u][v] = 1
            sp[v][u] = 1
            
        
        for k in range(1, self.nodes_cnt + 1):
            for i in range(1, self.nodes_cnt + 1):
                for j in range(1, self.nodes_cnt + 1):
                    sp[i][j] = min(sp[i][j] , (sp[i][k] + sp[k][j]))
                    
        
        return sp
    
    def get_next_on_path(self, source_node_id: int, dest_node_id: int):
        """returns the next node in the path towards the detination node"""
        path: Path
        for path in self.adjacent_paths[source_node_id]:
            next_node_id = path.first_node_id.id ^ path.second_node_id.id ^ source_node_id
            if (self.shortest_path[source_node_id][dest_node_id] == self.shortest_path[next_node_id][dest_node_id] + 1):
                return next_node_id
        
        return source_node_id 
    
    def get_score(self, node_id: int, polices_list):#??
        closest = 1000000
        for police in polices_list:
            closest = min(closest, self.get_distance(node_id, police))
        return closest