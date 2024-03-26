import math
import random

queue_limit = 100
busy = 1
idle = 0

# Global variables
mean_interarrival = 0
mean_service = 0
num_delays_required = 0
clock = 0
server_status = idle
num_in_q = 0
time_last_event = 0.0
total_of_delays = 0.0
area_num_in_q = 0.0
area_server_status = 0.0
time_next_event = [0.0] * 3  # Corrected initialization
num_custs_delayed = 0
next_event_type = 0

# Function to initialize simulation parameters
def initialize():
    global clock, server_status, num_in_q, time_last_event, time_next_event, num_custs_delayed, total_of_delays, area_num_in_q, area_server_status
    clock = 0
    server_status = idle
    num_in_q = 0
    time_last_event = 0.0
    num_custs_delayed = 0
    total_of_delays = 0.0
    area_num_in_q = 0.0
    area_server_status = 0.0
    time_next_event = [0.0] * 3
    time_next_event[1] = clock + expon(mean_interarrival)
    time_next_event[2] = 1.0e+30

# Advance the simulation clock to the next event
def timing():
    global clock, time_next_event, next_event_type
    min_time_next_event = min(time_next_event[1], time_next_event[2])
    next_event_type = time_next_event.index(min_time_next_event)
    clock = min_time_next_event

# Arrival of customers
def arrive():
    global clock, server_status, num_in_q, total_of_delays, num_custs_delayed
    time_next_event[1] = clock + expon(mean_interarrival)
    if server_status == busy:
        num_in_q += 1
        if num_in_q > queue_limit:
            print("\nOverflow of the array time_arrival at", clock)
            exit(2)
    else:
        delay = 0.0
        total_of_delays += delay
        num_custs_delayed += 1
        server_status = busy
        time_next_event[2] = clock + expon(mean_service)

# Departure of customers
def depart():
    global clock, server_status, num_in_q, total_of_delays, num_custs_delayed
    if num_in_q == 0:
        server_status = idle
        time_next_event[2] = 1.0e+30
    else:
        num_in_q -= 1
        delay = 0  # Corrected delay calculation
        total_of_delays += delay
        num_custs_delayed += 1
        time_next_event[2] = clock + expon(mean_service)

def report():
    global total_of_delays, num_custs_delayed, clock, area_num_in_q, area_server_status
    with open(r"C:\Users\hp\Desktop\single-server-queueing-system\mm1.out", "w") as outfile:
        outfile.write("Single server queuing system\n\n")
        outfile.write("Mean interarrival time%11.3f minutes\n\n" % mean_interarrival)
        outfile.write("Mean service time%16.3f minutes\n\n" % mean_service)
        outfile.write("Number of customers%14d\n\n" % num_delays_required)
        outfile.write("Average delay in queue%11.3f minutes\n\n" % (total_of_delays / num_custs_delayed))
        outfile.write("Averge number in queue%10.3f\n\n" % (area_num_in_q / clock))
        outfile.write("Server utilization%15.3f\n\n" % (area_server_status / clock))
        outfile.write("Time simulation ended%12.3f minutes" % clock)

def update_time_avg_stats():
    global clock, area_num_in_q, area_server_status, time_last_event
    time_since_last_event = clock - time_last_event
    time_last_event = clock
    area_num_in_q += num_in_q * time_since_last_event
    area_server_status += server_status * time_since_last_event

# Generate exponential random variables
def expon(mean):
    return -mean * math.log(random.random())

# Reading input from file
with open(r"C:\Users\hp\Desktop\single-server-queueing-system\mm1.in", "r") as infile:
    mean_interarrival, mean_service, num_delays_required = map(float, infile.readline().split())

initialize()

# Running the simulation until required number of customers are served
while num_custs_delayed < num_delays_required:
    timing()
    update_time_avg_stats()
    if next_event_type == 1:
        arrive()
    elif next_event_type == 2:
        depart()

report()
