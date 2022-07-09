import json
from datetime import datetime

import boto3
import pandas as pd
from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
from kafka import KafkaProducer

app = Flask(__name__)
CORS(app)


@app.route("/health", methods=["GET"])
def index():
    return make_response(
        jsonify({"timestamp": datetime.now().isoformat()}), 200
    )


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
    else:
        print(f"Unsuccessful S3 get_object response. Status - {status}")

    producer = KafkaProducer(
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )
    producer.send("raw", {"text": single_random_text[0].strip()})

    return make_response(
        jsonify({"success": True, "data": single_random_text[0].strip()}), 200
    )


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=False)
