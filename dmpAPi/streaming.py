from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark import SparkConf
from pyspark.ml.feature import HashingTF, IDF, Tokenizer
from pyspark.ml.feature import CountVectorizer
from timeit import default_timer as timer
from pyspark.sql.functions import udf
from pyspark.sql.types import DoubleType, ArrayType

import time
import pandas as pd


toptimer = timer()
starttime = timer()

app = 'exampleDataFrameApi'
conf = (SparkConf().setAppName(app)
                    .setMaster("local[*]")
                    .set('spark.driver.maxResultSize', '8g')
                    .set("spark.executor.memory", "8g")
                    .set('spark.logConf', 'true'))

sc = SparkContext(conf=conf)
# sc.setLogLevel("ERROR")
spark = SparkSession(sc)

from pyspark.sql.types import StructType,StructField, StringType, IntegerType
data2 = [("James","","Smith","36636","M",3000),
    ("Michael","Rose","","40288","M",4000),
    ("Robert","","Williams","42114","M",4000),
    ("Maria","Anne","Jones","39192","F",4000),
    ("Jen","Mary","Brown","","F",-1)]

schema = StructType([ \
    StructField("firstname",StringType(),True), \
    StructField("middlename",StringType(),True), \
    StructField("lastname",StringType(),True), \
    StructField("id", StringType(), True), \
    StructField("gender", StringType(), True), \
    StructField("salary", IntegerType(), True) \
  ])
 
df = spark.createDataFrame(data=data2,schema=schema)
df.printSchema()
df.show(truncate=False)


# # Subscribe to 1 topic
# df = spark \
#   .readStream \
#   .format("kafka") \
#   .option("kafka.bootstrap.servers", "host1:port1,host2:port2") \
#   .option("subscribe", "topic1") \
#   .load()
# df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
