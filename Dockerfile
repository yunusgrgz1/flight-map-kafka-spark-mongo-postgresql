# Use the official Apache Airflow image with Python 3.9
FROM apache/airflow:2.6.0-python3.9

# Switch to the root user to install system packages
USER root

# Install Java 11 (OpenJDK)
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables for Java
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Switch back to the airflow user
USER airflow
