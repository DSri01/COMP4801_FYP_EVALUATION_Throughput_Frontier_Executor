"""
FYP : 22013

Module:
    Throughput Frontier Executor

Description:
    This python script contains function definitions that allow the main executor
    to perform experimentation.
"""

# Imports from built-in modules
import json
import socket
import subprocess
import threading
import time

# Imports from Throughput Frontier Executor Module
from EEM002_logger import Logger

# Stops the Server Skeleton remote server
def stop_server(IP_ADDRESS, PORT_NUMBER, logger):
    dict = {}
    dict["OPERATION_ID"] = 30

    socket_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_to_server.connect((IP_ADDRESS, PORT_NUMBER))

    message = json.dumps(dict) + '|'
    socket_to_server.sendall(message.encode('ascii'))

    logger.log("SERVER TERMINTAION SIGNAL SENT")
    time.sleep(10)


# Starts the Server Skeleton remote server and is blocked
def start_remote_server(IP_ADDRESS, logger):
    subprocess.run(['ssh', IP_ADDRESS, "./LiveGraph/LiveGraph-SS/execute-server.sh"])
    logger.log("REMOTE SERVER STOPPED")

# Starts the Server Skeleton remote server in a new thread, which remains blocked until the Server Skeleton finishes execution
def start_server(IP_ADDRESS, logger):
    start_remote_server_thread = threading.Thread(target=start_remote_server, args=(IP_ADDRESS, logger))
    start_remote_server_thread.start()
    time.sleep(10)
    logger.log("STARTED REMOTE SERVER")

# Changes the thread numbers in the query driver configuration file
def change_benchmark_driver_thread_numbers(benchmark_config_file_name, new_analytical_thread_number, new_transactional_thread_number, logger):
    current_data = ""
    with open(benchmark_config_file_name, "r") as read_fp:
        current_data = read_fp.read()
        current_data = json.loads(current_data)
        read_fp.close()

    current_data["number_of_analytical_threads"] = new_analytical_thread_number
    current_data["number_of_transactional_threads"] = new_transactional_thread_number

    with open(benchmark_config_file_name, "w") as write_fp:
        write_fp.write(json.dumps(current_data))
        write_fp.close()
    log_message = "Benchmark configuration changed to A: " + str(new_analytical_thread_number) + "| T: " + str(new_transactional_thread_number)
    logger.log(log_message)

# Executes the data loader to load data to the Server Skeleton
def bulk_load_data(bulk_loader_command, bulk_loader_working_directory, logger):
    logger.log("Bulkloader Execution Started")
    subprocess.run(bulk_loader_command, cwd = bulk_loader_working_directory)
    logger.log("Bulkloader Execution FINISHED")

# Executes the query driver to run the experiment
def run_benchmark(benchmark_command, benchmark_working_directory, logger):
    logger.log("Benchmark Execution Started")
    subprocess.run(benchmark_command, cwd = benchmark_working_directory)
    logger.log("Benchmark Execution Finished")

# Changes the IP Address of the Server Skeleton in the Data Loader and Quer Driver configuration files
def change_benchmark_IP(IP_ADDRESS, driver_config_file_name, bulk_loader_config_file_name, logger):
    current_config = ""
    with open(driver_config_file_name, "r") as read_fp:
        current_config = read_fp.read()
        current_config = json.loads(current_config)
        read_fp.close()

    current_config["IP_ADDRESS"] = IP_ADDRESS

    with open(driver_config_file_name, "w") as write_fp:
        write_fp.write(json.dumps(current_config))
        write_fp.close()

    current_config = ""
    with open(bulk_loader_config_file_name, "r") as read_fp:
        current_config = read_fp.read()
        current_config = json.loads(current_config)
        read_fp.close()

    current_config["IP_ADDRESS"] = IP_ADDRESS

    with open(bulk_loader_config_file_name, "w") as write_fp:
        write_fp.write(json.dumps(current_config))
        write_fp.close()

    log_message = "Benchmark configuration changed IP ADDRESS to: " + IP_ADDRESS
    logger.log(log_message)

# Changes the benchmarking mode in the query driver configuration file
def change_benchmark_mode(benchmark_mode, is_freshness_score_enabled, driver_config_file_name, logger):
    current_config = ""
    with open(driver_config_file_name, "r") as read_fp:
        current_config = read_fp.read()
        current_config = json.loads(current_config)
        read_fp.close()

    current_config["enable_freshness_score"] = is_freshness_score_enabled
    current_config["experiment_mode"] = benchmark_mode

    with open(driver_config_file_name, "w") as write_fp:
        write_fp.write(json.dumps(current_config))
        write_fp.close()
    log_message = "Benchmark configuration mode changed to : "  + benchmark_mode + "FRESHNESS SCORE?: "+str(is_freshness_score_enabled)
    logger.log(log_message)
