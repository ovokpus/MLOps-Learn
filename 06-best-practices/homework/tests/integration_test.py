import pandas as pd
import boto3
import os
import batch
from datetime import datetime
from pprint import pprint
from deepdiff import DeepDiff

s3_url = os.getenv(
    'S3_ENDPOINT_URL', 'https://localhost:4566')
s3_client = boto3.client('s3', endpoint_url=s3_url)


def dt(hour, minute, second=0):
    return datetime(2020, 1, 1, hour, minute, second)


data = [
    (None, None, dt(1, 2), dt(1, 10)),
    (1, 1, dt(1, 2), dt(1, 10)),
    (1, 1, dt(1, 2, 0), dt(1, 2, 50)),
    (1, 1, dt(1, 2, 0), dt(2, 2, 1)),
]

columns = ['PUlocationID', 'DOlocationID',
           'pickup_datetime', 'dropOff_datetime']

df = pd.DataFrame(data, columns=columns)

year = 2021
month = 1


input_pattern = f'tests/data/test_integration_data.parquet'
input_file = os.getenv('INPUT_FILE_PATTERN', input_pattern).format(
    year=year, month=month)


options = {
    'client_kwargs': {
        'endpoint_url': os.getenv('S3_ENDPOINT_URL'),
    }
}


df.to_parquet(
    input_file,
    engine='pyarrow',
    compression=None,
    index=False,
    storage_options=options
)

print("Done", input_file)

command = "python3 ../batch.py {} {}".format(year, month)
os.system(command)

response = s3_client.list_objects(
    Bucket=os.getenv('S3_BUCKET_NAME'), Prefix="out/")

# pprint(response['Contents'])

assert len(response['Contents']) >= 1

expected_record = ('out/2021-01.parquet', 1970)

actual_record = [(r['Key'], r['Size']) for r in response['Contents']
                 if r['Key'] == f'out/{year:04d}-{month:02d}.parquet']

pprint(actual_record[0])

diff = DeepDiff(actual_record[0], expected_record, significant_digits=1)

print(f'Difference: {diff}')

assert 'values_changed' not in diff
assert 'type_changes' not in diff


print('all good')
