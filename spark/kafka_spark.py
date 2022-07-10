import findspark

findspark.init()

from pyspark import SparkContext
from pyspark.conf import SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

if __name__ == "__main__":
    conf = SparkConf()
    conf.setAll(
        [
            (
                "spark.master",
                "spark://192.168.192.2:7077",
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
            # (
            #     "spark.driver.host",
            #     "172.31.48.86",
            # ),  # <--- this host is the resolvable IP for the host that is running the driver and it must be reachable by the master and master must be able to reach it (in our case the IP of the container where we are running pyspark
        ]
    )
    # sc = SparkContext(appName="PythonStreamingKafkaWordCount", conf=conf)
    # ssc = StreamingContext(sc, 60)
    # message = KafkaUtils.createDirectStream(
    #     ssc, topics=["kaf"], kafkaParams={"metadata.broker.list": "broker:9092"}
    # )

    # words = message.map(lambda x: x[1]).floatMap(lambda x: x.split(" "))
    # wordcount = words.map(lambda x: (x, 1)).reduceByKey(lambda x, y: x + y)
    # wordcount.pprint()

    # ssc.start()
    # ssc.awaitTermination()
