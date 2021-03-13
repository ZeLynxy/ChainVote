FROM ubuntu:20.04
RUN apt update
RUN apt install -y software-properties-common && \
    rm -rf /var/lib/apt/lists/*
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt install -y python3.8 python3-pip

WORKDIR /chainvote-api

COPY requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install  --no-cache-dir  -r requirements.txt

VOLUME /chainvote-api 
VOLUME /chainvote-smart-contracts 

ADD /chainvote-api  /chainvote-api
ADD /chainvote-smart-contracts /chainvote-smart-contracts 

#deploy contracts
RUN add-apt-repository ppa:ethereum/ethereum
RUN apt-get update
RUN apt-get install -y solc
RUN pip3 install py-solc-x
WORKDIR /chainvote-smart-contracts
RUN python3.8 deploy.py
RUN ls
WORKDIR /chainvote-api
