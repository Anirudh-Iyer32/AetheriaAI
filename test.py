import boto3

client = boto3.client('sagemaker-runtime')

response = client.invoke_endpoint(
    EndpointName='lgbm-champion-endpoint-v2',
    ContentType='text/csv',
    Body='0	,1,	20,	0,	1	,192,	2,	0,	2,	4,	2,	2,	2,	2,	4,	1,	3,	2,	2,	2,	0,	0'
)

print(response['Body'].read().decode())
