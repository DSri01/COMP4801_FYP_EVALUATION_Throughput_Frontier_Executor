# COMP4801_FYP_EVALUATION_Throughput_Frontier_Executor

## FYP: 22013

### FYP Team

**Student:** SRIVASTAVA Dhruv (3035667792)

**Supervisor:** Dr. Heming Cui

## Description

Throughput Frontier Executor for the evaluation phase of HTAP Graph Database
System Benchmark development. This module controls the execution of the *System Under Test* (Server Skeleton SUT), *Data Loader*, and *Hybrid Query Driver* to perform experiments
to find the throughput frontier of the SUT.

Since the SUT was an in-memory database system, exiting the program
effectively resets the SUT.

## Usage Instructions

Fill in the configuration details in ```build_config.py``` and execute it to
generate a configuration file for the Throughput Frontier Executor. Finally,
execute the executor by running:

```python3 EEM000_main.py <JSON configuration file>```

For simplicity of implementation and prevention of early-stopping due to unexpected
load on the hardware, this Throughput Frontier Executor does not look at the output
of the query driver to early-stop in case of decreasing performance. The executor
probes the throughputs for each value of the analytical-transactional thread number
pairs present in the probe thread numbers provided in the configuration.

The current implementation also assumes that the query driver and data loader
are stored in the ```benchmark-driver``` and ```bulk-loader``` folders respectively,
with the base data from the Base Data Generator stored in the ```Data``` folder.

The ```benchmark-driver``` and ```bulk-loader``` folders also contain the shell
scripts, which the executor executes to start executing the respective component.

The benchmarking results appear as appended data in the query driver output file as
specified in ```benchmark-driver/execute-driver.sh```.

## Module Components Description

| File Name | Description |
|-----------|-------------|
|EEM000_main.py|Script to schedule execution of all benchmark components and SUT to do *Throughput Frontier* related operations|
|EEM0001_util.py|Contains the utility functions used by the main executor to schedule the execution of benchmark components and the SUT|
|EEM002_logger.py|Logs the output of the executor in a log file|
|build_config.py|Builds the JSON configuration file for the executor|