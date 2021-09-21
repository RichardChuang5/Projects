![image](https://user-images.githubusercontent.com/80606434/134219834-d7ee3046-9b08-4195-8cb5-f89c7d7a79b4.png)

This overview is to provide a rundown of how to use and run a Hadoop job to breakdown various key value pairs within a dataset using Python.

### Step 1 - Setting up Hadoop
Download Hadoop from the Apache website and follow the steps outlined here: 

https://www.datasciencecentral.com/profiles/blogs/how-to-install-and-run-hadoop-on-windows-for-beginners

Additionally, follow the instructions outlined in this youtube video in order to download the virtual box/sandbox from Hortonworks: 

https://www.youtube.com/watch?v=735yx2Eak48&ab_channel=BinodSumanAcademy

Note: The instructions per the first link require some additional editing. Within the core-site.XML file, where it requires the dfs endpoint locator, I had to remove 'localhost:9000' and replace it with '[my computer name]:[my IP address]'. This allowed the namenode and data node to run properly. I also needed to run the hortonworks sandbox in parallel with my CMD terminal

![image](https://user-images.githubusercontent.com/80606434/126086634-55ef24c3-9f6a-4f4b-bb22-7ac2711e014d.png)


### Step 2 - Useful commands to know
Using the CMD terminal, the following commands are useful:
1. Not so much a command, but when you first open the CMD terminal, you need to navigate to your sbin folder within hadoop. From there, execute the start-all.cmd which will allow you to run namenode, datanode, resourcemanager, and namenodemanager.
2. jps: This commands lets you know what nodes are up and running. Ideally, you should have name node, data node, resource manager, and node manager up and running.
3. hadoop fs -ls /: Shows the contents within the root directory. The '/' is mandatory, otherwise it does not read properly. 
4. hadoop fs -put '[file directory] [location you want to place the file]'. Ultimately for me, this looked like hadoop fs -put C:/Users/Squarebear/Python/Projects/Hadoop/data.csv /input_dir

To execute the Python command via Windows-
type data.csv|python first_mapper.py|python first_reducer.py|python second_mapper.py|python second_reducer.py

To execute via MACOS replace type with cat.

Note: Run the final Hadoop job through 'report'
I had to execute the final Hadoop project from a different computer running MACOS, hence the username defined in the Hadoop CLI and report.sh file are different.
