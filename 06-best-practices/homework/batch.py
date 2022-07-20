#!/usr/bin/env python
# coding: utf-8

import sys
import pickle
import pandas as pd
import os


if len(sys.argv) > 1:
    year = int(sys.argv[1])
    month = int(sys.argv[2])
else:
    year = 2021
    month = 3


input_file = f'https://raw.githubusercontent.com/alexeygrigorev/datasets/master/nyc-tlc/fhv/fhv_tripdata_{year:04d}-{month:02d}.parquet'
# output_file = f's3://nyc-duration/taxi_type=fhv/year={year:04d}/month={month:02d}/predictions.parquet'
output_file = f'output_data/taxi_type=fhv_year={year:04d}_month={month:02d}.parquet'


with open('/home/ovokpus/mlops-learn/06-best-practices/homework/model.bin', 'rb') as f_in:
    dv, lr = pickle.load(f_in)


def get_input_path(year, month):
    default_input_pattern = input_file
    input_pattern = os.getenv('INPUT_FILE_PATTERN', default_input_pattern)
    print(input_pattern.format(year=year, month=month))
    return input_pattern.format(year=year, month=month)


def get_output_path(year, month):
    default_output_pattern = output_file
    output_pattern = os.getenv('OUTPUT_FILE_PATTERN', default_output_pattern)
    print(output_pattern.format(year=year, month=month))
    return output_pattern.format(year=year, month=month)


def read_data(filename, options):
    df = pd.read_parquet(
        filename, storage_options=options)
    return df


def save_data(df, output_file, options):
    df.to_parquet(output_file, engine='pyarrow',
                  index=False, compression=None, storage_options=options)


def prepare_data(df, categorical):
    df['duration'] = df.dropOff_datetime - df.pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    print("length of dataframe", len(df))
    return df


def main(year, month):
    input_file = get_input_path(year, month)
    output_file = get_output_path(year, month)
    categorical = ['PUlocationID', 'DOlocationID']
    options = {
        'client_kwargs': {
            'endpoint_url': os.getenv('S3_ENDPOINT_URL'),
        }
    }
    raw_df = read_data(input_file, options)
    df = prepare_data(raw_df, categorical)
    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')

    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = lr.predict(X_val)

    print('predicted mean duration:', y_pred.mean())
    print('sum of predicted durations:', y_pred.sum())
    df_result = pd.DataFrame()
    df_result['ride_id'] = df['ride_id']
    df_result['predicted_duration'] = y_pred

    save_data(df_result, output_file, options)
    print('saved to', output_file)


if __name__ == '__main__':
    main(year, month)
    print('done')
    sys.exit(0)
