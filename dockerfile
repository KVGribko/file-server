FROM python:3.11 AS builder

COPY poetry.lock pyproject.toml ./

RUN python -m pip install --no-cache-dir poetry==1.4.2 \
    && poetry export --without-hashes --without dev,test -f requirements.txt -o requirements.txt

FROM python:3.11

WORKDIR /code

COPY --from=builder requirements.txt ./
RUN python -m pip install -r requirements.txt

COPY . /code

RUN make env_prod

CMD make run_prod
