#4.6 BANKING OOP README

There are 3 main files uploaded and used in the course of this project:
  1. Banking_Projectv2.py -  This is where the main file/code is located. All classes and functions are held and run from this file.
  2. PreStage_Banking_Information.txt - This is where the data storage is located. For the purposes of this project, I am using JSON as my storage system.
  3. test.log - This is where I ran my debugger and used to identify any issues during testing that the file may have encountered. Not necessary to run the code.
 
**INTRODUCTION - RUNNING THE FILE**
As per the instructions outlined at the start of the project, my implementation uses JSON as the main storage system. When running the file in the terminal, the file should automatically request user information to determine whether or not they are held within the PreStage_Banking_Information.txt. The first initial user inputs will be your first name, last name, and date of birth. These will be stored as variables and stored as a key within the JSON dictionary to pull relevant information related to the user. When an instantiation ends, all the information collected during current script will be stored within the JSON file and can be retrieved when you rerun the program again.
