import collections
from collections import defaultdict
import heapq
import math
# import time


# Helper function for BFS
# Checks if x, y are valid values, if been visited before then don't add to queue. If valid values and haven't been
# visited then check before adding to queue if year_location is the target, if so return and output the results
def bfs_explore(year, x, y, parent_child_pair, bfs_queue, parents):
    global target_year_location
    x = str(x)
    y = str(y)
    year_location = (year, x, y)

    # check if not in parents, i.e. if not visited before
    if year_location not in parents and (0 <= int(x) < int(W)) and (0 <= int(y) < int(H)):
        parent_year_location = parent_child_pair[1]  # parent of current year_location is the child of the previous one

        if year_location == target_year_location:
            parents[year_location] = parent_year_location
            writeoutput(True, BFS_NAME, parents=parents)
            return True

        new_parent_child_pair = (parent_year_location, year_location)
        bfs_queue.append(new_parent_child_pair)
    return False


# BFS
# Cost: each move to any 8 neighbouring directions has cost 1, jump through any number of years is cost 1.
# Algorithm: Using a Queue, put all possible next moves (neighbouring 8 directions, as long as not out of index, and
#   all possible jaunts channels, x-y-year, from the current location) to the queue. Before adding to the queue check
#   if current action will result in reaching the goal, if so then return it without adding to queue.
#   Element format in queue: each element in the queue is a tuple pair of parent and child, both the parent and child
#   have the format (year, x, y)
# Channels: dict mapping each year to the potential jaunting year_locations
# Parents Dict: set of (year, x, y) children mapping to their parents. This will also be used to check if a
#   year_location has been visited before
def bfs(bfs_queue, channels):
    global target_year_location
    parents = dict()

    while bfs_queue:
        parent_child_pair = bfs_queue.popleft()
        parent_year_location = parent_child_pair[0]
        child_year_location = parent_child_pair[1]

        if child_year_location not in parents:  # If not visited
            parents[child_year_location] = parent_year_location

            year = child_year_location[0]
            x = child_year_location[1]
            y = child_year_location[2]

            if bfs_explore(year, int(x) - 1, int(y) - 1, parent_child_pair, bfs_queue, parents):
                return  # bot-left
            if bfs_explore(year, x, int(y) - 1, parent_child_pair, bfs_queue, parents):
                return  # bot
            if bfs_explore(year, int(x) + 1, int(y) - 1, parent_child_pair, bfs_queue, parents):
                return  # bot-right
            if bfs_explore(year, int(x) - 1, y, parent_child_pair, bfs_queue, parents):
                return   # left
            if bfs_explore(year, int(x) + 1, y, parent_child_pair, bfs_queue, parents):
                return  # right
            if bfs_explore(year, int(x) - 1, int(y) + 1, parent_child_pair, bfs_queue, parents):
                return  # top-left
            if bfs_explore(year, x, int(y) + 1, parent_child_pair, bfs_queue, parents):
                return   # top
            if bfs_explore(year, int(x) + 1, int(y) + 1, parent_child_pair, bfs_queue, parents):
                return   # top-right

            if year in channels:
                for year_location in channels[year]:
                    if x == year_location[1] and y == year_location[2]:
                        if bfs_explore(year_location[0], x, y, parent_child_pair, bfs_queue, parents): return

    # If not able to reach goal then return failure output
    writeoutput(False)


# Helper function for UCS
# Checks if x, y are valid values, if been visited before then don't add to queue. If valid values and haven't been
# visited then check if it's in the frontier, if so only add the element if it has a lower total cost. If it's not in
# the frontier then add it to the queue
def ucs_explore(step_cost, year, x, y, score_cost_childpair, ucs_queue, parents, visiting, visiting_costs):
    x = str(x)
    y = str(y)
    year = str(year)
    step_cost = str(step_cost)

    if (year, x, y) not in parents and (0 <= int(x) < int(W)) and (0 <= int(y) < int(H)):
        year_location = (year, x, y)
        total_cost = score_cost_childpair[0]  # grab total cost
        parent_child = score_cost_childpair[1]  # grab old parent and child (and step cost)
        parent_year_location = parent_child[1]  # parent of current year_location is the child of the previous one

        new_total_cost = int(total_cost) + int(step_cost)
        new_parent_child_stepcost = (parent_year_location, year_location, step_cost)

        # Check if the year_location is cheaper than the one in the frontier or it is not in the frontier then add
        # to queue
        if (year_location in visiting and visiting_costs[year_location] > new_total_cost) \
                or year_location not in visiting:
            new_tuple_list = (new_total_cost, new_parent_child_stepcost)
            visiting.add(year_location)
            visiting_costs[year_location] = new_total_cost
            heapq.heappush(ucs_queue, new_tuple_list)


# UCS
# Cost: Orthogonal moves have cost 10, diagonal cost 14, and jaunts cost number of years traveled.
# Algorithm: Using a priority queue, put all possible next moves with their respective costs, as long as not out of
#   index, and all possible jaunts channels, x-y-year from the current location, to the queue. Only after popping from
#   queue can we return the path if it includes the goal
# Element format in priority queue: each element in queue is a tuple (parent, child, step_cost)
# Parents Dict: (year, x, y) children mapping to their parents. This will also be used to check if a
#   year_location has been visited before
# Step Costs dict: mapping each child year_location to its step cost
# Visiting Costs dict: mapping each year_location in the frontier to its step cost
def ucs(ucs_queue, channels, step_costs):
    global target_year_location
    diagonal_cost = 14
    orthogonal_cost = 10

    visiting = set()  # frontier, set of year location tuples for the nodes that will be expanded next
    visiting_costs = dict()  # map each element from visiting set to its lowest total cost for this tuple so far

    parents = dict()

    while ucs_queue:
        score_cost_childpair = heapq.heappop(ucs_queue)

        parent_child_stepcost = score_cost_childpair[1]  # grab parent and child and step cost:
        # (parent, child, step_cost)
        parent_year_location = parent_child_stepcost[0]
        child_year_location = parent_child_stepcost[1]

        if child_year_location not in parents:  # If not visited
            parents[child_year_location] = parent_year_location  # Map current year_location to its parent
            step_costs[child_year_location] = parent_child_stepcost[2]  # Store current step count for child node

            if child_year_location == target_year_location:
                writeoutput(True, UCS_NAME, parents=parents, step_costs=step_costs)
                return

            if child_year_location in visiting:
                visiting.remove(child_year_location)
                del visiting_costs[child_year_location]

            year = child_year_location[0]
            x = child_year_location[1]
            y = child_year_location[2]

            ucs_explore(orthogonal_cost, year, int(x) - 1, y, score_cost_childpair, ucs_queue, parents, visiting,
                        visiting_costs)
            ucs_explore(orthogonal_cost, year, int(x) + 1, y, score_cost_childpair, ucs_queue, parents, visiting,
                        visiting_costs)
            ucs_explore(orthogonal_cost, year, x, int(y) - 1, score_cost_childpair, ucs_queue, parents, visiting,
                        visiting_costs)
            ucs_explore(orthogonal_cost, year, x, int(y) + 1, score_cost_childpair, ucs_queue, parents, visiting,
                        visiting_costs)
            ucs_explore(diagonal_cost, year, int(x) - 1, int(y) - 1, score_cost_childpair, ucs_queue, parents, visiting,
                        visiting_costs)
            ucs_explore(diagonal_cost, year, int(x) + 1, int(y) + 1, score_cost_childpair, ucs_queue, parents, visiting,
                        visiting_costs)
            ucs_explore(diagonal_cost, year, int(x) - 1, int(y) + 1, score_cost_childpair, ucs_queue, parents, visiting,
                        visiting_costs)
            ucs_explore(diagonal_cost, year, int(x) + 1, int(y) - 1, score_cost_childpair, ucs_queue, parents, visiting,
                        visiting_costs)

            if year in channels:
                for year_location in channels[year]:
                    if x == year_location[1] and y == year_location[2]:
                        ucs_explore(abs(int(year) - int(year_location[0])), year_location[0], x, y, score_cost_childpair
                                    , ucs_queue, parents, visiting, visiting_costs)

    # If not able to reach goal then return failure output
    writeoutput(False)


# Calculate using an admissible heuristic the integer cost from the given year location to the target. The heuristic
# uses the straight line distance plus the number of years traveled
def heuristic(start_year_location):
    global target_year_location
    scaling_factor = 10.0
    x1 = 1.0 * int(start_year_location[1])
    x2 = 1.0 * int(target_year_location[1])
    y1 = 1.0 * int(start_year_location[2])
    y2 = 1.0 * int(target_year_location[2])
    year1 = int(start_year_location[0])
    year2 = int(target_year_location[0])

    h = math.sqrt((x1 - x2)**2 + (y1 - y2)**2) * scaling_factor
    h = round(h + abs(year1 - year2))
    return int(h)


# Helper function for A*
# Checks if x, y are valid values, if been visited before then don't add to queue. If valid values and haven't been
# visited then check if it's in the frontier, if so only add the element if it has a A* score. If it's not in the
# frontier then add it to the queue
def a_star_explore(step_cost, year, x, y, score_cost_childpair, a_star_queue, parents, visiting, visiting_scores):
    x = str(x)
    y = str(y)
    year = str(year)
    step_cost = str(step_cost)

    if (year, x, y) not in parents and (0 <= int(x) < int(W)) and (0 <= int(y) < int(H)):
        year_location = (year, x, y)
        parent_child = score_cost_childpair[2]  # grab parent and child (and step cost)
        parent_year_location = parent_child[1]  # parent of current year_location is the child of the previous one

        total_cost = score_cost_childpair[1]  # grab total cost
        new_total_cost = int(total_cost) + int(step_cost)
        h = heuristic(year_location)
        f = h + new_total_cost  # f = h + g, where h is the heuristic to reach the target from the current node and g
        # is the real cost to reach current node

        new_parent_child_tuple = (parent_year_location, year_location, step_cost)

        if (year, x, y) not in visiting or ((year, x, y) in visiting and visiting_scores[(year, x, y)] > f):
            new_tuple_list = (f, new_total_cost, new_parent_child_tuple)
            if (year, x, y) not in visiting:
                visiting.add((year, x, y))
            visiting_scores[(year, x, y)] = f
            heapq.heappush(a_star_queue, new_tuple_list)


# A*
# Cost: Orthogonal moves have cost 10, diagonal cost 14, and jaunts cost number of years traveled.
# Algorithm: Using a priority queue, put all possible next moves with their respective A* scores, as long as not out of
#   index, and all possible jaunts channels, x-y-year from the current location, to the queue. Only after popping from
#   queue can we return the path if it includes the goal
# Element format in priority queue: each element in queue is a tuple (parent, child, step_cost)
# Parents Dict: (year, x, y) children mapping to their parents. This will also be used to check if a
#   year_location has been visited before
# Step Costs dict: mapping each child year_location to its step cost
# Visiting Costs dict: mapping each year_location in the frontier to its step cost
def a_star(a_star_queue, channels, step_costs):
    global target_year_location
    diagonal_cost = 14
    orthogonal_cost = 10

    visiting = set()
    visiting_scores = dict()  # map each element from visiting set to its lowest total cost for this tuple

    parents = dict()
    while a_star_queue:
        score_cost_childpair = heapq.heappop(a_star_queue)
        parent_child_stepcost = score_cost_childpair[2]  # grab parent and child and step cost: (parent, child, step_cost)
        parent_year_location = parent_child_stepcost[0]
        child_year_location = parent_child_stepcost[1]

        if child_year_location not in parents:  # If this year location tuple hasn't been visited yet
            parents[child_year_location] = parent_year_location
            step_costs[child_year_location] = parent_child_stepcost[2]

            if child_year_location == target_year_location:
                writeoutput(True, algorithm=A_STAR_NAME, parents=parents, step_costs=step_costs)
                return

            if child_year_location in visiting:
                visiting.remove(child_year_location)
                del visiting_scores[child_year_location]

            year = child_year_location[0]
            x = child_year_location[1]
            y = child_year_location[2]

            a_star_explore(orthogonal_cost, year, int(x) - 1, y, score_cost_childpair, a_star_queue, parents, visiting,
                           visiting_scores)
            a_star_explore(orthogonal_cost, year, int(x) + 1, y, score_cost_childpair, a_star_queue, parents, visiting,
                           visiting_scores)
            a_star_explore(orthogonal_cost, year, x, int(y) - 1, score_cost_childpair, a_star_queue, parents, visiting,
                           visiting_scores)
            a_star_explore(orthogonal_cost, year, x, int(y) + 1, score_cost_childpair, a_star_queue, parents, visiting,
                           visiting_scores)

            a_star_explore(diagonal_cost, year, int(x) - 1, int(y) - 1, score_cost_childpair, a_star_queue, parents,
                           visiting, visiting_scores)
            a_star_explore(diagonal_cost, year, int(x) + 1, int(y) + 1, score_cost_childpair, a_star_queue, parents,
                           visiting, visiting_scores)
            a_star_explore(diagonal_cost, year, int(x) - 1, int(y) + 1, score_cost_childpair, a_star_queue, parents,
                           visiting, visiting_scores)
            a_star_explore(diagonal_cost, year, int(x) + 1, int(y) - 1, score_cost_childpair, a_star_queue, parents,
                           visiting, visiting_scores)

            if year in channels:
                for year_location in channels[year]:
                    if x == year_location[1] and y == year_location[2]:
                        a_star_explore(abs(int(year) - int(year_location[0])), year_location[0], x, y,
                                       score_cost_childpair , a_star_queue, parents, visiting, visiting_scores)

    # If not able to reach goal then return failure output
    writeoutput(False)


# Use any of the implementation of BFS, UCS or A*
def search(algorithm, channels):
    global initial_year_location
    global target_year_location

    if algorithm == BFS_NAME:
        bfs_queue = collections.deque()
        initial_parent_child = (-1, initial_year_location)  # parent child pair. For initial point parent is -1
        parents = dict()
        parents[initial_year_location] = -1

        if initial_year_location == target_year_location:
            writeoutput(True, algorithm, parents=parents)
            return

        bfs_queue.append(initial_parent_child)
        bfs(bfs_queue, channels)

    if algorithm == UCS_NAME:
        ucs_queue = []
        # Parent child pair. For initial point parent is -1
        initial_parent_child_stepcost = (-1, initial_year_location, '0')
        parents = dict()
        step_costs = dict()
        parents[initial_year_location] = -1
        step_costs[initial_year_location] = 0

        if initial_year_location == target_year_location:
            writeoutput(True, algorithm, parents=parents, step_costs=step_costs)
            return

        # First value (total cost) in the array pushed to heap must be integer so that the ordering of cost is correct
        heapq.heappush(ucs_queue, (0, initial_parent_child_stepcost))
        ucs(ucs_queue, channels, step_costs)

    if algorithm == A_STAR_NAME:
        a_star_queue = []
        initial_parent_child_stepcost = (-1,  initial_year_location, '0')  # parent child pair. For initial point parent
        parents = dict()
        step_costs = dict()
        parents[initial_year_location] = -1
        step_costs[initial_year_location] = 0

        if initial_year_location == target_year_location:
            writeoutput(True, algorithm, parents=parents, step_costs=step_costs)
            return

        f = heuristic(initial_year_location)  # f = g + h, g = 0 since its the start point

        # First value (total cost) in the array pushed to heap must be integer so that the ordering of cost is correct
        heapq.heappush(a_star_queue, (f, 0, initial_parent_child_stepcost))

        a_star(a_star_queue, channels, step_costs)


# Helper function to read input from input.txt, return the input values in an array in the following format:-
# [algorithm, W, H, initial_year_location, target_year_location, channels]
# algorithm: string for algorithm name
# W, H: string values for width and height of grid
# initial_year_location, target_year_location: tuples of the form year_location (year, x, y)
# channels: dict mapping each year to a potential year_location jump
def readinput():
    input_path = 'input.txt'
    input_file = open(input_path, 'r')
    file_content_array = input_file.readlines()

    input_values = [file_content_array[0]]  # algorithm to use

    w_h_array = file_content_array[1].split()
    input_values.append(w_h_array[0])  # W
    input_values.append(w_h_array[1])  # H

    initial_location_array = file_content_array[2].split()
    # initial year location: (year, x ,y)
    input_values.append((initial_location_array[0], initial_location_array[1], initial_location_array[2]))

    target_location_array = file_content_array[3].split()
    # target year location: (year, x ,y)
    input_values.append((target_location_array[0], target_location_array[1], target_location_array[2]))

    N = file_content_array[4]  # Number of lines for the channels
    input_values.append(defaultdict(list))
    for i in range(5, 5 + int(N)):
        channel = file_content_array[i]
        channel_split = channel.split()
        input_values[5][channel_split[0]].append((channel_split[3], channel_split[1], channel_split[2]))
        input_values[5][channel_split[3]].append((channel_split[0], channel_split[1], channel_split[2]))

    input_file.close()
    return input_values


# Print to output.txt, 1st line is cost, 2nd is number of lines, all next lines are the steps to reach the goal printed
# in the format: year x y step_cost
# Cost for:-
    #       bfs: each step costs 1
    #       ucs: stored in the cost steps dict (diagonal 14, neighbouring 10, jaunt number of years traveled)
    #       A*: stored in the cost steps dict (diagonal 14, neighbouring 10, jaunt number of years traveled)
def writeoutput(solution_exists, algorithm=None, parents=None, step_costs=None):
    output_path = 'output.txt'
    output_file = open(output_path, 'w')

    if not solution_exists:
        output_file.write('FAIL')
        output_file.close()
        return

    if algorithm == BFS_NAME:
        total_cost = 0
        steps_array = collections.deque()
        child_year_location = target_year_location
        parent_year_location = parents[child_year_location]
        if parent_year_location == -1:
            steps_array.append((0, child_year_location))

        step_cost = 1

        # Build up the array going from target all the way back to the initial year location
        while parent_year_location != -1:  # Reaching -1 means reaching the initial year location
            parent_year_location = parents[child_year_location]

            if parent_year_location == -1:
                step_cost = 0

            total_cost += int(step_cost)

            steps_array.append((step_cost, child_year_location))
            child_year_location = parent_year_location

        output_file.write(str(total_cost) + '\n')
        output_file.write(str(len(steps_array)) + '\n')

        for i in range(len(steps_array)):
            line = steps_array.pop()
            output_file.write(line[1][0] + " " + line[1][1] + " " + line[1][2] +
                              " " + str(line[0]) + "\n")
        output_file.close()


    if algorithm == UCS_NAME or algorithm == A_STAR_NAME:
        total_cost = 0
        steps_array = collections.deque()
        child_year_location = target_year_location
        parent_year_location = parents[child_year_location]

        if parent_year_location == -1: # if parent is -1 means the initial year location is the only element
            steps_array.append((0, child_year_location))

        # Build up the array going from target all the way back to the initial year location
        while parent_year_location != -1: # Reaching -1 means reaching the initial year location
            parent_year_location = parents[child_year_location]
            step_cost = step_costs[child_year_location]

            total_cost += int(step_cost)

            steps_array.append((step_cost, child_year_location))
            child_year_location = parent_year_location

        output_file.write(str(total_cost) + '\n')
        output_file.write(str(len(steps_array)) + '\n')

        for i in range(len(steps_array)):
            line = steps_array.pop()
            output_file.write(line[1][0] + " " + line[1][1] + " " + line[1][2] +
                              " " + str(line[0]) + "\n")
        output_file.close()


initial_year_location = ()
target_year_location = ()
W = 0
H = 0
BFS_NAME = "BFS"
UCS_NAME = "UCS"
A_STAR_NAME = "A*"


def main():
    input_values = readinput()

    # Inputs
    algorithm = input_values[0].rstrip()
    global W
    global H
    global initial_year_location
    global target_year_location
    global BFS_NAME
    global UCS_NAME
    global A_STAR_NAME
    W = input_values[1]
    H = input_values[2]
    initial_year_location = input_values[3]
    target_year_location = input_values[4]
    channels = input_values[5]

    # start = time.process_time()

    search(algorithm, channels)
    # print(time.process_time() - start)

if __name__ == "__main__":
    main()