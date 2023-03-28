"""
FYP : 22013

Module:
    Throughput Frontier Executor

Description:
    This python script schedules the execution of the benchmark components and
    the Server Skeleton System Under Test (SUT) to compute the Throughput Frontier.
"""

# Imports from built-in modules
import json
import sys

# Imports from Throughput Frontier Executor Module
import EEM001_util as UTIL
from EEM002_logger import Logger


def start_benchmarking(configs):
    logger = Logger(configs["LOG_FILE_NAME"])
    UTIL.change_benchmark_IP(configs["SUT_SERVER_IP"], "benchmark-driver/DRIVER-CONFIG.json", "bulk-loader/BDL005_config_file.json",logger)
    UTIL.change_benchmark_mode(configs["BENCHMARK_MODE"], configs["ENABLE_FRESHNESS_SCORE_COLLECTION"], "benchmark-driver/DRIVER-CONFIG.json",logger)

    if (configs["BENCHMARK_MODE"] == "TRANSACTIONAL"):
        for i in range(configs["TRANSACTIONAL_PROBE_START_THREAD_NUBMER"], configs["TRANSACTIONAL_PROBE_END_THREAD_NUBMER"]+1):
            UTIL.start_server(configs["SUT_SERVER_IP"], logger)
            UTIL.change_benchmark_driver_thread_numbers("benchmark-driver/DRIVER-CONFIG.json", 1, i, logger)
            UTIL.bulk_load_data('./execute-bulkloader.sh', 'bulk-loader/', logger)
            UTIL.run_benchmark('./execute-driver.sh', "benchmark-driver/", logger)
            UTIL.stop_server(configs["SUT_SERVER_IP"], configs["SUT_SERVER_PORT#"], logger)

    elif (configs["BENCHMARK_MODE"] == "ANALYTICAL"):
        for i in range(configs["ANALYTICAL_PROBE_START_THREAD_NUBMER"], configs["ANALYTICAL_PROBE_END_THREAD_NUBMER"]+1):
            UTIL.start_server(configs["SUT_SERVER_IP"], logger)
            UTIL.change_benchmark_driver_thread_numbers("benchmark-driver/DRIVER-CONFIG.json", i, 1, logger)
            UTIL.bulk_load_data('./execute-bulkloader.sh', 'bulk-loader/', logger)
            UTIL.run_benchmark('./execute-driver.sh', "benchmark-driver/", logger)
            UTIL.stop_server(configs["SUT_SERVER_IP"], configs["SUT_SERVER_PORT#"], logger)

    else:
        for i in range(configs["ANALYTICAL_PROBE_START_THREAD_NUBMER"], configs["ANALYTICAL_PROBE_END_THREAD_NUBMER"]+1):
            for j in range(configs["TRANSACTIONAL_PROBE_START_THREAD_NUBMER"], configs["TRANSACTIONAL_PROBE_END_THREAD_NUBMER"]+1):
                UTIL.start_server(configs["SUT_SERVER_IP"], logger)
                UTIL.change_benchmark_driver_thread_numbers("benchmark-driver/DRIVER-CONFIG.json", i, j, logger)
                UTIL.bulk_load_data('./execute-bulkloader.sh', 'bulk-loader/', logger)
                UTIL.run_benchmark('./execute-driver.sh', "benchmark-driver/", logger)
                UTIL.stop_server(configs["SUT_SERVER_IP"], configs["SUT_SERVER_PORT#"], logger)

    logger.close_log()

if __name__ == '__main__':
    if len(sys.argv) == 2:
        with open(sys.argv[1], "r") as config_fp:
            configs = config_fp.read()
            config_dict = json.loads(configs)
            start_benchmarking(config_dict)
            config_fp.close()
    else:
        print("USAGE:", sys.argv[0], "<JSON CONFIG FILE>")
