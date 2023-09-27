import math
import copy
NAME = "ABCDE"

# from A to B
graph = []
searched = []
distance = []

def init_graph(node_num):
    global graph
    for i in range(node_num):
        graph.append([math.inf]*node_num)
        graph[i][i] = 0

def connect(from_node, to_node, distance):
    global graph
    graph[from_node][to_node] = distance

def init_distance(graph):
    global distance
    distance = [math.inf] * len(graph)
    distance[0] = 0


def update():
    global graph, distance

    min_distance = math.inf
    min_place = None

    for i in range(len(distance)):
        if i in searched:
            continue

        if distance[i]<min_distance:
            min_distance = distance[i]
            min_place = i

    searched.append(min_place)
    for i in range(len(distance)):
        if i in searched:
            continue
        if i==min_place:
            continue

        if min_distance + graph[min_place][i] < distance[i]:
            distance[i] = min_distance + graph[min_place][i]


NODE_NUM = 5

init_graph(NODE_NUM)
connect(0, 1, 10)
connect(0, 2, 3)
connect(1, 2, 1)
connect(2, 1, 4)
connect(1, 3, 2)
connect(2, 3, 8)
connect(2, 4, 2)
connect(3, 4, 7)
connect(4, 3, 9)

init_distance(graph)



while len(searched)<NODE_NUM:
    print(distance)
    update()


