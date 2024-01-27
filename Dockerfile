FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements/base.txt
ARG PORT=80
EXPOSE ${PORT}
RUN chmod u+x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
