import sys

#this is the second reducer
master_info={}

def flush():
    """
    Observe each key inside our master_info dictionary we created.
    We will print the make, year and accident_count as result.
    :return: Prints make, year and accident_count to be read with second mapper Python script.
    """
    for key, value in master_info.items():
        print( f'Model and Year: {key}, Number of accidents: {value}')

for line in sys.stdin:
    line.strip()
    make_year=line.split(',')[0]+' '+line.split(',')[1]
    master_info[make_year]=1
flush()





