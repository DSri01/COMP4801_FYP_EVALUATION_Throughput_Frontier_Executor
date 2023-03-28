"""
FYP : 22013

Module:
    Throughput Frontier Executor

Description:
    This python script contains the definition of the Logger class that logs the
    benchmarking events in a log file.
"""


class Logger:

    def __init__(self, log_file_name):
        self.file_pointer = open(log_file_name, "w")

    def log(self,message):
        self.file_pointer.write(message + '\n')

    def close_log(self,):
        self.file_pointer.close()
