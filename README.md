# cadmium2_testing_framework

## About The Project

This testing framework is designed to make the process of testing DEVS Atomic models semi-automated by generating test drivers and utilizing
chatgpt to create test cases.

## Built With

* Boost<span>.</span>org
* CMake
* SimulationEverywhere/Cadmium2
* json

## Prerequisites

## Important Notes

* Generating test files, you must cofigure your build targets manually as there are no generated files that can set up your targets (yet).
* When you build your executables from your test drivers, make sure to have your current working drictory in the folder where all of your drivers are located.
  This is so the driver can find the log files for reading.
* Be nice to ChatGPT. If it does not generate data to your liking based off of the provided JSON template (see examples for JSON model file examples) then
  it may help to make your state variables or port names more meaningful. It also may help if you are using custom data types for ports or functions in the model, to add small comments after ;'s incase a statement or variable is confusing the AI. 

## User Manual

