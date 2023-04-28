# Mu2e CRV Tester
## Table of Contents
* [Overview](#overview)
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Running the code](#running-the-code)
## Overview 
This project uses Python to code FEB(Front End Boards) for the Mu2e project. 
## General info 
The FEB utilizes 4 FPGA chips where each chip contains 16 DAC channels, 2 AFE chips, and 16 SIPMs. The FEB register is written in hexadecimal and the Python code mainly focuses on the bias voltages/buses displayed between 0x300 and 0x3FF as well as histogram functions that utilize the AFE chips and SIPMs in the FPGA chips. 
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
When you are in the current directory Mu2e CRV Tester on Command Prompt type `py` and press enter to open python. Make sure that python is version 3.0 or higher, *your version will be displayed once you hit enter.*

***The code will not work depending on what version of python you are running it on, check that your version is compatible.***

In the command line type `from run_code import s, feb, tst` this will pull the sockexpect, feb connection, and test variables, from the run_code.py file.
These variables will be used as arguments needed for the tests.
Once you have imported those variables you will need to put tst. infront of what you are trying to run.

***exp.*** 

If we want to test the ADC we can look and see it has an feb_connection argument so I would,

Input `tst.test_ADC(feb)` in the comand line. 

Output  
 `**** This is the expected voltage 1.2 , This is the actual voltage 1.2 ,This is the error 0.0 % !!!!
 
 **** This is the expected voltage 1.8 , This is the actual voltage 1.8 ,This is the error 0.0 % !!!!
 
 **** This is the expected voltage 5.0 , This is the actual voltage 5.0 ,This is the error 0.0 % !!!!
 
 **** This is the expected voltage 10 , This is the actual voltage 9.82 ,This is the error 1.7999999999999972 % !!!!
 
 **** This is the expected voltage 2.5 , This is the actual voltage 2.5 ,This is the error 0.0 % !!!!
 
 **** This is the expected voltage 5.0 , This is the actual voltage 4.99 ,This is the error 0.19999999999999576 % !!!!
 
 **** This is the expected voltage 15 , This is the actual voltage 15.02 ,This is the error -0.1333333333333305 % !!!!
 
 **** This is the expected voltage 3.3 , This is the actual voltage 3.35 ,This is the error -1.5151515151515234 % !!!!
 
 **** Tbe bias volatge is 0.11  !!!!
 
 **** Tbe bias volatge is 0.11  !!!!
 
 **** Tbe bias volatge is 0.17  !!!!
 
 **** Tbe bias volatge is 0.53  !!!!
 
 **** Tbe bias volatge is 0.11  !!!!
 
 **** Tbe bias volatge is 0.42  !!!!
 
 **** Tbe bias volatge is 0.63  !!!!
 
 **** Tbe bias volatge is 0.11  !!!!
 
 **** The temperature is 24.44 degC !!!!`

For tests that use the FPGA chips or DAC channels make sure you use the desired FPGA and DAC numbers in the arguments.

***IF A TEST REQUIRES AN FPGA ARGUMENT, BEFORE THE TEST ALWAYS ZERO THE VOLTAGES ON THE FPGA CHIP(S). THIS IS DONE BY INPUTING `tst.zero_all_bias(s,FPGA#)`, YOU WILL KNOW IF YOU DID THIS CORRECTLY BY A 4 SECOND RUN TIME THAT HAS NO OUTPUT***

For any final questions or insights into the board, click the link below to see the boards register  

[CRV_FEB_Regs.docx](https://github.com/zacharyeisenhutt/Mu2e-CRV-Tester/files/10322233/CRV_FEB_Regs.4.docx)


