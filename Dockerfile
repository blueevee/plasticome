FROM ubuntu:20.04

COPY . /app

WORKDIR /app

RUN apt-get update && apt-get install -y \
    # apt-transport-https \
    # ca-certificates \
    # build-essential \
    curl \
    # gnupg-agent \
    # software-properties-common && \
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add - && \
    add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) stable" && \
    apt-get install -y docker-ce docker-ce-cli containerd.io && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    sudo apt install python3.11


RUN curl -sSL https://install.python-poetry.org | python3 - &&\
    poetry install --no-root

RUN chmod +x /app/start.sh

CMD [ "/bin/bash", "/app/start.sh" ]

