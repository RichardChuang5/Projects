# Issues and fixes

1. from pyspark.sql import SparkSession
   from pyspark.sql.functions import month, count
  
2. Updated the path strings for answers_input_path and questions_input_path

3. resultDF.orderBy('question_id', 'month').explain() to show physical plan.
