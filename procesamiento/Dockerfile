FROM openjdk:8-jdk-slim

ENV HADOOP_VERSION=3.3.6 \
    PIG_VERSION=0.17.0

RUN apt-get update && \
    apt-get install -y wget tar && \
    wget https://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz && \
    tar -xzf hadoop-${HADOOP_VERSION}.tar.gz -C /opt && \
    mv /opt/hadoop-${HADOOP_VERSION} /opt/hadoop && \
    wget https://archive.apache.org/dist/pig/pig-${PIG_VERSION}/pig-${PIG_VERSION}.tar.gz && \
    tar -xzf pig-${PIG_VERSION}.tar.gz -C /opt && \
    mv /opt/pig-${PIG_VERSION} /opt/pig && \
    rm hadoop-${HADOOP_VERSION}.tar.gz pig-${PIG_VERSION}.tar.gz && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV HADOOP_HOME=/opt/hadoop \
    PIG_HOME=/opt/pig \
    PATH=$PATH:/opt/hadoop/bin:/opt/pig/bin

WORKDIR /data

COPY procesamiento.pig ./

RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install elasticsearch==8.13.0

CMD ["pig", "-x", "local", "procesamiento.pig"]