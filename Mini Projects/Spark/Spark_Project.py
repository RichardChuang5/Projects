#! /usr/bin/python
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster('local').setAppName('post_sales')
sc = SparkContext(conf = conf)
raw_rdd = sc.textFile('data.csv')

# Need to propagate make and year to the accident records with INCIDENT TYPE A.
# Use vin_number as the aggregate key. Map output should be vin_number, value is make and year and incident type


def extract_vin_key_value(x):
    items = x.split(',')
    vin_num = items[2]
    make = items[3] + items[4]
    year = items[5]
    incident = items[1]
    return vin_num, (make, year, incident)
vin_kv = raw_rdd.map(lambda x: extract_vin_key_value(x))
print(vin_kv.collect())

def populate_make(kv):
    sorted(kv)
    output=[]
    # flatmap explodes the individual elements within an item. For example, each item in kv is comprised of a
    # tuple, with item 0 being the vin and item 1 being ANOTHER tuple of make, year, incident. Flat map will interpret
    # this list as an item of 2, vin, and the tuple. Thus when we say populate_make(kv[1]) we are pushing through
    # only the tuple of make, year, incident. It is important to note that kv is a spark object and returning it
    # only provides the object location and therefore, doing something like kv[0] returns an error as it is not a
    # subscriptable item as it is a spark object. Spark objects can however be looped on.
    for val in kv:
        # to capture all incidents, not just 'I'
        incident = val[2]
        if val[0] != '':
            make = val[0]
            year = val[1]
        output.append(((make,year), incident))
    return output
enhance_make = vin_kv.groupByKey().flatMap(lambda kv: populate_make(kv[1]))
print(enhance_make.collect())

def extract_make_key_value(x):
    if x[1] == 'A':
        return x[0], 1
    else:
        return x[0], 0

make_kv = enhance_make.map(lambda x: extract_make_key_value(x))
print(make_kv.collect())

final_reduce = make_kv.reduceByKey(lambda x,y: x+y)
final_rdd = final_reduce.collect()

#final_statement = final_reduce.map(lambda x: x[0][0]+'-'+str(x[0][1])+','+str(x[1]))
#print(final_statement.collect(), end='\n')

for item in final_rdd:
    print(item[0][0]+'-'+str(item[0][1])+','+str(item[1]))
    