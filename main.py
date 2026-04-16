import random  # used to generate random numbers later


# We start with ONE big hole (free memory)
# Negative number = free space
# Example: -100 means 100 units of free memory
memory = [-100]


# -------------------------------
# FIRST-FIT ALLOCATION FUNCTION
# -------------------------------

def first_fit(memory, size):
    """
    This function tries to allocate memory using the First-Fit strategy.
    
    First-Fit = pick the FIRST hole that is big enough.
    
    Parameters:
    memory -> list representing memory blocks
    size -> size of the block we want to allocate
    
    Returns:
    True if allocation worked
    False if it failed
    """

    # Loop through memory blocks
    for i in range(len(memory)):

        # Check if this block is a hole (negative)
        # and large enough to fit the request
        if memory[i] < 0 and abs(memory[i]) >= size:

            # Calculate how much space is left after allocation
            remaining = abs(memory[i]) - size

            # Replace the hole with the allocated block (positive number)
            memory[i] = size

            # If there is leftover space, create a new hole
            if remaining > 0:
                memory.insert(i + 1, -remaining)

            # Allocation successful
            return True

    # If no hole was large enough
    return False


# TESTING THE FUNCTION

print("Before allocation:", memory)

# Try to allocate a block of size 20
success = first_fit(memory, 20)

print("Allocation success:", success)
print("After allocation:", memory)

# -------------------------------
# NEXT-FIT ALLOCATION FUNCTION
# -------------------------------

def next_fit(memory, size, last_index):
    """
    Next-Fit = continue searching from the last position used

    Parameters:
    memory -> memory list
    size -> requested block size
    last_index -> index where the last successful allocation happened

    Returns:
    (success, new_last_index)
    """

    # If memory list is empty, allocation fails
    if len(memory) == 0:
        return False, 0

    # Make sure last_index is always inside valid bounds
    last_index = last_index % len(memory)

    # Start searching from last_index
    i = last_index
    checked = 0

    # Check each block at most once
    while checked < len(memory):

        # If this block is a hole and big enough, allocate here
        if memory[i] < 0 and abs(memory[i]) >= size:
            remaining = abs(memory[i]) - size

            # Replace hole with allocated block
            memory[i] = size

            # If space is left, insert a new hole after it
            if remaining > 0:
                memory.insert(i + 1, -remaining)

            # Return success and remember this position
            return True, i

        # Move forward circularly
        i = (i + 1) % len(memory)
        checked += 1

    # No hole was large enough
    return False, last_index
print("\n--- Testing Next-Fit ---")

memory = [-100]
last_index = 0

print("Before:", memory)

success, last_index = next_fit(memory, 30, last_index)

print("Success:", success)
print("After:", memory)

# -------------------------------
# BEST-FIT ALLOCATION FUNCTION
# -------------------------------

def best_fit(memory, size):
    """
    Best-Fit = find the SMALLEST hole that fits
    """

    best_index = -1
    smallest_size = float('inf')  # start with very large number

    # Find best hole
    for i in range(len(memory)):
        if memory[i] < 0:
            hole_size = abs(memory[i])

            # Check if it fits AND is smaller than current best
            if hole_size >= size and hole_size < smallest_size:
                smallest_size = hole_size
                best_index = i

    # If no hole found
    if best_index == -1:
        return False

    # Allocate memory
    remaining = abs(memory[best_index]) - size
    memory[best_index] = size

    if remaining > 0:
        memory.insert(best_index + 1, -remaining)

    return True

print("\n--- Testing Best-Fit ---")

memory = [10, -60, -20, -40]

print("Before:", memory)

success = best_fit(memory, 35)

print("Success:", success)
print("After:", memory)

import random  # used to choose a random allocated block to release

# -------------------------------
# MERGE NEIGHBORING HOLES
# -------------------------------

def merge_holes(memory):
    """
    Combine neighboring negative blocks into one larger hole.
    Example: [-10, -15] becomes [-25]
    """
    i = 0

    # Go through the memory list
    while i < len(memory) - 1:

        # If current block and next block are both holes
        if memory[i] < 0 and memory[i + 1] < 0:
            # Merge them into one bigger hole
            memory[i] = memory[i] + memory[i + 1]

            # Remove the next block since it was merged
            memory.pop(i + 1)

        else:
            # Move to the next position
            i += 1


# -------------------------------
# RELEASE A RANDOM ALLOCATED BLOCK
# -------------------------------

def release_block(memory):
    """
    Pick one allocated block at random, free it,
    then merge neighboring holes.
    
    Returns:
    True if a block was released
    False if there were no allocated blocks
    """

    # Find indexes of all allocated blocks (positive numbers)
    allocated_indexes = []

    for i in range(len(memory)):
        if memory[i] > 0:
            allocated_indexes.append(i)

    # If there are no allocated blocks, nothing to release
    if len(allocated_indexes) == 0:
        return False

    # Randomly choose one allocated block
    chosen_index = random.choice(allocated_indexes)

    # Turn it into a hole by making it negative
    memory[chosen_index] = -memory[chosen_index]

    # Merge neighboring holes
    merge_holes(memory)

    return True

print("\n--- Testing Release + Merge ---")

memory = [20, -10, 15, -5]

print("Before release:", memory)

success = release_block(memory)

print("Release success:", success)
print("After release:", memory)

import time
import random

# -------------------------------
# SIMULATION FUNCTION
# -------------------------------

def simulate(strategy_func, memory_size=100, iterations=50):
    """
    Runs the memory allocation simulation.

    strategy_func -> allocation method to use
    memory_size -> total memory size
    iterations -> number of release/reallocate cycles
    """

    memory = [-memory_size]   # start with one big free hole
    total_utilization = 0
    last_index = 0            # used only for next-fit

    # First fill memory until allocation fails
    while True:
        request_size = random.randint(5, 20)

        if strategy_func == next_fit:
            success, last_index = next_fit(memory, request_size, last_index)
        else:
            success = strategy_func(memory, request_size)

        if not success:
            break

    start_time = time.time()

    # Repeat for a number of iterations
    for _ in range(iterations):

        # Release one random allocated block
        release_block(memory)

        # Keep allocating until one request fails
        while True:
            request_size = random.randint(5, 20)

            if strategy_func == next_fit:
                success, last_index = next_fit(memory, request_size, last_index)
            else:
                success = strategy_func(memory, request_size)

            if not success:
                break

        # Compute memory utilization
        used = sum(block for block in memory if block > 0)
        utilization = used / memory_size
        total_utilization += utilization

    end_time = time.time()

    avg_utilization = total_utilization / iterations
    runtime = end_time - start_time

    return avg_utilization, runtime

    print("\n--- Running Full Simulation ---")

last_index = 0

ff_util, ff_time = simulate(first_fit)
nf_util, nf_time = simulate(next_fit)
bf_util, bf_time = simulate(best_fit)

print("\nResults:")
print(f"First-fit -> Utilization: {ff_util:.2f}, Time: {ff_time:.4f}s")
print(f"Next-fit -> Utilization: {nf_util:.2f}, Time: {nf_time:.4f}s")
print(f"Best-fit -> Utilization: {bf_util:.2f}, Time: {bf_time:.4f}s")