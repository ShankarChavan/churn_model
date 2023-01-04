FROM python:3.7-slim-buster

WORKDIR /code

COPY ./requirements_api.txt /code/requirements_api.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements_api.txt

COPY ./churn_api/ /code/churn_api

ENV PYTHONPATH "${PYTHONPATH}:/code/churn_api"

EXPOSE 8000

CMD [ "uvicorn","churn_api.predict:app","--host=0.0.0.0", "--reload"]