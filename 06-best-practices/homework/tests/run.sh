#!/usr/bin/env bash

cd "$(dirname "$0")"


export INPUT_FILE_PATTERN="s3://nyc-duration-prediction/in/{year:04d}-{month:02d}.parquet"
export OUTPUT_FILE_PATTERN="s3://nyc-duration-prediction/out/{year:04d}-{month:02d}.parquet"
export S3_ENDPOINT_URL="http://localhost:4566"
export S3_BUCKET_NAME="nyc-duration-prediction"
export S3_TEST_PATTERN="s3://nyc-duration-prediction/test/{year:04d}-{month:02d}.parquet"

docker-compose up -d

sleep 1

awslocal s3 mb s3://nyc-duration-prediction

pipenv run python test_batch.py

sleep 1

pytest

awslocal s3 ls

ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
    docker-compose logs
    docker-compose down
    exit ${ERROR_CODE}
fi

# docker-compose down