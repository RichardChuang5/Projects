import sys

#this is the mapper

for line in sys.stdin:

    line=line.strip()
    items=line.split('\t')
    # to print the mapper values as a combination of make/model/year and count of accidents
    print (f"{items[0]},{items[1]}")