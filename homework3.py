import collections
from collections import defaultdict
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
# Cost: each move to any 8 neighbouring directions has cost 1, jump through any number of years is cost 1
# Algorithm: Using a Queue, put all possible next moves (neighbouring 8 directions, as long as not out of index, and
#   all possible jaunts channels, x-y-year, from the current location) to the queue. Before adding to the queue check
#   if current action will result in reaching the goal, if so then return there.

def bfs(initial_year_location, target_year_location, channels):
    if initial_year_location == target_year_location:
        writeoutput(True, BFS_NAME, [initial_year_location])
        return
    visited = set()
    bfs_queue = collections.deque()
    path = [ initial_year_location ]
    bfs_queue.append(path)

    # print(bfs_queue)

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

# input_values [algorithm, W, H, initial_year_location, target_year_location, channels]
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

    output_file.close()
    # output_file.write('My output is:\n')


# output_path = 'output.txt'
# output_file = open(output_path, 'w')
#
# output_file.write('My output is:\n')
#
# output_file.write("Algorithm: " + file_content_array[0]);
# output_file.write("W H: " + file_content_array[1]);
# output_file.write("Initial year-location: " + file_content_array[2]);
# output_file.write("Target year-location: " + file_content_array[3]);
# output_file.write("N (number of channels): " + file_content_array[4]);
#
# for i in range(5, 5+int(file_content_array[4])):
#     output_file.write("Channel " + str(i-4) + ": " + file_content_array[i]);
#
# input_file.close()
# output_file.close()


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
    algorithm = input_values[0]
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

    # print("W= " + W + ", " + "H= " + H + ", " + "initial_year_location= " + str(initial_year_location) + ", " + "target_year_location= " + str(target_year_location) + ", " + "channels= " + str(channels))

    # if initial_year_location == target_year_location: print("FOUND  :format this to proper output")
    start = time.process_time()
    # your code here

    bfs(initial_year_location, target_year_location, channels)
    print(time.process_time() - start)



# TODO put the following in two methods that grab the data from the input file and outputs to an output file
# input file, and another method that writes out the output.txt
# input_path = 'input.txt'
# input_file = open(input_path, 'r')
# file_content_array = input_file.readlines()
#
# output_path = 'output.txt'
# output_file = open(output_path, 'w')
#
# output_file.write('My output is:\n')
#
# output_file.write("Algorithm: " + file_content_array[0]);
# output_file.write("W H: " + file_content_array[1]);
# output_file.write("Initial year-location: " + file_content_array[2]);
# output_file.write("Target year-location: " + file_content_array[3]);
# output_file.write("N (number of channels): " + file_content_array[4]);
#
# for i in range(5, 5+int(file_content_array[4])):
#     output_file.write("Channel " + str(i-4) + ": " + file_content_array[i]);
#
# input_file.close()
# output_file.close()
#

if __name__ == "__main__":
    main()