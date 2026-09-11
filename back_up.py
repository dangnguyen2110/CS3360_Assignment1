#!/usr/bin/env python3
"""
CS 3360: Computing Systems Fundamentals
Reference Solution: Synthetic Process Workload Generation and Simulation
"""
import math
import random

class Process:
    def __init__(self, pid, arrival_time, service_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.service_time = service_time
        self.state = "NEW"
        self.start_time = None
        self.end_time = None

def generate_processes(num_processes = 1000, lambda_per_ms = 2.0, T_ms = 1.0):
    # Hardcoded process list matching the assignment example
    processes = []
    current_arrival_time = 0
    
    for i in range(1, num_processes + 1):
        if i == 1:
            inter_arrival_ms = 0
        else:
            u1 = random.random()
            while u1 == 0:
                u1 = random.random() #Prevent log(0)
            inter_arrival_ms = round(-math.log(u1) / lambda_per_ms)
           
        current_arrival_time += inter_arrival_ms   
        
        u2 = random.random()
        while u2 == 0:
            u2 = random.random() #Prevent log(0)
        service_time_ms = round(-T_ms * math.log(u2))
        
        if service_time_ms == 0:
            service_time_ms = 1 #ensure service time at least 1ms

        # Initialize Process objects
        p = Process(pid = i, arrival_time = current_arrival_time, service_time = service_time_ms)
        processes.append(p)
    return processes

def print_workload(processes):
    # Output formatted list of tuples
    print("**Process Workload**\n")
    print("process_id | arrival_time | requested_service_time")
    for p in processes[:15]:
        print(f"{p.pid:<10} | {p.arrival_time:<12} | {p.service_time}")
    print("\n")

def run_fifo_simulation(processes):
    print("**CPU Simulation Trace**\n")
    print("Time (in ms) | CPU Status | PID")

    # Construct the trace table using a loop
    current_time = 0
    for p in processes:
        # Check for gaps between processes to print IDLE states
        if current_time < p.arrival_time:
            print(f"[{current_time:4d},{p.arrival_time:5d}) | {'IDLE':<10} |  ")
            current_time = p.arrival_time
            
        p.start_time = current_time
        p.end_time = p.start_time + p.service_time
        
        # Print the BUSY state for the process
        print(f"[{p.start_time:4d},{p.end_time:5d}) | {'BUSY':<10} | {p.pid}")
        current_time = p.end_time

    print("\n")

def calculate_statistic(processes):
    last_arrival_time = processes[-1].arrival_time
    computed_arrival_time = len(processes) / last_arrival_time
    
    total_service_time = sum(p.service_time for p in processes)
    computed_service_time = total_service_time / len(processes)
    
    #Output Generated Averages Comparison 
    print("**Generation Statistics**\n")
    print("Statistics                    | Results")
    print("------------------------------|-----------------")
    print("Expected Average Arrival Rate | 2.0 processes per ms")
    print(f"Computed Average Arrival Rate | {computed_arrival_time:.2f} processes per ms")
    print("Expected Average Service Time | 1.0 ms")
    print(f"Computed Average Service Time | {computed_service_time:.2f} ms")
    print("\n")

    total_complete_time = processes[-1].end_time
    total_turnaround_time = sum(p.end_time - p.arrival_time for p in processes)
    total_waiting_time = sum(p.start_time - p.arrival_time for p in processes)
        
    average_turnaround_time = total_turnaround_time / len(processes)
    average_waiting_time = total_waiting_time / len(processes)
    overall_cpu_ultilization = (total_service_time / total_complete_time) * 100
    overall_system_throughput = len(processes) / total_complete_time
    
    # Output Final Statistics Table in the requested vertical format
    print("**Simulation Statistics**\n")
    print("Statistics                    | Results")
    print("------------------------------|-----------------")
    print(f"Total Complete Time           | {total_complete_time:.2f}ms")
    print(f"Average Turnaround Time       | {average_turnaround_time:.2f}ms")
    print(f"Average Waiting Time          | {average_waiting_time:.2f}ms")
    print(f"Overall CPU utilization       | {overall_cpu_ultilization:.2f}%")
    print(f"Overall System Throughput     | {overall_system_throughput:.2f} processes/ms")
    print("\n")    

def main():
    # Combine generation and simulation phases
    processes = generate_processes()
    print_workload(processes)
    run_fifo_simulation(processes)
    calculate_statistic(processes)

if __name__ == "__main__":
    main()
