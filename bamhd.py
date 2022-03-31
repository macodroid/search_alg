import json
from collections import deque


class BaMHD(object):
    def __init__(self, db_file='ba_mhd_db.json'):
        # Initialize BaMHD object, load data from json file
        self.data = json.load(open(db_file, 'r'))

    def neighbors(self, stop):
        # Return neighbors for a given stop
        return self.data['neighbors'][stop]

    def stops(self):
        # Return list of all stops (names only)
        return self.data['neighbors'].keys()


class BusStop(object):
    # Object representing node in graph traversal. Includes name and parent node.
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent

    def traceBackPath(self):
        # Returns path represented by this node as list of node names (bus stop names).
        if self.parent == None:
            return [self.name]
        else:
            path = self.parent.traceBackPath()
            path.append(self.name)
            return path


def findPathIDDFS(bamhd, stopA, stopB):
    # Implement Iterative deepening depth-first search to find shortest path between two MHD stops in Bratislava.
    # Return a list of MHD stops, print how many bus stops were in the "OPEN list" at its maximum and 
    # how many bus stops you have inserted into the "OPEN list."
    route = []
    max_open, max_insert = 0, 0
    path_found = False
    depth = 1
    OPEN = [BusStop(stopA)]
    while OPEN and path_found is False:
        CLOSED = set()
        OPEN = [BusStop(stopA)]
        for i in range(depth):
            if len(OPEN) > max_open:
                max_open = len(OPEN)
            stop = OPEN.pop()
            CLOSED.add(stop.name)
            nb_stops = bamhd.neighbors(stop.name)
            for nb_stop in nb_stops:
                current_stop = BusStop(nb_stop, stop)
                if current_stop.name in CLOSED:
                    continue
                OPEN.append(current_stop)
                max_insert += 1
                if nb_stop == stopB:
                    route = current_stop.traceBackPath()
                    path_found = True
                    break
            if path_found is True:
                break
        depth += 1

    ### Your code here ###
    print('\tAt most {} bus stops in the "OPEN list", {} bus stops inserted into OPEN list" '.format(max_open,
                                                                                                     max_insert))
    if len(route) == 0:
        return ['Route not found']
    return route


def findPathDFS(bamhd, stopA, stopB):
    # Implement Depth-first search to find shortest path between two MHD stops in Bratislava.
    # Return a list of MHD stops, print how many bus stops were in the "OPEN list" at its maximum and 
    # how many bus stops you have inserted into the "OPEN list."
    route = []
    max_open = 0
    max_insert = 0
    path_found = False
    OPEN = [BusStop(stopA)]
    CLOSED = set()
    while OPEN and path_found is False:
        if len(OPEN) > max_open:
            max_open = len(OPEN)
        stop = OPEN.pop()
        CLOSED.add(stop.name)
        nb_stops = bamhd.neighbors(stop.name)
        for nb_stop in nb_stops:
            current_stop = BusStop(nb_stop, stop)
            if current_stop.name in CLOSED:
                continue
            OPEN.append(current_stop)
            max_insert += 1
            if nb_stop == stopB:
                route = current_stop.traceBackPath()
                path_found = True
                break
    ### Your code here ###
    print('\tAt most {} bus stops in the "OPEN list", {} bus stops inserted into OPEN list" '.format(max_open,
                                                                                                     max_insert))
    return route


def findPathBFS(bamhd, stopA, stopB):
    # Implement Breadth-first search to find the shortest path between two MHD stops in Bratislava.
    # Return a list of MHD stops, print how many bus stops were in the "OPEN list" at its maximum and 
    # how many bus stops you have inserted into the "OPEN list."
    best_route = []
    max_open = 0
    max_insert = 0
    shortest_path_found = False
    OPEN = deque([BusStop(stopA)])
    CLOSED = set()
    while OPEN and shortest_path_found is False:
        if len(OPEN) > max_open:
            max_open = len(OPEN)
        stop = OPEN.popleft()
        CLOSED.add(stop.name)
        nb_stops = bamhd.neighbors(stop.name)
        for nb_stop in nb_stops:
            current_stop = BusStop(nb_stop, stop)
            if current_stop.name in CLOSED:
                continue
            OPEN.append(current_stop)
            max_insert += 1
            if nb_stop == stopB:
                best_route = current_stop.traceBackPath()
                shortest_path_found = True
                break

    ### Your code here ###
    print(
        '\tAt most {} bus stops in the "OPEN list", {} bus stops inserted into OPEN list" '.format(max_open,
                                                                                                   max_insert))
    return best_route


if __name__ == "__main__":
    # Initialization
    bamhd = BaMHD()

    # # Examples of function usage:
    # # -> accessing the list of bus stops (is 'Zoo' a bus stop?)
    # print('Zoo' in bamhd.stops())
    # # -> get neighbouring bus stops
    # print(bamhd.neighbors('Zochova'))
    # # -> get whole path from last node of search algorithm
    # s1 = BusStop('Zoo')     # some dummy data
    # s2 = BusStop('Lafranconi', s1)
    # s3 = BusStop('Park kultury', s2)
    # print(s3.traceBackPath())
    # # -> using stack
    # stack = []
    # stack.append('a'); stack.append('b'); stack.append('c')
    # print('Retrieving from stack: {}, {}, {}'.format(stack.pop(), stack.pop(), stack.pop()))
    # # -> using queue
    # queue = deque()
    # queue.append('a'); queue.append('b'); queue.append('c')
    # print('Retrieving from queue: {}, {}, {}'.format(queue.popleft(), queue.popleft(), queue.popleft()))

    # Your task: find best route between two stops with IDDFS/BFS/DFS
    print('IDDFS Zoo - Aupark:')
    path = findPathIDDFS(bamhd, 'Zoo', 'Aupark')
    print('\tpath length: {}\n\tpath: {}'.format(len(path), path))

    print('BFS Zoo - Aupark:')
    path = findPathBFS(bamhd, 'Zoo', 'Aupark')
    print('\tpath length: {}\n\tpath: {}'.format(len(path), path))

    print('DFS Zoo - Aupark:')
    path = findPathDFS(bamhd, 'Zoo', 'Aupark')
    print('\tpath length: {}\n\tpath: {}\n'.format(len(path), path))

    print('IDDFS VW - Astronomicka:')
    path = findPathIDDFS(bamhd, 'Volkswagen', 'Astronomicka')
    print('\tpath length: {}\n\tpath: {}'.format(len(path), path))

    # print('IDDFS VW - HALABALA:')
    # path = findPathIDDFS(bamhd, 'Volkswagen', 'HALABALA')
    # print('\tpath length: {}\n\tpath: {}'.format(len(path), path))

    print('BFS VW - Astronomicka:')
    path = findPathBFS(bamhd, 'Volkswagen', 'Astronomicka')
    print('\tpath length: {}\n\tpath: {}'.format(len(path), path))

    print('DFS VW - Astronomicka:')
    path = findPathDFS(bamhd, 'Volkswagen', 'Astronomicka')
    print('\tpath length: {}\n\tpath: {}'.format(len(path), path))
