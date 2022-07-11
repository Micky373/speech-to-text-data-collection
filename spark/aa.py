from pyspark import SparkContext
from pyspark.conf import SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

# create SC with the specified configuration
def spark_context_creator():
    conf = SparkConf()
    # set name for our app
    conf.setAppName("ConnectingDotsSparkKafkaStreaming")
    # The master URL to connect
    conf.setMaster("spark://192.168.192.2:7077")
    sc = None
    try:
        sc.stop()
        sc = SparkContext(conf=conf)
    except:
        sc = SparkContext(conf=conf)
    return sc


sc = spark_context_creator()
# To avoid unncessary logs
sc.setLogLevel("WARN")
# batch duration, here i process for each second
ssc = StreamingContext(sc, 1)

kafkaStream = KafkaUtils.createStream(
    ssc, "zookeeper:2181", "test-consumer-group", {"input_event": 1}
)

