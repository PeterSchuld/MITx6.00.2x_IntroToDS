# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 17:27:04 2019

@author: peter
"""

'''
From MIT OpenCourseWare Intro. to Computational Thinking and Data Science

PLEASE NOTE: ps1_partition.py function provided with the problem set. Function 
names and additional hints on how to think about writing the code were also provided.

Use a greedy and a brute force algorithm to determine how many space cows can
fit in space transport that is limited to a maximum weight of 10 units. Compare
the results and run time of the two functions. 
 
'''

from ps1_partition import get_partitions
import time

def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    # Create empty dict to hold cow names/weights
    cow_dict = {}
    
    # using with/as will ensure that the file is opened, read and closed without
    # explicitly needing the line of code that closes the file.    
    with open(filename) as f:
    
        # Use for loop to read lines from a file one at a time. supposed to be fast 
        # and memory efficient
        for line in f:
        
            # Split each line at comma and save to list
            line_list = line.split(",")
            
            # Use list indices 0,1 to create dictionary entries
            cow_dict[line_list[0]] = int(line_list[1]) 
    
    # return dict of cow name as key and cow weight as int value    
    return cow_dict

#print(load_cows("ps1_cow_data.txt"))
        
    

def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # Below code based on 0/1 knapsack greedy algorithm.
    # Sort cows dict by values (i.e. cow weights) in reverse order and save to 
    # copy of dict so that original dict is not mutated. Lambda function from
    # answer by Mark from https://stackoverflow.com/questions/613183/sort-a-python-dictionary-by-value
    # I think this takes each dict entry as a tuple and sorts by index 1 which
    # is the value.
    Kuh = sorted(cows,key=cows.get,reverse=True)
    Ergebnis = []
    while True:
        
        trip = []
        totalvalue = 0
        for i in Kuh:
            
            if totalvalue + cows[i] <= limit:
                trip.append(i)
                totalvalue += cows[i]
        
        Ergebnis.append(trip)
        temp = []
        for i in Kuh:
            if i not in trip:
               temp.append(i) 
        Kuh = temp
        if Kuh == []:
            break

    return Ergebnis
    
#print("Test greedy_cow_transport", greedy_cow_transport(load_cows("ps1_cow_data.txt"), 10))


    


def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # Initialize variable which will store the best trip so far
    result = []
    
    # Cycle through every possible combination of trips
    for partition in get_partitions(cows):
        # Count number of trips
        trips = len(partition)
        # Initialize variable which will be used to check if weight not exceeded
        flag = True
        # Cycle through each trip
        for item in partition:
            # Initialize weight of this trip to 0
            weight = 0
            # Cycle through each cow on this trip and add up the weight
            for element in item:
                weight += cows[element]
            # If weight limit exceeded, flag it and exit loop
            if weight > limit:
                flag = False
                break
        # If weight not exceeded and number of trips is fewest, then store as result
        if flag == True:
            if trips < len(result) or len(result) == 0:
                result = partition
    
    # Return best result
    return result
    
# Test brute force appears to be working correctly.
#print("Test brute_force_cow_transport:", brute_force_cow_transport(load_cows("ps1_cow_data.txt"),limit=10))   
        

def compare_cow_transports_short(functions, cow_data, weight_limit):
    ''' 
    This function allows for the comparison of multiple functions. 
    
    Functions is a list of function names without the trailing (). Cow_data is a function that calls 
    cow data from a file. Weight_limit is an int and the weight limit for each trip.
    Prints out the number of trips and time to complete for each function in the list.
    '''
    # Iterate over functions in functions list
    for function in functions:
        
        # Start tracking time 
        start = time.time()
        
        # Run each function using the cow_data and weight_limit arguments passed in
        # to compare_cow_transports_short function.
        # Save result to a variable.
        this_function_result = function(cow_data, weight_limit)
        
        # Stop tracking time
        end = time.time()
        
        # Get number of trips by counting the length of the list returned
        num_trips = len(this_function_result)
        
        # Print out the function name by calling its __name__ attribute and print
        # the number of trips that resulted from the function.
        print("\n" + function.__name__ + " function returns " + str(num_trips) + " trips.")
        
        # Print the time it took to run each function by subtracting end from start and 
        # rounding the result.
        print("The time it took to run is", round((end - start),5), "seconds.\n")

# Call compare_cow_transports_short 
print(compare_cow_transports_short([greedy_cow_transport, brute_force_cow_transport], load_cows("ps1_cow_data.txt"), 10))

cows = load_cows("ps1_cow_data.txt")

#for partition in get_partitions(cows):
#    print(partition)