import math
import copy

LUT = "ABCD"

class Node():
    def __init__(self, id):
        self.id = id
        self.distance_vector = {}
        self.update_message = {}

    def creat_empty_distance_vector(self, node_num):
        for via in range(node_num):
            self.distance_vector[via] = {}
            for to in range(node_num):
                self.distance_vector[via][to] = math.inf

    def set_distance_vector_item(self, via, to, distance):
        self.distance_vector[via][to] = distance

    def calc_update_message(self, to_whom):
        # when send to A, the data from A itself should be dropped
        self.update_message = {}
        for to in self.distance_vector.keys():
            if to == self.id:
                continue

            if to == to_whom:
                continue

            to_distance = math.inf
            for via in self.distance_vector.keys():
                if via == self.id:
                    continue
                # if via == to_whom:
                #     continue
                if self.distance_vector[via][to] < to_distance:
                    to_distance = self.distance_vector[via][to]
            self.update_message[to] = to_distance

            # for via in self.distance_vector.keys():
            #     if via == self.id:
            #         continue
            #     if via == to_whom:
            #         to_distance = math.inf
            #         break
            #     if self.distance_vector[via][to] < to_distance:
            #         to_distance = self.distance_vector[via][to]
            # self.update_message[to] = to_distance

        print(self.id,self.update_message)
        return self.update_message

    def update_using_update_message(self, from_whom, update_message):
        has_update = False
        distance = self.distance_vector[from_whom][from_whom]
        for to_whom in update_message.keys():
            #if update_message[to_whom]+distance < self.distance_vector[from_whom][to_whom]:
            if self.distance_vector[from_whom][to_whom] != update_message[to_whom]+distance:
                has_update = True
                self.distance_vector[from_whom][to_whom] = update_message[to_whom]+distance

        return has_update

class Graph():
    def __init__(self):
        self.nodes = []
        self.nodes_update_data = []
        self.distances = []
        self.round_count = 0

    def creat_node(self, node_num):
        for i in range(node_num):
            node = Node(len(self.nodes))
            self.nodes.append(node)
            self.distances.append([math.inf]*(len(self.nodes)-1)+[0])

    def connect(self, id0, id1, distance):
        if id0 < id1:
            id0, id1 = id1, id0
        # so id0 > id1 now
        self.distances[id0][id1] = distance

    def creat_all_node_tables(self):
        node_num = len(self.nodes)
        for i in range(node_num):
            self.nodes[i].creat_empty_distance_vector(node_num)

    def init_all_node(self):
        node_num = len(self.nodes)
        for i in range(node_num):
            for via in range(node_num):
                if i>via:
                    self.nodes[i].set_distance_vector_item(via, via, self.distances[i][via])
                else:
                    self.nodes[i].set_distance_vector_item(via, via, self.distances[via][i])


    def update_all_node_data(self):
        has_update = False
        distances_full = copy.deepcopy(self.distances)  # 不对原数据进行修改
        for i in range(len(self.nodes)):
            for j in range(i+1, len(self.nodes)):
                distances_full[i].append(self.distances[j][i])

        for to_whom in range(len(self.nodes)):
            for from_whom in range(len(self.nodes)):
                if from_whom == to_whom:
                    continue

                if self.nodes[to_whom].update_using_update_message(from_whom, self.nodes[from_whom].calc_update_message(to_whom)):
                    has_update = True

        return has_update

    def print_all_node_data(self):
        print("第",self.round_count,"轮")
        node_num = len(self.nodes)
        for i in range(node_num):
            print("id", LUT[self.nodes[i].id])
            print("Via |",end="")
            for via in range(node_num):
                if via == self.nodes[i].id:
                    continue
                print(str(LUT[via]).rjust(3, " "), end="|")
            print()
            for to in range(node_num):
                if to == self.nodes[i].id:
                    continue
                print("To", LUT[to], end="|")
                for via in range(node_num):
                    if via==self.nodes[i].id:
                        continue
                    print(str(self.nodes[i].distance_vector[via][to]).rjust(3, " "), end=" ")
                print()
            print()
        print("-" * 10)

    def compute_untill_stable(self):
        while graph.update_all_node_data():
            self.round_count += 1
            #graph.print_all_node_data()
        return self.round_count




graph = Graph()
graph.creat_node(node_num=3)

graph.connect(0, 1, 4)
graph.connect(1, 2, 50)
graph.connect(0, 2, 1)

graph.creat_all_node_tables()
graph.init_all_node()

graph.compute_untill_stable()
graph.print_all_node_data()
print("Total Rounds:", graph.round_count)

graph.distances[1][0] = 60
graph.init_all_node()

graph.compute_untill_stable()
graph.print_all_node_data()
print("Total Rounds:", graph.round_count)

