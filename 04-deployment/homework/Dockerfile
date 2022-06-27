FROM agrigorev/zoomcamp-model:mlops-3.9.7-slim

# do stuff here
RUN pip install -U pip
RUN pip install pipenv 

WORKDIR /app

RUN mkdir -p /app/data

RUN mkdir -p /app/output

ADD data/*.* /app/data

COPY [ "Pipfile", "Pipfile.lock", "data/*.*", "./" ]

RUN pipenv install --system --deploy

COPY [ "starter.py", "./" ]

EXPOSE 9696

ENTRYPOINT [ "python3", "./starter.py","--year","2021", "--month","04"]