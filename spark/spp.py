import pyspark

# from pyspark.streaming import StreamingContext
# from pyspark.streaming.kafka import KafkaUtils

from pyspark.conf import SparkConf
from pyspark.context import SparkContext

# create SC with the specified configuration
def spark_context_creator():
    conf = SparkConf()
    conf.setAll(
        [
            (
                "spark.master",
                "spark://192.168.96.4:7077",
            ),  # <--- this host must be resolvable by the driver in this case pyspark (whatever it is located, same server or remote) in our case the IP of server
            ("spark.driver.host","local[*]"),
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
    # set name for our app
    # conf.setAppName("ConnectingDotsSparkKafkaStreaming")
    # The master URL to connect
    # conf.setMaster("spark://localhost:7077")
    # 172.31.48.86

    # sc = SparkContext(conf=conf)
    try:
        sc.stop()
        sc = SparkContext(conf=conf)
    except:
        sc = SparkContext(conf=conf)
    return sc


sc = spark_context_creator()
# To avoid unncessary logs
sc.setLogLevel("WARN")
