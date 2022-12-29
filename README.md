# Mu2e CRV Tester
## Table of Contents
* [Overview](#overview)
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Running the code](#running-the-code)
## Overview 
This project uses Python to code motherboards for Mu2e 
## General info 
The motherboards used all have 4 FPGA chips, each with their own 16 DAC channels. The boards register is written in hexadecimal and the Python code mainly focuses on the bias voltages/buses displayed between 0x300 and 0x3FF. 
## Technologies 
This Project was created with:
* Geany 
* PuTTY
* Command Prompt 
* Python version: 3.9.13
## Setup 
To run this project open command prompt and navigate to the desired file you would like to put the code in,
exp. C:\Users\user\folder-name. Once sucessfully done copy and past this code into the command line.
`git clone https://github.com/zacharyeisenhutt/Mu2e-CRV-Tester.git`
This will clone a copy of every file you will need into the file you chose.
If you would like to check your work at this point, in the command line type `dir` and hit enter, what should pop up is the Mu2e-CRV-Tester file.
Now all you have to do is type `cd Mu2e-CRV-Tester` into the command line and press enter.
You should sucessfully be in the folder Mu2e CRV Tester that contains all of the code for this project. 
## Running the code 


