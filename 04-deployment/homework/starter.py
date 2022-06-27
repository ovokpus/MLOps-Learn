#!/usr/bin/env python
# coding: utf-8

# In[1]:


# get_ipython().system('pip freeze | grep scikit-learn')


# In[2]:

import argparse
import pickle
import pandas as pd


# In[3]:


with open('./model.bin', 'rb') as f_in:
    dv, lr = pickle.load(f_in)


# In[4]:


categorical = ['PUlocationID', 'DOlocationID']


def read_data(filename):
    df = pd.read_parquet(filename)

    df['duration'] = df.dropOff_datetime - df.pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')

    return df


# In[6]:
parser = argparse.ArgumentParser()
parser.add_argument('--year', type=str, default='2021')
parser.add_argument('--month', type=str, default='01')
args = parser.parse_args()

df = read_data(f'./data/fhv_tripdata_{args.year}-{args.month}.parquet')


# In[7]:


dicts = df[categorical].to_dict(orient='records')
X_val = dv.transform(dicts)
y_pred = lr.predict(X_val)


# In[9]:


print("mean predicted duration", y_pred.mean())


# In[15]:


df['ride_id'] = f"{2021:04d}/{2:02d}_" + df.index.astype('str')
df.to_parquet(
    "output/results.parquet",
    engine='pyarrow',
    compression=None,
    index=False
)
