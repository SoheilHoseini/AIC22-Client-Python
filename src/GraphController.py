from src.model import Graph, Path

class GraphController:
    """Config the graph charachteristics"""
    
    def __init__(self, graph: Graph):
        self.graph = graph
        self.nodes_cnt = len(graph.nodes)
        self.adjacent_paths = [[] for i in range(self.nodes_cnt + 1)] # nodes' IDs are not zero based apparently :)
        self.shortest_path = self.floyd_warshall_algorithm()
        
        for path in graph.paths:
            self.adjacent_paths[path.first_node_id].append[path]
            self.adjacent_paths[path.second_node_id].append[path]
        
    def get_graph(self):
        """Returns the given graph"""
        return self.graph
    
    def get_adjacent_path(self, node_id):
        """Get all adjacent paths to the given node"""
        return self.adjacent_paths[node_id] 
     
    def get_distance(self, u, v):
        """Get the distence between node u and v"""
        return self.shortest_path[u][v]
    
    def bfs_algorithm(self, source):
        """"""
        pass
    
    def dijkstra_algorithm(self, source):
        pass
    
    def floyd_warshall_algorithm(self):
        """Implement floyd algorithm to calculate the shortest path"""
        
        sp = [[] for i in range(self.nodes_cnt + 1)] # a 2D list to store shortest path between each two nodes
        
        for i in range(1, self.nodes_cnt + 1):
            for j in range(1, self.nodes_cnt + 1):
                sp[i][j] = self.nodes_cnt + 1
                
                
        for i in range(1, self.nodes_cnt + 1):
            sp[i][i] = 0
            
        
        for path in self.graph.paths:
            u = path.first_node_id
            v = path.second_node_id
            sp[u][v] = 1
            sp[v][u] = 1
            
        
        for k in range(1, self.nodes_cnt + 1):
            for i in range(1, self.nodes_cnt + 1):
                for j in range(1, self.nodes_cnt + 1):
                    sp[i][j] = min(sp[i][j] , (sp[i][j], sp[i][k] + sp[k][j]))
                    
        
        return sp
    
    def get_next_on_path(self, source, dest):
        """returns the next node in the path towards the detination node"""
        for path in self.adjacent_paths[source]:
            next_node = path.first_node_id ^ path.second_node_id ^ source
            if (self.shortest_path[source][dest] == self.shortest_path[next_node][dest] + 1):
                return next_node
        
        return source 
    
    def get_score(self, node_id, polices_list):
        closest = 1000000
        for police in polices_list:
            closest = min(closest, self.get_distance(node_id, police))
        return closest