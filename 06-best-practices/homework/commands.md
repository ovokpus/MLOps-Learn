# Sample Template commands to set up the test stack

1. Set Environment Variables for batch script.
2. Spin up docker container.
3. Add input objects to the S3 bucket
4. Run batch script.
5. Run Test Bash script.
6. Run Integration Test.

## COMMANDS

```bash
awslocal s3 mb s3://nyc-duration-prediction

awslocal s3 ls

awslocal s3api put-object --bucket nyc-duration-prediction --key in/2021-05.parquet --body /home/ovokpus/mlops-learn/06-best-practices/homework/input_data/fhv_tripdata_2021-08.parquet

awslocal s3api put-object --bucket nyc-duration-prediction --key in/2021-04.parquet --body /home/ovokpus/mlops-learn/06-best-practices/homework/input_data/fhv_tripdata_2021-07.parquet

awslocal s3api put-object --bucket nyc-duration-prediction --key in/2021-03.parquet --body /home/ovokpus/mlops-learn/06-best-practices/homework/input_data/fhv_tripdata_2021-06.parquet

awslocal s3api put-object --bucket nyc-duration-prediction --key in/2021-02.parquet --body /home/ovokpus/mlops-learn/06-best-practices/homework/input_data/fhv_tripdata_2021-05.parquet

awslocal s3api put-object --bucket nyc-duration-prediction --key in/2021-01.parquet --body /home/ovokpus/mlops-learn/06-best-practices/homework/input_data/fhv_tripdata_2021-04.parquet

awslocal s3api put-object --bucket nyc-duration-prediction --key in/2020-12.parquet --body /home/ovokpus/mlops-learn/06-best-practices/homework/input_data/fhv_tripdata_2021-03.parquet

awslocal s3api put-object --bucket nyc-duration-prediction --key in/2020-11.parquet --body /home/ovokpus/mlops-learn/06-best-practices/homework/input_data/fhv_tripdata_2021-02.parquet

awslocal s3api put-object --bucket nyc-duration-prediction --key in/2020-10.parquet --body /home/ovokpus/mlops-learn/06-best-practices/homework/input_data/fhv_tripdata_2021-01.parquet

awslocal s3api list-objects --bucket nyc-duration-prediction --prefix test/

awslocal s3api list-objects --bucket nyc-duration-prediction --prefix test/

awslocal s3api list-objects --bucket nyc-duration-prediction --prefix in/
```
