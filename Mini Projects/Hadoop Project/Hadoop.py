import sys
import boto3
#this is the first mapper
for line in sys.stdin:
    line=line.strip()
    items=line.split(',')
    # to print the mapper values as a combination of vin_number and tuples
    print (f'{items[3]}\t{items[1], items[3], items[5]}')

#define the reducer
#define group level master information here
master_reduce={}
'''def reset():
    #some logic to reset master info for every new group
    #run for end of every group
def flush():
    #write output
    #input comes from stdin
for line in sys.stdin:
    #parse the input we got from the mapper and update the master info
    #detect any key changes
    if current_vin !=vin:
        if current_vin != None:
            #write result to STDOUT
            flush()
        reset()
        #update more master info after the key change handling
        current_vin=current_vin
flush()'''
