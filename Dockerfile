FROM amd64/debian
COPY . /app
WORKDIR /app
RUN apt-get update &&\ 
    apt-get install -y openssl procps iputils-ping net-tools curl gcc python3 python3-pip &&\ 
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install bottle gevent requests
CMD [ "python3", "./main.py" ]