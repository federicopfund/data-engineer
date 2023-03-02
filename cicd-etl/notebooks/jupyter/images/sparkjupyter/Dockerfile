FROM ubuntu:20.04

RUN apt update && \
    apt install openjdk-8-jdk openssh-server -y && \
    apt install python3 python3-venv python3-pip -y && \
    apt install sudo telnet groff vim -y && \
    rm -rf /var/lib/apt/lists/*

RUN adduser --disabled-password --gecos "" fede && \
    echo "fede:fede" | chpasswd && \
    adduser fede sudo

RUN sed -i "s/%sudo\tALL=(ALL:ALL) ALL/%sudo\tALL=(ALL:ALL) NOPASSWD:ALL/g" /etc/sudoers

USER fede

WORKDIR /home/fede
COPY --chown=fede:fede .ssh .ssh
RUN chmod 700 -R .ssh

COPY --chown=fede:fede requirements.txt /requirements.txt
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r /requirements.txt

COPY --chown=fede:fede softwares /softwares
COPY --chown=fede:fede deploy.sh /deploy.sh
COPY --chown=fede:fede configs/.profile .profile
COPY --chown=fede:fede configs /configs
COPY --chown=fede:fede kernels .kernels

ENV JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-amd64
ENV SPARK3_HOME=/opt/spark3
ENV PATH=$PATH:${SPARK3_HOME}/bin
ENV PATH=$PATH:/home/fede/.local/bin

RUN jupyter kernelspec \
    install .kernels/pyspark3 \
    --user
RUN jupyter kernelspec \
    install .kernels/pyspark3local \
    --user

RUN chmod u+x /deploy.sh

CMD ["/deploy.sh"]

CMD ["/home/fede/.local/bin/jupyter", "lab", "--ip", "0.0.0.0"]
