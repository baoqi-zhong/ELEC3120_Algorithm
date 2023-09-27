import math
import copy

LUT = "ABCD"


class Node():
    def __init__(self, id):
        self.id = id
        self.bandwidth_vector = {}
        self.update_message = {}

    def creat_empty_bandwidth_vector(self, node_num):
        for via in range(node_num):
            self.bandwidth_vector[via] = {}
            for to in range(node_num):
                self.bandwidth_vector[via][to] = 0

    def set_bandwidth_vector_item(self, via, to, bandwidth):
        self.bandwidth_vector[via][to] = bandwidth

    def calc_update_message(self, to_whom):
        # when send to A, the data from A itself should be dropped
        self.update_message = {}
        for to in self.bandwidth_vector.keys():
            if to == self.id:
                continue

            if to == to_whom:
                continue

            to_bandwidth = 0
            for via in self.bandwidth_vector.keys():
                if via == self.id:
                    continue
                if via == to_whom:
                    continue
                if self.bandwidth_vector[via][to] > to_bandwidth:
                    to_bandwidth = self.bandwidth_vector[via][to]
            self.update_message[to] = to_bandwidth

        # print(LUT[self.id],">", LUT[to_whom], self.update_message)
        return self.update_message

    def update_using_update_message(self, from_whom, update_message):
        has_update = False
        bandwidth = self.bandwidth_vector[from_whom][from_whom]
        for to_whom in update_message.keys():
            #if update_message[to_whom]+bandwidth < self.bandwidth_vector[from_whom][to_whom]:
            if self.bandwidth_vector[from_whom][to_whom] != min(update_message[to_whom], bandwidth):
                has_update = True
                self.bandwidth_vector[from_whom][to_whom] = min(update_message[to_whom], bandwidth)

        return has_update

class Graph():
    def __init__(self):
        self.nodes = []
        self.nodes_update_data = []
        self.bandwidths = []
        self.round_count = 0

    def creat_node(self, node_num):
        for i in range(node_num):
            node = Node(len(self.nodes))
            self.nodes.append(node)
            self.bandwidths.append([0]*(len(self.nodes)-1)+[0])

    def connect(self, id0, id1, bandwidth):
        if id0 < id1:
            id0, id1 = id1, id0
        # so id0 > id1 now
        self.bandwidths[id0][id1] = bandwidth

    def creat_all_node_tables(self):
        node_num = len(self.nodes)
        for i in range(node_num):
            self.nodes[i].creat_empty_bandwidth_vector(node_num)

    def init_all_node(self):
        node_num = len(self.nodes)
        for i in range(node_num):
            for via in range(node_num):
                if i>via:
                    self.nodes[i].set_bandwidth_vector_item(via, via, self.bandwidths[i][via])
                else:
                    self.nodes[i].set_bandwidth_vector_item(via, via, self.bandwidths[via][i])


    def update_all_node_data(self):
        has_update = False
        bandwidths_full = copy.deepcopy(self.bandwidths)  # 不对原数据进行修改
        for i in range(len(self.nodes)):
            for j in range(i+1, len(self.nodes)):
                bandwidths_full[i].append(self.bandwidths[j][i])

        update_messages = {}
        for to_whom in range(len(self.nodes)):
            update_messages[to_whom] = {}
            for from_whom in range(len(self.nodes)):
                if from_whom == to_whom:
                    continue

                update_messages[to_whom][from_whom] = self.nodes[from_whom].calc_update_message(to_whom)

        for to_whom in range(len(self.nodes)):
            for from_whom in range(len(self.nodes)):
                if from_whom == to_whom:
                    continue
                if self.nodes[to_whom].update_using_update_message(from_whom, update_messages[to_whom][from_whom]):
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
                    print(str(self.nodes[i].bandwidth_vector[via][to]).rjust(3, " "), end=" ")
                print()
            print()
        print("-" * 10)

    def compute_untill_stable(self):
        while graph.update_all_node_data():
            self.round_count += 1
            graph.print_all_node_data()

        return self.round_count


graph = Graph()
graph.creat_node(node_num=4)

graph.connect(0, 1, 5)
graph.connect(1, 2, 20)
graph.connect(0, 2, 10)
graph.connect(3, 1, 20)
graph.connect(3, 2, 10)

graph.creat_all_node_tables()
graph.init_all_node()

graph.print_all_node_data()
graph.compute_untill_stable()

print("Total Rounds:", graph.round_count)

# graph.bandwidths[2][0] = 60
# graph.init_all_node()
#
# graph.compute_untill_stable()
# graph.print_all_node_data()
# print("Total Rounds:", graph.round_count)
