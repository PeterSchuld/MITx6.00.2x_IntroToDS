###########################
# 6.00.2x Problem Set 1: Space Cows 

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

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

    cow_dict = dict()

    f = open(filename, 'r')
    
    for line in f:
        line_data = line.split(',')
        cow_dict[line_data[0]] = int(line_data[1])
    return cow_dict


# Problem 1
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
    # TODO: Your code here
    #pass
    cows_copy = sorted(cows.items(), key=lambda x: x[1], reverse=True)
    print()
    print(cows_copy)
    # Create empty list to hold cow names and all_results list to hold lists of 
    # those cow names. 
    result = []
    all_results = []
    
    # Initialize total_weight at 0. Will be used to compare total cow weights to
    # given weight limit provided as a parameter to the function.
    total_weight = 0
    
    # Iterate over the sorted cow tuples in cows_copy
    for cow in cows_copy:
        
        # If total_weight + the weight of current cow is > the limit
        if (total_weight + cow[1]) > limit:
        
            # reset total_weight to zero to start a new trip
            total_weight = 0 
            
            # add current results list to all_results
            all_results.append(result)
            
            # reset results to empty list
            result = []
           
            # Append the current cow to results. This is the cow which put the 
            # previous results list over the limit. We need to add it to the 
            # results list here because otherwise we will lose it when the loop
            # moves on to the next cow.
            result.append(cow[0])
            
            # Add the weight of the current cow to total_weight and then advance
            # the loop to the next cow.
            total_weight += cow[1]
        else:
            # If the total_weight is not exceeded with the current cow, then 
            # add that cow to the results list and add the cow's weight to the 
            # total weight and advance the loop to the next cow.
            result.append(cow[0])
            total_weight += cow[1]
    
    # Append current results list to all_results
    all_results.append(result)
    
    # Return all_results
    return all_results


# Problem 2
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
    # TODO: Your code here
    pass
    # best_part will be a list of lists and will hold one of the partitions from the generator
    best_part = None 
    
    # fewest trips is an int, default to 0 and use zero to check against in the conditional 
    fewest_trips = 0 

    # get_partitions() is a helper function provided by the professor. It
    # creates partitions of cows to enumerate all of the possible ways the cows
    # can be divided. A partition creates sets of elements in all combinations, 
    # but does not include an empty set and no element is included in more than 
    # one partition subset. 
    # This code creates a generator instead of a list. This allows for memory 
    # savings because a generator is made and used at (sort of) the same time,
    # meaning nothing is stored in memory. You iterate through a generator by
    # using a for loop.     
    # Use for loop to access each partition from the generator
    for partition in get_partitions(cows):
        
        # Call the check_cow_list_weight() function to ensure no single trip 
        # exceeds the weight limit. Trips that exceed the weight limit disqualify
        # the partition to which they belong from being considered for best_part.
        # If check_cow_list_weight() returns a tuple with True in index 0, then
        # the partition includes trips that meet the weight limit.
        (valid_part, current_trips) = check_cow_list_weight(cows, partition, limit, current_trips=0)
        
        if valid_part:
            
            # Below conditional is necessary because I default fewest_trips to 0
            # when initializing the variable outside of the loop. Fewest_trips
            # should only be 0 on the first iteration of the loop, so that first partition
            # will by default be the fewest_trips and we'll compare against it 
            # going forward through the rest of the partitions.
            if fewest_trips == 0:
                fewest_trips = current_trips
                best_part = partition
            
            # Using < only instead of <= because we can break ties arbitrarily
            if current_trips < fewest_trips: 
                fewest_trips = current_trips
                best_part = partition
        # If check_cow_list_weight() returns a tuple with False in the index 0, 
        # then the partition has a trip that is over the weight limit and therefore
        # not eligible for consideration as best_part. So, the loop should continue
        # on to the next partition to check weight and ultimately number of trips.
        else:
            continue

    return best_part    
    
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


        
# Problem 3
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    # TODO: Your code here
    pass
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


"""
Here is some test data for you to see the results of your algorithms with. 
Do not submit this along with any of your answers. Uncomment the last two
lines to print the result of your problem.
"""

cows = load_cows("ps1_cow_data.txt")
limit=10
print(cows)

print(greedy_cow_transport(cows, limit))
print(brute_force_cow_transport(cows, limit))


