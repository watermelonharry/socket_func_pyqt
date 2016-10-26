# -*- coding: utf-8 -*-


class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}
        # Set distance to infinity for all nodes
        self.distance = 32400.0
        # Mark all nodes unvisited
        self.visited = False
        # Predecessor
        self.previous = None

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

    def set_distance(self, dist):
        self.distance = dist

    def get_distance(self):
        return self.distance

    def set_previous(self, prev):
        self.previous = prev

    def set_visited(self):
        self.visited = True

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])


class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, cost=0):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

    def get_vertices(self):
        return self.vert_dict.keys()

    def set_previous(self, current):
        self.previous = current

    def get_previous(self, current):
        return self.previous

    def readFromLines(self, lines):
        """
        读取直线list结构，保存为
        :param lines:
        :return:
        """


def shortest(v, path):
    ''' make shortest path from v.previous'''
    if v.previous:
        path.append(v.previous.get_id())
        shortest(v.previous, path)
    return


import heapq


def dijkstra(aGraph, start, target):
    print '''Dijkstra's shortest path'''
    # Set the distance for the start node to zero
    start.set_distance(0)

    # Put tuple pair into the priority queue
    unvisited_queue = [(v.get_distance(), v) for v in aGraph]
    heapq.heapify(unvisited_queue)

    while len(unvisited_queue):
        # Pops a vertex with the smallest distance
        uv = heapq.heappop(unvisited_queue)
        current = uv[1]
        current.set_visited()

        # for next in v.adjacent:
        for next in current.adjacent:
            # if visited, skip
            if next.visited:
                continue
            new_dist = current.get_distance() + current.get_weight(next)

            if new_dist < next.get_distance():
                next.set_distance(new_dist)
                next.set_previous(current)
                print 'updated : current = %s next = %s new_dist = %s' \
                      % (current.get_id(), next.get_id(), next.get_distance())
            else:
                print 'not updated : current = %s next = %s new_dist = %s' \
                      % (current.get_id(), next.get_id(), next.get_distance())

        # Rebuild heap
        # 1. Pop every item
        while len(unvisited_queue):
            heapq.heappop(unvisited_queue)
        # 2. Put all vertices not visited into the queue
        unvisited_queue = [(v.get_distance(), v) for v in aGraph if not v.visited]
        heapq.heapify(unvisited_queue)

def distOfPoints(x1,y1,x2,y2):
    """
    计算距离^2
    :param x1:
    :param y1:
    :param x2:
    :param y2:
    :return:
    """
    if __name__ == '__main__':
        return (x1 - x2)**2 + (y1 - y2)**2
    else:
        return ((x1 - x2)**2 + (y1 - y2)**2) *100000

def GetPath(lines,StartPoint, EndPoint):
    # 建立index 和 point字典

    # 'x|y': 1
    pointDict = {}
    # 1: (x,y)
    indexDict = {}
    indexedGraph = Graph()
    indexCount = 1
    newLines = []
    if lines is not None and len(lines) != 0:
        for singleLine in lines:
            indexedEdge = []
            try:
                #加入line的起点
                pointDictKey = '|'.join(str(x) for x in singleLine[:2])
                if pointDictKey not in pointDict:
                    pointDict[pointDictKey] = indexCount
                    indexDict[indexCount] = tuple(singleLine[:2])
                    indexCount += 1
                    indexedGraph.add_vertex(pointDict[pointDictKey])
                indexedEdge.append(pointDict[pointDictKey])
                # 加入line的终点
                pointDictKey = '|'.join(str(x) for x in singleLine[2:])
                if pointDictKey not in pointDict:
                    pointDict[pointDictKey] = indexCount
                    indexDict[indexCount] = tuple(singleLine[2:])
                    indexCount += 1
                    indexedGraph.add_vertex(pointDict[pointDictKey])
                indexedEdge.append(pointDict[pointDictKey])
            except Exception as e:
                print('error in dijkstra.GetPath.create dict:', e.message)

            if len(indexedEdge) == 2:
                # 加入edge
                try:
                    distance = distOfPoints(*(indexDict[indexedEdge[0]] + indexDict[indexedEdge[1]]))
                    indexedGraph.add_edge(indexedEdge[0], indexedEdge[1], distance)
                except Exception as e:
                    print('error in error in dijkstra.GetPath.add edge:',e.message)
            else:
                raise ('error in dijkstra.GetPath: invalid line.')

        #计算path
        try:
            startIndex = pointDict['|'.join(str(x) for x in StartPoint)]
            endIndex = pointDict['|'.join(str(x) for x in EndPoint)]
            dijkstra(indexedGraph, indexedGraph.get_vertex(startIndex), indexedGraph.get_vertex(endIndex))

            target = indexedGraph.get_vertex(endIndex)
            path = [target.get_id()]
            shortest(target, path)
            path = path[::-1]

            for i in range(0,len(path)-1):
                strPoints = indexDict[path[i]]
                endPoints = indexDict[path[i+1]]
                newLines.append(strPoints + endPoints)

            print(path)
            print (newLines)
            return newLines

        except Exception as e:
            print('error in  dijkstra.GetPath:', e.message)




if __name__ == '__main__':
    # g = Graph()
    #
    # g.add_vertex(1)
    # g.add_vertex(2)
    # g.add_vertex(3)
    # g.add_vertex(4)
    # g.add_vertex(5)
    # g.add_vertex(6)
    #
    # g.add_edge(1, 2, 7)
    # g.add_edge(1, 3, 9)
    # g.add_edge(1, 6, 14)
    # g.add_edge(2, 3, 10)
    # g.add_edge(2, 4, 15)
    # g.add_edge(3, 4, 11)
    # g.add_edge(3, 6, 2)
    # g.add_edge(4, 5, 6)
    # g.add_edge(5, 6, 9)
    #
    # print 'Graph data:'
    # for v in g:
    #     for w in v.get_connections():
    #         vid = v.get_id()
    #         wid = w.get_id()
    #         print '( %s , %s, %3d)' % (vid, wid, v.get_weight(w))
    #
    # dijkstra(g, g.get_vertex(1), g.get_vertex(5))
    #
    # target = g.get_vertex(5)
    # path = [target.get_id()]
    # shortest(target, path)
    # print 'The shortest path : %s' % (path[::-1])

    lines = [
        (0,0,1,-1),
        (1,-1,2,2),
        (1,-1,2,0),
        (2,2,3,1),
        (2,0,3,-2),
        (3,1,3,-2),
        (3,1,4,2),
        (4,2,5,1),
        (4,2,5,-1),
        (3,-2,5,-1),
        (5,1,5,-1),
        (5,1,6,0),
        (5,-1,6,0)
    ]
    GetPath(lines,(0,0),(6,0))