import batch
from pathlib import Path
from datetime import datetime
import pandas as pd
import os


def dt(hour, minute, second=0):
    return datetime(2020, 1, 1, hour, minute, second)


def test_read_data():
    data = [
        (None, None, dt(1, 2), dt(1, 10)),
        (1, 1, dt(1, 2), dt(1, 10)),
        (1, 1, dt(1, 2, 0), dt(1, 2, 50)),
        (1, 1, dt(1, 2, 0), dt(2, 2, 1)),
    ]

    year = 2021
    month = 1

    columns = ['PUlocationID', 'DOlocationID',
               'pickup_datetime', 'dropOff_datetime']

    df = pd.DataFrame(data, columns=columns)

    options = {
        'client_kwargs': {
            'endpoint_url': os.getenv('S3_ENDPOINT_URL')
        }
    }

    expected_df = batch.read_data(
        os.getenv('INPUT_FILE_PATTERN').format(year=year, month=month),
        options
    )

    actual_transformed_df = batch.prepare_data(
        df.copy(), categorical=['PUlocationID', 'DOlocationID'])

    expected_transformed_df = batch.prepare_data(
        expected_df.copy(), categorical=['PUlocationID', 'DOlocationID'])

    print(len(expected_df))

    assert len(df) == len(expected_df)
    assert df.columns.all() == expected_df.columns.all()
    assert len(expected_transformed_df) == len(actual_transformed_df)
    assert len(expected_transformed_df.columns) == len(
        actual_transformed_df.columns)
