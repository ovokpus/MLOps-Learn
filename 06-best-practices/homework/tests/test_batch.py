import batch
from pathlib import Path
from datetime import datetime
import pandas as pd
import os


def dt(hour, minute, second=0):
    return datetime(2020, 1, 1, hour, minute, second)


def prepare_data(df, categorical=['PUlocationID', 'DOlocationID']):
    df['duration'] = df.dropOff_datetime - df.pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    print(len(df))
    return df


def test_prepare_data():
    data = [
        (None, None, dt(1, 2), dt(1, 10)),
        (1, 1, dt(1, 2), dt(1, 10)),
        (1, 1, dt(1, 2, 0), dt(1, 2, 50)),
        (1, 1, dt(1, 2, 0), dt(2, 2, 1)),
    ]

    columns = ['PUlocationID', 'DOlocationID',
               'pickup_datetime', 'dropOff_datetime']
    df = pd.DataFrame(data, columns=columns)

    expected_df = batch.read_data(
        '/home/ovokpus/mlops-learn/06-best-practices/homework/tests/data/test_prepare_data.parquet')
    assert df.equals(expected_df)
    assert df.columns.all() == expected_df.columns.all()
