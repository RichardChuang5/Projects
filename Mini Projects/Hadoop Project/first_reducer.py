import sys

#this is the first reducer
master_info={}

def flush():
    """
    Observe each key inside our master_info dictionary we created.
    We will print the make, year and accident_count as result.
    :return: Prints make, year and accident_count to be read with second mapper Python script.
    """
    for key in master_info.keys():
        print(f'{master_info[key]["make"]}, {master_info[key]["year"]}\t{master_info[key]["accidents"]}')

for line in sys.stdin:
    line.strip()
    vin_number=line.split (',')[0]
    year=line.split(',')[4]
    year=year.strip()
    if len(line.split(',')[2])!=0:
        master_info[vin_number]={'make':line.split(',')[2]+' '+line.split(',')[3], 'year':year, 'accidents':0}
flush()





