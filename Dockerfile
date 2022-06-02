FROM python:3.9-slim-buster

WORKDIR /app
RUN cd /app
COPY Pipfile.lock .
COPY Pipfile .
RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile
EXPOSE 8000
# ENV PYTHONPATH "${PYTHONPATH}:/app/"
COPY ./app /app

CMD ["hypercorn", "endpoints:app", "--bind", "0.0.0.0:8000", "--log-level", "debug"]
