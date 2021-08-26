'''
Optimize the query plan

Suppose we want to compose query in which we get for each question also the number of answers to this question for each month. See the query below which does that in a suboptimal way and try to rewrite it to achieve a more optimal plan.
'''

# Import SparkSession from pyspark.sql
from pyspark.sql import SparkSession
from pyspark.sql.functions import month, count

import os, time

start_1 = time.time()
spark = SparkSession.builder.appName('Optimize I').getOrCreate()

base_path = os.getcwd()

project_path = ('/').join(base_path.split('/')[0:-3]) 

# Update the path to the answers directory
answers_input_path = os.path.join(project_path, '/Users/yasmeenfuentes/PycharmProjects/pythonProject/Mini-Projects/Spark/Spark_Optimization/data/answers')
# Update the path to the questions directory
questions_input_path = os.path.join(project_path, '/Users/yasmeenfuentes/PycharmProjects/pythonProject/Mini-Projects/Spark/Spark_Optimization/data/questions')

answersDF = spark.read.option('path', answers_input_path).load()

questionsDF = spark.read.option('path', questions_input_path).load()

'''
Answers aggregation

Here we : get number of answers per question per month
'''

# from pyspark.sql.functions import month and count
answers_month = answersDF.withColumn('month', month('creation_date')).groupBy('question_id', 'month').agg(count('*').alias('cnt'))

resultDF = questionsDF.join(answers_month, 'question_id').select('question_id', 'creation_date', 'title', 'month', 'cnt')

resultDF.orderBy('question_id', 'month').show(truncate = False)

end_1 = time.time()
total_time = end_1 - start_1
print("%s total seconds to process\n--------------------------------------" %total_time)
resultDF.orderBy('question_id', 'month').explain()
'''
Task:

see the query plan of the previous result and rewrite the query to optimize it

--------------------------
query plan result
--------------------------
== Physical Plan ==
*(4) Sort [question_id#12L ASC NULLS FIRST, month#28 ASC NULLS FIRST], true, 0
+- Exchange rangepartitioning(question_id#12L ASC NULLS FIRST, month#28 ASC NULLS FIRST, 200), ENSURE_REQUIREMENTS, [id=#151]
   +- *(3) Project [question_id#12L, creation_date#14, title#15, month#28, cnt#44L]
      +- *(3) BroadcastHashJoin [question_id#12L], [question_id#0L], Inner, BuildRight, false
         :- *(3) Filter isnotnull(question_id#12L)
         :  +- *(3) ColumnarToRow
         :     +- FileScan parquet [question_id#12L,creation_date#14,title#15] Batched: true, DataFilters: [isnotnull(question_id#12L)], Format: Parquet, Location: InMemoryFileIndex[file:/Users/yasmeenfuentes/PycharmProjects/pythonProject/Mini-Projects/Spark/Sp..., PartitionFilters: [], PushedFilters: [IsNotNull(question_id)], ReadSchema: struct<question_id:bigint,creation_date:timestamp,title:string>
         +- BroadcastExchange HashedRelationBroadcastMode(List(input[0, bigint, true]),false), [id=#146]
            +- *(2) HashAggregate(keys=[question_id#0L, month#28], functions=[count(1)])
               +- Exchange hashpartitioning(question_id#0L, month#28, 200), ENSURE_REQUIREMENTS, [id=#142]
                  +- *(1) HashAggregate(keys=[question_id#0L, month#28], functions=[partial_count(1)])
                     +- *(1) Project [question_id#0L, month(cast(creation_date#2 as date)) AS month#28]
                        +- *(1) Filter isnotnull(question_id#0L)
                           +- *(1) ColumnarToRow
                              +- FileScan parquet [question_id#0L,creation_date#2] Batched: true, DataFilters: [isnotnull(question_id#0L)], Format: Parquet, Location: InMemoryFileIndex[file:/Users/yasmeenfuentes/PycharmProjects/pythonProject/Mini-Projects/Spark/Sp..., PartitionFilters: [], PushedFilters: [IsNotNull(question_id)], ReadSchema: struct<question_id:bigint,creation_date:timestamp>
'''

# ---------------------------------------------------------------------------------------------------------------
# Optimized below
# ---------------------------------------------------------------------------------------------------------------


start_2 = time.time()

# enable sparks adaptive enablement for 'smart' querying
spark.conf.set("spark.sql.adaptive.enabled", "true")
answers_month = answersDF.withColumn('month', month('creation_date')).groupBy('question_id', 'month').agg(count('*').alias('cnt'))
resultDF = questionsDF.join(answers_month, 'question_id').select('question_id', 'creation_date', 'title', 'month', 'cnt')
resultDF.orderBy('question_id', 'month').show(truncate = False)
end_2 = time.time()
total_time_2 = end_2 - start_2
print("%s total seconds to process\nOptimized Query Diff:\
%s\n--------------------------------------" %((total_time_2),(total_time_2 - total_time)))

resultDF.orderBy('question_id', 'month').explain()

'''
Updated Query Plan

== Physical Plan ==
AdaptiveSparkPlan isFinalPlan=false
+- Sort [question_id#12L ASC NULLS FIRST, month#86 ASC NULLS FIRST], true, 0
   +- Exchange rangepartitioning(question_id#12L ASC NULLS FIRST, month#86 ASC NULLS FIRST, 200), ENSURE_REQUIREMENTS, [id=#356]
      +- Project [question_id#12L, creation_date#14, title#15, month#86, cnt#102L]
         +- BroadcastHashJoin [question_id#12L], [question_id#0L], Inner, BuildRight, false
            :- Filter isnotnull(question_id#12L)
            :  +- FileScan parquet [question_id#12L,creation_date#14,title#15] Batched: true, DataFilters: [isnotnull(question_id#12L)], Format: Parquet, Location: InMemoryFileIndex[file:/Users/yasmeenfuentes/PycharmProjects/pythonProject/Mini-Projects/Spark/Sp..., PartitionFilters: [], PushedFilters: [IsNotNull(question_id)], ReadSchema: struct<question_id:bigint,creation_date:timestamp,title:string>
            +- BroadcastExchange HashedRelationBroadcastMode(List(input[0, bigint, true]),false), [id=#352]
               +- HashAggregate(keys=[question_id#0L, month#86], functions=[count(1)])
                  +- Exchange hashpartitioning(question_id#0L, month#86, 200), ENSURE_REQUIREMENTS, [id=#349]
                     +- HashAggregate(keys=[question_id#0L, month#86], functions=[partial_count(1)])
                        +- Project [question_id#0L, month(cast(creation_date#2 as date)) AS month#86]
                           +- Filter isnotnull(question_id#0L)
                              +- FileScan parquet [question_id#0L,creation_date#2] Batched: true, DataFilters: [isnotnull(question_id#0L)], Format: Parquet, Location: InMemoryFileIndex[file:/Users/yasmeenfuentes/PycharmProjects/pythonProject/Mini-Projects/Spark/Sp..., PartitionFilters: [], PushedFilters: [IsNotNull(question_id)], ReadSchema: struct<question_id:bigint,creation_date:timestamp>
'''


