try:

    from datetime import timedelta
    from airflow import DAG
    from airflow.operators.python_operator import PythonOperator
    from datetime import datetime
    import pandas as pd
    import boto3

    import json
    from confluent_kafka import Consumer, Producer
    from confluent_kafka.admin import AdminClient, NewTopic

    print("All Dag modules are ok ......")
except Exception as e:
    print("Error  {} ".format(e))

BROKER_URL = "localhost:9092"
TOPIC = "raw"


def consumer_from_kafka(**context):
    kafka_admin = AdminClient({"bootstrap.servers": BROKER_URL})
    # print(kafka_admin.list_topics().topics)
    # print(topic)
    """
    Consume messages from the topic

    Args:
        topic: The topic to consume from
    """

    c = Consumer(
        {
            "bootstrap.servers": BROKER_URL,
            "group.id": "121",
            "auto.offset.reset": "latest",
        }
    )
    messages = []
    c.subscribe([TOPIC])
    running = True
    # logger.info("Consumer started")
    poll_timeout = 0
    while running:
        msg = c.poll(1.0)

        if poll_timeout == 20:
            running = False
            break

        if msg is None:
            poll_timeout = poll_timeout + 1
            print("No message received", poll_timeout)
            # logger.debug("No message received")
        elif msg.error() is not None:
            # logger.error(msg.error())
            running = False

        else:
            poll_timeout = 0
            # Get the message from Kafka
            msg_value = msg.value()
            # decode the message
            msg_value = msg_value.decode("utf-8")
            messages.append(msg_value)

            print(f"Received message: {msg_value}")
    context["ti"].xcom_push(key="data", value=messages)


# def train_model(**context):
#     print("train_model")
#     data = context.get("ti").xcom_pull(key="data")
#     print("data is {}".format(data))
#     print("train_model")


def insert_to_s3(**context):
    print("insert_to_s3")
    data = context.get("ti").xcom_pull(key="data")
    print("data is {}".format(data))
    print("insert_to_s3")
    s3 = boto3.client("s3")

    bucket = "10ac-batch-5"
    # format name with current timestamp
    json_file_name = "json_file_" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".json"
    s3object = s3.Object(bucket, json_file_name)

    s3object.put(Body=(bytes(json.dumps(data).encode("UTF-8"))))
    print("Inserted to S3")

with DAG(
    dag_id="consumer_dag",
    schedule_interval="@daily",
    default_args={
        "owner": "airflow",
        "retries": 3,
        "retry_delay": timedelta(minutes=5),
        "start_date": datetime(2021, 1, 1),
    },
    catchup=False,
) as f:

    consumer_from_kafka = PythonOperator(
        task_id="consumer_from_kafka",
        python_callable=consumer_from_kafka,
        provide_context=True,
    )

    insert_to_s3 = PythonOperator(
        task_id="insert_to_s3",
        python_callable=insert_to_s3,
        provide_context=True,
    )

consumer_from_kafka >> insert_to_s3
