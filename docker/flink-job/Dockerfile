FROM flink:1.17.1-scala_2.12-python3.7

USER root
RUN apt-get update && apt-get install -y wget python3-pip && rm -rf /var/lib/apt/lists/*

USER flink

ENV KAFKA_CONNECTOR_VERSION=1.17.1
ENV JDBC_CONNECTOR_VERSION=1.17.1

RUN wget -P /opt/flink/lib/ https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-kafka/${KAFKA_CONNECTOR_VERSION}/flink-sql-connector-kafka-${KAFKA_CONNECTOR_VERSION}.jar && \
    wget -P /opt/flink/lib/ https://repo.maven.apache.org/maven2/org/apache/flink/flink-connector-jdbc/${JDBC_CONNECTOR_VERSION}/flink-connector-jdbc-${JDBC_CONNECTOR_VERSION}.jar

COPY --chown=flink:flink ./flink_cdc_analytics /opt/flink_cdc_analytics

COPY --chown=flink:flink requirements.txt /opt/
RUN pip3 install --no-cache-dir -r /opt/requirements.txt

WORKDIR /opt/flink_cdc_analytics

ENTRYPOINT ["python3", "main.py"]
