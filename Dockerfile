FROM python:3.10

RUN mkdir -p /usr/src/run/
WORKDIR /usr/src/run/


COPY . /usr/src/run/
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python", "run.py"]
