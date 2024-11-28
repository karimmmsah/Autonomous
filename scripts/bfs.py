#! /usr/bin/env python3

def breadth_first(map, start, goal, direction):
	queue = [start]
	explored = []
	parents = []
	goal_reached = False
	while queue:
 		node = queue.pop(0)
 		if node == goal:
 			goal_reached = True
 			break
 			
 		neighbours = get_neighbours(node, direction)
 		for neighbour in neighbours:
 			if neighbour not in explored and map[neighbour[0]][neighbour[1]] == 1:
				 queue.append(neighbour)
				 explored.append(neighbour)
				 parents.append(node)
	if goal_reached:
 		get_path(start, goal, parents, explored)
	else:
 		print("Stuck")
 		
def get_path(start, goal, parents, explored):
	 path = [goal]
	 node = goal
	 while node != start:
		 path.append(parents[explored.index(node)]) # explored.index(node) 5
		 node = parents[explored.index(node)]
		 path.reverse()
		 print("The path is: " + str(path))
		 
def get_neighbours(node, direction):
	neighbours = []
	if direction == 1: #CW
		 neighbours.append([node[0], node[1]+1]) #node = [1, 1]
		 neighbours.append([node[0]+1, node[1]+1])
		 neighbours.append([node[0]+1, node[1]])
		 neighbours.append([node[0] + 1, node[1] - 1])
		 neighbours.append([node[0], node[1] - 1])
		 neighbours.append([node[0] - 1, node[1] - 1])
		 neighbours.append([node[0] - 1, node[1]])
		 neighbours.append([node[0] - 1, node[1] + 1])

	if direction == -1:
		 neighbours.append([node[0], node[1] + 1])
		 neighbours.append([node[0] - 1, node[1] + 1])
		 neighbours.append([node[0] - 1, node[1]])
		 neighbours.append([node[0] - 1, node[1] - 1])
		 neighbours.append([node[0], node[1] - 1])
		 neighbours.append([node[0] + 1, node[1] - 1])
		 neighbours.append([node[0] + 1, node[1]])
		 neighbours.append([node[0] + 1, node[1] + 1])
		 
	return neighbours
		 
if __name__ == '__main__':
	Map = [[0, 0, 0, 0, 0, 0, 0],
	[0, 1, 1, 1, 0, 0, 0],
	[0, 1, 1, 0, 0, 1, 0],
	[0, 1, 0, 1, 1, 1, 0],
	[0, 0, 0, 1, 1, 1, 0],
	[0, 0, 1, 1, 1, 1, 0],
	[0, 0, 0, 0, 0, 0, 0]]

	breadth_first(Map, [1,1], [5,5], 1) # map, start, goal, direction
