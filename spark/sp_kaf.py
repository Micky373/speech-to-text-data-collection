import pyspark

# from pyspark.streaming import StreamingContext
# from pyspark.streaming.kafka import KafkaUtils

from pyspark.conf import SparkConf
from pyspark.context import SparkContext
from pyspark.sql import SparkSession

conf = SparkConf()
conf.setAll(
    [
        (
            "spark.master",
            "spark://192.168.16.2:7077",
        ),  # <--- this host must be resolvable by the driver in this case pyspark (whatever it is located, same server or remote) in our case the IP of server
        ("spark.driver.host", "local[*]"),
        ("spark.app.name", "myApp"),
        ("spark.submit.deployMode", "client"),
        ("spark.ui.showConsoleProgress", "true"),
        ("spark.eventLog.enabled", "false"),
        ("spark.logConf", "false"),
        (
            "spark.driver.bindAddress",
            "0.0.0.0",
        ),  # <--- this host is the IP where pyspark will bind the service running the driver (normally 0.0.0.0)
        (
            "spark.driver.host",
            "172.31.48.86",
        ),  # <--- this host is the resolvable IP for the host that is running the driver and it must be reachable by the master and master must be able to reach it (in our case the IP of the container where we are running pyspark
    ]
)

# Set conf for spark session
# spark = SparkSession.builder.config(conf=conf).appName("audio-data").getOrCreate()
spark = SparkSession.builder.appName("audio-data").getOrCreate()
spark.sparkContext.setLogLevel("WARN")


# kafka_df = (
#     spark.readStream.format("kafka")
#     .option("kafka.bootstrap.servers", "broker:9092")
#     .option("subscribe", "kaf")
#     .option("startingOffsets", "latest")
#     .load()
# )

# kafka_streaming_df = kafka_df.selectExpr(
#     "cast(key as string) key", "CAST(value AS STRING)"
# )

# kafka_streaming_df.writeStream.outputMode("append").format(
#     "console"
# ).start().awaitTermination()

logFile = "dup.txt"
logData = spark.read.text(logFile).cache()
print("LOG DATA: ", logData)

numDs = logData.filter(logData.value.contains("b")).count()
numAs = logData.filter(logData.value.contains("a")).count()


print("***************")
print("***************")
print(f"DDD: {numDs} AAAA: {numAs}")
print("***************")
print("***************")

spark.stop()
