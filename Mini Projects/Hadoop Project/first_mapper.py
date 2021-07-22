import sys

#this is the mapper

for line in sys.stdin:

    line=line.strip()
    items=line.split(',')
    # to print the mapper values as a combination of vin_number and tuples
    # prints out as Vin number  (tab) accident/incident, car, model, year
    print (f"{items[2]},{items[1]},{items[3]},{items[4]},{items[5]}")