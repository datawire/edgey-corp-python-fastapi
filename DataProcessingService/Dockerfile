FROM python:3
LABEL MAINTAINER="Arturo Gonzalez"

WORKDIR /app
ADD app.py /app

RUN pip install fastapi uvicorn requests
EXPOSE 3000

CMD ["python", "app.py"]
