import findspark
findspark.init()

import pyspark
from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils


if __name__ == __main__:
    sc = SparkContext(appName="KafkaSpark")
    ssc = StreamingContext(sc, 1)