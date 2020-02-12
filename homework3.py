import collections
from collections import defaultdict
import heapq
import time

# return false if target is found, or true otherwise
def bfs_explore(year, x, y, target_year_location, current_path, bfs_queue, visited):
    x = str(x)
    y = str(y)
    # print("x= " + x + ", y= " + y)
    if (year, x, y) not in visited and (0 <= int(x) < int(W)) and (0 <= int(y) < int(H)):
        # visited.add((year, x, y))
        # print("GOT HERE")
        if (year, x, y) == target_year_location:
            new_path = list(current_path)
            new_path.append((year, x, y))
            writeoutput(True, BFS_NAME, new_path)
            return True
        new_path = list(current_path)
        new_path.append((year, x, y))
        bfs_queue.append(new_path)
        # print("Append return value" + str(bfs_queue.append(new_path)))
        # print("Append return value" + str(bfs_queue))
        # return bfs_queue.append(new_path), False
    return False
    # return True


# BFS
# Cost: each move to any 8 neighbouring directions has cost 1, jump through any number of years is cost 1.
# Algorithm: Using a Queue, put all possible next moves (neighbouring 8 directions, as long as not out of index, and
#   all possible jaunts channels, x-y-year, from the current location) to the queue. Before adding to the queue check
#   if current action will result in reaching the goal, if so then return it without adding to queue.
#   Path format in queue: each path in the queue is an array of tuples, where a tuple is a time-year-location in the
#   format of (year, x, y)
# Visited Set: set of (year, x, y) visited tuples

def bfs(bfs_queue, target_year_location, channels, visited):
    while bfs_queue:
        current_path = bfs_queue.popleft()
        current_year_location = current_path[-1]
        if current_year_location not in visited:

            visited.add(current_year_location)

            year = current_year_location[0]
            x = current_year_location[1]
            y = current_year_location[2]
            # print("year= " + year + ", " + "x= " + x + ", " + "y= " + y + ", ")

            if bfs_explore(year, int(x) - 1, int(y) - 1, target_year_location, current_path, bfs_queue, visited): return  #bot-left

            if bfs_explore(year, x, int(y) - 1, target_year_location, current_path, bfs_queue, visited): return  #bot

            if bfs_explore(year, int(x) + 1, int(y) - 1, target_year_location, current_path, bfs_queue, visited): return  #bot-right

            if bfs_explore(year, int(x) - 1, y, target_year_location, current_path, bfs_queue, visited): return   #left

            if bfs_explore(year, int(x) + 1, y, target_year_location, current_path, bfs_queue, visited): return  #right

            if bfs_explore(year, int(x) - 1, int(y) + 1, target_year_location, current_path, bfs_queue, visited): return  #top-left

            if bfs_explore(year, x, int(y) + 1, target_year_location, current_path, bfs_queue, visited): return   #top

            if bfs_explore(year, int(x) + 1, int(y) + 1, target_year_location, current_path, bfs_queue, visited): return   #top-right
            # print(bfs_queue)

            if year in channels:
                for year_location in channels[year]:
                    if x == year_location[1] and y == year_location[2]:
                        if bfs_explore(year_location[0], x, y, target_year_location, current_path, bfs_queue, visited): return
    # If not able to reach goal then return failure output
    writeoutput(False)

def ucs_explore(step_cost, year, x, y, current_cost_path, ucs_queue, visited):
    global entry_count
    x = str(x)
    y = str(y)
    year = str(year)
    step_cost = str(step_cost)
    # step_cost = str(step_cost)
    if (year, x, y) not in visited and (0 <= int(x) < int(W)) and (0 <= int(y) < int(H)):
        # current_cost = current_cost_path[0]  # grab total cost

        total_cost = current_cost_path[0] # grab total cost
        entry_count = entry_count + 1 # grab entry count
        current_path = current_cost_path[2] # grab path

        new_path = list(current_path)
        new_step = (step_cost, (year, x, y))
        new_total_cost = str(int(total_cost) + int(step_cost))
        new_path.append(new_step)

        heapq.heappush(ucs_queue, (int(new_total_cost), entry_count, new_path))

# UCS
# Cost: Orthogonal moves have cost 10, diagonal cost 14, and jaunts cost number of years traveled
# Algorithm: Using a priority queue, put all possible next moves with their respective costs, as long as not out of
# index, and all possible jaunts channels, x-y-year from the current location, to the queue. Only after popping from
# queue can we return the path if it includes the goal
# Path format in priority queue: each path in queue is a tuple (total_cost, [array of tuples for this path] where the
# tuples in the array are of the format (current_step_cost, (year, x, y))
# Visited Set: set of (year, x, y) visited tuples
def ucs(ucs_queue, target_year_location, channels, visited):
    diagonal_cost = 14
    orthogonal_cost = 10

    while ucs_queue:
        current_cost_path = heapq.heappop(ucs_queue)

        current_path = current_cost_path[2] # grab path
        current_cost_step = current_path[-1]

        step_cost = current_cost_step[0] # grab step cost
        year_location = current_cost_step [1] # grab year location tuple
        if year_location not in visited:

            if year_location == target_year_location:
                writeoutput(True, UCS_NAME, current_path)
                return

            visited.add(year_location)
            # print("visited so far: " + str(visited))
            # print("target_year_location= " + str(target_year_location))
            # return
            year = year_location[0]
            x = year_location[1]
            y = year_location[2]

            ucs_explore(orthogonal_cost, year, int(x) - 1, y, current_cost_path, ucs_queue, visited)
            ucs_explore(orthogonal_cost, year, int(x) + 1, y, current_cost_path, ucs_queue, visited)
            ucs_explore(orthogonal_cost, year, x, int(y) - 1, current_cost_path, ucs_queue, visited)
            ucs_explore(orthogonal_cost, year, x, int(y) + 1, current_cost_path, ucs_queue, visited)

            ucs_explore(diagonal_cost, year, int(x) - 1, int(y) - 1, current_cost_path, ucs_queue, visited)
            ucs_explore(diagonal_cost, year, int(x) + 1, int(y) + 1, current_cost_path, ucs_queue, visited)
            ucs_explore(diagonal_cost, year, int(x) - 1, int(y) + 1, current_cost_path, ucs_queue, visited)
            ucs_explore(diagonal_cost, year, int(x) + 1, int(y) - 1, current_cost_path, ucs_queue, visited)

            if year in channels:
                for year_location in channels[year]:
                    if x == year_location[1] and y == year_location[2]:
                        ucs_explore(abs(int(year) - int(year_location[0])), year_location[0], x, y, current_cost_path,
                                    ucs_queue, visited)

    # If not able to reach goal then return failure output
    writeoutput(False)



        # current_cost = current_cost_path[0] # grab total cost
        # current_path = current_cost_path[1] # grab path
        # print("current total cost is: " + str(current_cost))
        # print("current path tuple is: " + str(current_path) + "\n")
        #
        # current_cost_step = current_path[0] # grab one step, i.e. cost_step from path
        # step_cost = current_cost_step[0] # grab step cost
        # year_location = current_cost_step [1] # grab year location tuple
        # print("current step cost: " + str(step_cost) + ", year location is: " + str(year_location))


def search(algorithm, initial_year_location, target_year_location, channels):
    # if initial_year_location == target_year_location:
    #     writeoutput(True, algorithm, [initial_year_location])
    #     return

    visited = set()

    if algorithm == BFS_NAME:
        bfs_queue = collections.deque()
        path = [initial_year_location]

        if initial_year_location == target_year_location:
            writeoutput(True, algorithm, path)
            return

        bfs_queue.append(path)
        bfs(bfs_queue, target_year_location, channels, visited)

    if algorithm == UCS_NAME:
        ucs_queue = []
        # path_cost format: [(step cost, (year,x,y)), (step cost, (year,x,y)).....]
        path_cost = [('0', initial_year_location)]
        # push on p queue an element of this format:
        # (path_total_cost, [(step_cost, (year,x,y)), (step_cost, (year,x,y))...])
        # popping from the queue will pop the path with the lowest total cost

        if initial_year_location == target_year_location:
            writeoutput(True, algorithm, path_cost)
            return

        # First value (total cost) in the tuple pushed to heap must be integer so that the ordering of cost is correct
        # use an entry count to prevent comparisons with equal total costs
        heapq.heappush(ucs_queue, (0, entry_count, path_cost))
        ucs(ucs_queue, target_year_location, channels, visited)


# input_values [algorithm, W, H, initial_year_location, target_year_location, channels]
# algorithm: string for algorithm name
# W, H: string values for width and height of grid
# initial_year_location, target_year_location: tuples of the form year_location (year, x, y)
# channels: dict mapping each year to a potential year_location jump
def readinput():
    input_path = 'input.txt'
    input_file = open(input_path, 'r')
    file_content_array = input_file.readlines()

    input_values = [file_content_array[0]] # algorithm to use

    w_h_array = file_content_array[1].split()
    input_values.append(w_h_array[0]) # W
    input_values.append(w_h_array[1]) # H

    initial_location_array = file_content_array[2].split()
    input_values.append((initial_location_array[0], initial_location_array[1], initial_location_array[2]))

    target_location_array = file_content_array[3].split()
    input_values.append((target_location_array[0], target_location_array[1], target_location_array[2]))

    N = file_content_array[4]
    input_values.append(defaultdict(list))
    for i in range(5, 5 + int(N)):
        channel = file_content_array[i]
        channel_split = channel.split()
        input_values[5][channel_split[0]].append((channel_split[3], channel_split[1], channel_split[2]))
        input_values[5][channel_split[3]].append((channel_split[0], channel_split[1], channel_split[2]))

    input_file.close()
    return input_values


def writeoutput(solution_exists, algorithm=None, solution_path=None):
    output_path = 'output.txt'
    output_file = open(output_path, 'w')

    if not solution_exists:
        print("Failing")
        output_file.write('FAIL')
        output_file.close()
        return

    # Print cost on 1st line
    # Cost for:-
    #       bfs: number of lines in solution path (minus 1, since first point doesn't add to cost)
    #       ucs: stored in the path steps (diagonal 14, neighbouring 10, jaunt number of years traveled)
    #       A*: stored in the path steps (diagonal 14, neighbouring 10, jaunt number of years traveled)

    # Print number of steps on 2nd line

    if algorithm == "BFS":
        output_file.write(str(len(solution_path) - 1) + '\n')
        output_file.write(str(len(solution_path)) + '\n')
        #First line is starting point, i.e. cost is 0
        output_file.write(solution_path[0][0] + " " + solution_path[0][1] + " " + solution_path[0][2] + " 0\n")
        for i in range(1, len(solution_path)):
            output_file.write(solution_path[i][0] + " " + solution_path[i][1] + " " + solution_path[i][2] + " 1\n")

    if algorithm == "UCS":
        total_cost = 0
        steps_array = []
        print("solution path length is: " + str(len(solution_path)))
        print("solution path: " + str(solution_path))
        for i in range(len(solution_path)):
            current_cost_step = solution_path[i]
            step_cost = current_cost_step[0]  # grab step cost
            year_location = current_cost_step[1]  # grab year location tuple

            total_cost += int(step_cost)

            steps_array.append((step_cost, year_location))

        output_file.write(str(total_cost) + '\n')
        output_file.write(str(len(solution_path)) + '\n')

        for i in range (len(solution_path)):
            output_file.write(solution_path[i][1][0] + " " + solution_path[i][1][1] + " " + solution_path[i][1][2] +
                              " " + str(solution_path[i][0]) + "\n")

    output_file.close()
    # output_file.write('My output is:\n')


initial_year_location = ()
target_year_location = ()
W = 0
H = 0
BFS_NAME = "BFS"
UCS_NAME = "UCS"
A_STAR_NAME = "A*"
entry_count = 0

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
    global entry_count
    W = input_values[1]
    H = input_values[2]
    initial_year_location = input_values[3]
    target_year_location = input_values[4]
    channels = input_values[5]

    # print("W= " + W + ", " + "H= " + H + ", " + "initial_year_location= " + str(initial_year_location)
    # + ", " + "target_year_location= " + str(target_year_location) + ", " + "channels= " + str(channels))

    # if initial_year_location == target_year_location: print("FOUND  :format this to proper output")
    start = time.process_time()

    # bfs(initial_year_location, target_year_location, channels)
    search(algorithm, initial_year_location, target_year_location, channels)
    print(time.process_time() - start)

if __name__ == "__main__":
    main()