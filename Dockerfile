From python:3.9.0
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip

RUN pip3 install -r requirements.txt
EXPOSE 8000
RUN chmod +X ./django_server.sh

ENTRYPOINT ["/bin/sh"]
CMD ["./django_server.sh"]
