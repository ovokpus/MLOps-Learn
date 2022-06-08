import pandas as pd
import datetime as dt
import pickle

from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

import mlflow

from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
from hyperopt.pyll import scope

from prefect import flow, task
from prefect.task_runners import SequentialTaskRunner

mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment('linear_regression')


@task
def get_paths(date):
    if date == None:
        date = dt.date.today()
    else:
        date = dt.datetime.strptime(date, '%Y-%m-%d')
    first = date.replace(day=1)
    train_month = (first - dt.timedelta(days=1)).strftime('%Y-%m')
    val_month = (first - dt.timedelta(days=32)).strftime('%Y-%m')
    print(train_month, val_month)
    path_prefix = './data/fhv_tripdata_'
    train_path = path_prefix + f"{train_month}.parquet"
    val_path = path_prefix + f"{val_month}.parquet"
    return train_path, val_path


@task
def read_data(path):
    df = pd.read_parquet(path)
    return df


@task
def prepare_features(df, categorical, train=True):
    df['duration'] = df.dropOff_datetime - df.pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    mean_duration = df.duration.mean()
    if train:
        print(f"The mean duration of training is {mean_duration}")
    else:
        print(f"The mean duration of validation is {mean_duration}")

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    return df


@task
def train_model(df, categorical):
    with mlflow.start_run():
        mlflow.set_tag('model', 'linear regression')
        dv = DictVectorizer()

        train_dicts = df[categorical].to_dict(orient='records')

        X_train = dv.fit_transform(train_dicts)
        y_train = df.duration.values

        print(f"The shape of X_train is {X_train.shape}")
        print(f"The DictVectorizer has {len(dv.feature_names_)} features")

        lr = LinearRegression()
        lr.fit(X_train, y_train)
        y_pred = lr.predict(X_train)
        mse = mean_squared_error(y_train, y_pred, squared=False)
        print(f"The MSE of training is: {mse}")
        mlflow.log_metric("training mse", mse)
        print(lr, dv)
        return lr, dv


@task
def run_model(df, categorical, dv, lr, date):
    with mlflow.start_run():
        val_dicts = df[categorical].to_dict(orient='records')
        X_val = dv.transform(val_dicts)
        y_pred = lr.predict(X_val)
        y_val = df.duration.values

        mse = mean_squared_error(y_val, y_pred, squared=False)
        mlflow.log_metric("validation mse", mse)
        print(f"The MSE of validation is: {mse}")
        with open(f'artifacts/dv-{date}.b', 'wb') as f_out:
            pickle.dump(dv, f_out)
        with open(f'models/model-{date}.bin', 'wb') as f:
            pickle.dump(lr, f)
        mlflow.log_artifact(
            f'models/model-{date}.bin', artifact_path='model')
        mlflow.log_artifact(
            f'artifacts/dv-{date}.b', artifact_path='dv')
        mlflow.sklearn.log_model(lr, artifact_path='models_mlflow')
        return


@flow(task_runner=SequentialTaskRunner())
def main_lr(date="2021-08-15"):
    train_path, val_path = get_paths(date).result()

    categorical = ['PUlocationID', 'DOlocationID']

    df_train = read_data(train_path)
    df_train_processed = prepare_features(df_train, categorical)

    df_val = read_data(val_path)
    df_val_processed = prepare_features(df_val, categorical, False)

    # train the model
    lr, dv = train_model(df_train_processed, categorical).result()
    run_model(df_val_processed, categorical, dv, lr, date)


# main_lr()

from prefect.deployments import DeploymentSpec
from prefect.orion.schemas.schedules import CronSchedule
from prefect.flow_runners import SubprocessFlowRunner
from datetime import timedelta

DeploymentSpec(
    flow=main_lr,
    name="lr_training_schedule",
    schedule=CronSchedule(cron="0 9 15 * *",
                          timezone="America/Los_Angeles"),
    flow_runner=SubprocessFlowRunner(),
    tags=["ml"]
)
