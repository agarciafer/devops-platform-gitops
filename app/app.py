from flask import Flask, jsonify, render_template
from prometheus_client import Counter, Histogram, generate_latest
from prometheus_client import CONTENT_TYPE_LATEST
import socket
import time
import os
import logging
from logging_config import setup_logging

setup_logging()

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "app_requests_total",
    "Total application requests",
    ["method", "endpoint"]
)

REQUEST_LATENCY = Histogram(
    "app_request_latency_seconds",
    "Request latency"
)

APP_VERSION = os.getenv("APP_VERSION", "vx")
ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")

hostname = socket.gethostname()

logger = logging.getLogger(__name__)


@app.before_request
def before_request():
    REQUEST_COUNT.labels(method="GET", endpoint="/").inc()


@app.route("/")
@REQUEST_LATENCY.time()
def home():
    logger.info("Home endpoint accessed")

    return render_template(
        "index.html",
        version=APP_VERSION,
        hostname=hostname,
        environment=ENVIRONMENT
    )


@app.route("/healthz")
def healthz():
    logger.info("Healthcheck endpoint accessed")

    return jsonify({
        "status": "healthy"
    }), 200


@app.route("/info")
def info():
    logger.info("Info endpoint accessed")

    return jsonify({
        "application": "devops-platform-demo",
        "version": APP_VERSION,
        "environment": ENVIRONMENT,
        "hostname": hostname
    })


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {
        "Content-Type": CONTENT_TYPE_LATEST
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
