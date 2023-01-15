FROM python:3.9

#create directory in container base directory
WORKDIR /code

#Add requirements list to /code dir
COPY ./requirements.txt /code/requirements.txt

#Install requirements, don't use cache, upgrade if available
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["uvicorn","app.main:app", "--host", "0.0.0.0", "--port", "80"]