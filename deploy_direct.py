import sagemaker
from sagemaker.sklearn.model import SKLearnModel
import boto3
import tarfile
import os

# ---- Step A: package the model artifact ----
with tarfile.open("model.tar.gz", "w:gz") as tar:
    tar.add("model.joblib")

# ---- Step B: upload to S3 ----
s3 = boto3.client("s3")
bucket = "customer-satisfaction-with-deploy"
key = "model-artifacts/model.tar.gz"
s3.upload_file("model.tar.gz", bucket, key)
model_s3_path = f"s3://{bucket}/{key}"
print("Uploaded to:", model_s3_path)

# ---- Step C: define the SageMaker Model ----
session = sagemaker.Session()
role = "arn:aws:iam::549116506545:role/service-role/AmazonSageMaker-ExecutionRole-20260626T155580"

sklearn_model = SKLearnModel(
    model_data=model_s3_path,
    role=role,
    entry_point="inference.py",
    source_dir="inference_package",
    framework_version="1.2-1",
    py_version="py3",
    sagemaker_session=session,
)

predictor = sklearn_model.deploy(
    initial_instance_count=1,
    instance_type="ml.m5.large",
    endpoint_name="lgbm-champion-endpoint-v2",
    container_startup_health_check_timeout=600,
)

print("Endpoint is live:", predictor.endpoint_name)