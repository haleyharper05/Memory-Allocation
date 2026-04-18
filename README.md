# Memory Allocation Simulator

## Course Information
- COMP 3306 Operating Systems
-  Spring 2026
-  Dr. Mary Kim

## Group Members
- Haley Harper - Project Leader
- Raylen Williams - Algorithm Researcher
- Nyla Mason - Lead Programmer
- Tayla Scott - Tester / QA
- James McGrone - Debugger / Optimization
- Kiva Williams - Documentation

## Project Objective
The objective of this project is to compare the performance of three memory allocation strategies used in operating systems:
- First-Fit
- Next-Fit
- Best-Fit

The program simulates a sequence of memory request and release operations and measures how efficiently each strategy uses memory.

## Project Description
In this simulation, memory is represented as a list of blocks:
- **Positive numbers** represent allocated memory blocks
- **Negative numbers** represent free holes

Example:
python
[20, -30, 15, -10]

## Debugging Note

An issue occurred in the Next-Fit implementation where an index went out of range after memory changes. This was resolved by ensuring the saved index always stayed within valid bounds.
