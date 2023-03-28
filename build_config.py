"""
FYP : 22013

Module:
    Throughput Frontier Executor

Description:
    This python script is a supporting script to generate the JSON configuration
    file for the Throughput Frontier Executor.
"""

import json
import sys

configs = {}

configs["LOG_FILE_NAME"] = "log.txt"
configs["SUT_SERVER_IP"] = '127.0.0.1'
configs["SUT_SERVER_PORT#"] = 12560

# Define the start and end thread number for the transactional thread number probe
configs["TRANSACTIONAL_PROBE_START_THREAD_NUBMER"] = 1
configs["TRANSACTIONAL_PROBE_END_THREAD_NUBMER"] = 2

# Define the start and end thread number for the analytical thread number probe
configs["ANALYTICAL_PROBE_START_THREAD_NUBMER"] = 1
configs["ANALYTICAL_PROBE_END_THREAD_NUBMER"] = 2

# Specify the mode of benchmarking
configs["BENCHMARK_MODE"] = "HYBRID"

# Specify if freshness score data is collected
configs["ENABLE_FRESHNESS_SCORE_COLLECTION"] = True

# It is recommended that the freshness score data collection is disabled when probing for Throughput Frontier

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage:", sys.argv[0],"<destination JSON file name>")
    else:
        with open(sys.argv[1], 'w') as file:
            file.write(json.dumps(configs))
            file.close()
