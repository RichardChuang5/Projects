# HADOOP
This overview is to provide a rundown of how to use Hadoop on a Windows machine.

### Step 1 - Setting up Hadoop
Download Hadoop from the Apache website and follow the steps outlined here: 
https://www.datasciencecentral.com/profiles/blogs/how-to-install-and-run-hadoop-on-windows-for-beginners
Additionally, follow the instructions outlined in this youtube video in order to download the virtual box/sandbox from Hortonworks: 
https://www.youtube.com/watch?v=735yx2Eak48&ab_channel=BinodSumanAcademy

Note: The instructions per the first link require some additional editing. Within the core-site.XML file, where it requires the dfs endpoint locator, I had to remove 'localhost:9000' and replace it with '<my computer name>:<my IP address>'. This allowed the namenode and data node to run properly.

### Step 2 - Useful commands to know
Using the CMD terminal, the following commands are useful:
1. jps: This commands lets you know what nodes are up and running. Ideally, you should have name node, data node, resource manager, and node manager up and running.
2. hadoop fs -ls /: Shows the contents within the root directory. The '/' is mandatory, otherwise it does not read properly. 
3. hadoop fs -put '<file directory> <location you want to place the file>'. Ultimately for me, this looked like hadoop fs -put C:/Users/Squarebear/Python/Projects/Hadoop/data.csv /input_dir
