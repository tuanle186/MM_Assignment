from collections import defaultdict
import heapq
import networkx as nx
import matplotlib.pyplot as plt

class MinCostFlowSolver:
    def __init__(self, num_nodes):
        self.num_nodes = num_nodes
        self.graph = defaultdict(list)

    def add_edge(self, u, v, capacity, cost):
        self.graph[u].append((v, capacity, cost))
        self.graph[v].append((u, 0, -cost))  # Backward edge

    def dijkstra(self, source, target):
        dist = [float('inf')] * self.num_nodes
        parent = [-1] * self.num_nodes
        dist[source] = 0

        priority_queue = [(0, source)]

        while priority_queue:
            current_dist, u = heapq.heappop(priority_queue)

            if current_dist > dist[u]:
                continue

            for v, capacity, cost in self.graph[u]:
                if capacity > 0 and dist[u] + cost < dist[v]:
                    dist[v] = dist[u] + cost
                    parent[v] = u
                    heapq.heappush(priority_queue, (dist[v], v))

        return dist, parent

    def min_cost_flow(self, source, target, flow):
        total_cost = 0
        total_flow = 0

        while True:
            dist, parent = self.dijkstra(source, target)

            if dist[target] == float('inf'):
                break

            augmenting_flow = float('inf')
            node = target

            while node != source:
                parent_node = parent[node]
                for edge in self.graph[parent_node]:
                    if edge[0] == node:
                        augmenting_flow = min(augmenting_flow, edge[1])
                node = parent_node

            total_flow += augmenting_flow
            total_cost += dist[target] * augmenting_flow

            node = target
            while node != source:
                parent_node = parent[node]
                for i, edge in enumerate(self.graph[parent_node]):
                    if edge[0] == node:
                        self.graph[parent_node][i] = (edge[0], edge[1] - augmenting_flow, edge[2])
                        break
                found = False
                for i, edge in enumerate(self.graph[node]):
                    if edge[0] == parent_node:
                        self.graph[node][i] = (edge[0], edge[1] + augmenting_flow, edge[2])
                        found = True
                        break
                if not found:
                    self.graph[node].append((parent_node, augmenting_flow, -self.graph[parent_node][-1][2]))
                node = parent_node

        return total_flow, total_cost
    def plot_graph(self):
        G = nx.DiGraph()

        for u, edges in self.graph.items():
            for v, capacity, cost in edges:
                if capacity > 0:  # Only include forward edges
                    G.add_edge(u, v, capacity=capacity, cost=cost)

        pos = nx.spring_layout(G)
        edge_labels = {(u, v): f"Cap:{G[u][v]['capacity']}\nCost:{G[u][v]['cost']}" for u, v in G.edges()}

        nx.draw(G, pos, with_labels=True, node_size=700, node_color="skyblue", font_size=10, arrows=True, connectionstyle='arc3,rad=0.1', arrowstyle='->')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        plt.show()




# Sample input
solver = MinCostFlowSolver(4)
solver.add_edge(0, 1, 10, 2)
solver.add_edge(0, 2, 5, 3)
solver.add_edge(1, 2, 2, 1)
solver.add_edge(1, 3, 8, 5)
solver.add_edge(2, 3, 10, 4)

solver.plot_graph()

source_node = 0
sink_node = 3

total_flow, total_cost = solver.min_cost_flow(source_node, sink_node, float('inf'))
print("Minimum Cost Flow:")
print("Total Flow:", total_flow)
print("Total Cost:", total_cost)