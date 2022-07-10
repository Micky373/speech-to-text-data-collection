import json
from datetime import datetime

import boto3
import pandas as pd
from flask import Flask, jsonify, make_response, request
from flask_cors import CORS

from kafka import KafkaProducer

# from confluent_kafka import Consumer, Producer
# from confluent_kafka.admin import AdminClient, NewTopic

app = Flask(__name__)
CORS(app)

BROKER_URL = "broker:9092"
TOPIC = "raw"

# kafka_admin = AdminClient({"bootstrap.servers": BROKER_URL})


@app.route("/health", methods=["GET"])
def index():
    return make_response(jsonify({"timestamp": datetime.now().isoformat()}), 200)


@app.route("/health", methods=["GET"])
def index_health():
    return make_response(jsonify({"timestamp": datetime.now().isoformat()}), 200)


def encode(msg_value):
    """
    Encode a message

    Args:
        msg_value: The message value to be encoded
    """
    return json.dumps(msg_value, ensure_ascii=False).encode("utf-8")


@app.route("/text", methods=["GET"])
def get_text():
    s3 = boto3.client("s3")

    bucket = "10ac-batch-5"

    response = s3.get_object(Bucket=bucket, Key="week9/hu/amharic.csv")

    status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

    if status == 200:
        print(f"Successful S3 get_object response. Status - {status}")
        df = pd.read_csv(response.get("Body"))
        single_random_text = df.sample(n=1)["headline"]
        single_random_text.reset_index(drop=True, inplace=True)
        print(single_random_text)
        print({"staus": "sucess", "data": single_random_text[0].strip()})

    else:
        print(f"Unsuccessful S3 get_object response. Status - {status}")
        return make_response(
            jsonify(
                {
                    "status": "fail",
                }
            ),
            400,
        )
    # p = Producer({"bootstrap.servers": BROKER_URL})
    # p.produce(TOPIC, encode(single_random_text.to_dict()))
    # p.flush()
    producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode("utf-8"))
    producer.send("raw", {"text": single_random_text[0].strip()})

    return make_response(
        jsonify({"success": True, "data": single_random_text[0].strip()}), 200
    )


if __name__ == "__main__":
    app.run(host="localhost", port=11000, debug=False)
