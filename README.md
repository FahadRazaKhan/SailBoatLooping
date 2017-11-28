# SailBoatLooping
This Program is used to make Autonomous Zig-Zag Looping of Hybrid SailBoat.

This program is for performing continous Autonomous loops (Open-loop) of a
Hybrid Sailboat. It also measures and then stores the Current Sensor (INA-219) values in
an XLSX file. Looping and Current measuring functions run on two different threads
simultaneously.

Looping_Server.py file runs on board (RPi) and Looping+Sensor.py file runs on client (PC/Laptop/Tablet).
