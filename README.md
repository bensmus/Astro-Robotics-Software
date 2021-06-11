# Astro Robotics Software

*Feel free to modify this file.*

Welcome to everything software related at Astro Robotics!

## Goals
- Currently working towards wayfinding, which requires a drivetrain and an ultrasonic sensor
> Wayfinding: The rover must go from point A to B, along rough terrain. The rovers/teams ability to pick the best path, and handle obstacles is important.
- Wayfinding does not include picking up any objects, everything is an obstacle for now. 

## Firmware tasks
- Writing code for non-autonomous motors control
    - Functions for driving forward, turning, etc. 
- Interfacing with game controller:
    - Mapping the buttons to different tasks, maybe have different control profiles.
- Outputting various robot data on an LCD screen:
    - Sensor data, robot state data.
        - Battery life
        - GPS location
        - States of all the motors
        - Readings of all the sensors
    - Have some sort of UI for selecting what sort of data you want to display.
        - Buttons? Dials?

## Wayfinding tasks
- Obstacle detection with ultrasonic sensor.
- Creating a live map of obstacles and planning a route around them. <-- pure CS, no roadblocks
    - http://www.cs.columbia.edu/~allen/F17/NOTES/lozanogrown.pdf
- Giving motor control instructions based on the planned route.

## Unknowns 
- Need more information about the rover:
    - What motors will be used?
    - What will be the sizes of the wheels?
    - Will it be powered by an Arduino AND a Raspberry Pi?
