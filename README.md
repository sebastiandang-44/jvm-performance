# JVM Logging Project
## Inside OpenJDK and the HotSpot Java Virtual Machine



JVM Performance Engineering is a deep dive into the world of Java Virtual Machine (JVM) performance, specifically focusing on the OpenJDK HotSpot VM. 

## Repository Contents

### Overview

This directory contains various Python scripts for parsing and visualizing Java GC logs. Each script provides different insights into Java's Garbage Collection (GC) behavior, allowing developers to understand and optimize the performance of their applications.

### Available Scripts

### heap_plotter.py 

Enhanced script for visualizing Java GC logs with comprehensive G1 time-based heap sizing analysis. Supports traditional GC analysis plus advanced G1 sizing activity visualizations. Features modern log format support, interactive dashboards, and backward compatibility.

### zstd_decompressed.py

Decompress the event log from Spark App and create pyplot server that focus on CPU utilization 
Total Job Execution Time (ms) - Measures the overall time taken for a Spark job to complete
Stage Execution Time (ms) - Shows the time spent in individual Spark stages
Task Duration (avg / max) - Indicates average and maximum task execution time

<img width="1611" height="176" alt="image" src="https://github.com/user-attachments/assets/61582e70-def1-41ef-b30e-5a71c54c7eb8" /># JVM Logging Project


### Sample Log
`driver.gc.log `
`event-app.zstd` in zstandard compresssion format

### Technical Stacks

<img alt="image" src="![docker](https://github.com/user-attachments/assets/9b0ac6f1-8a5f-4e5f-aa7d-1950ffdd6395)/>


