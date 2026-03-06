# 1. Use a lightweight Python base image
FROM python:3.12-slim

# 2. Set environment variables
# This prevents Python from writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
# This prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# 3. Install OpenJDK-21 (Required for PySpark)
# We use 'slim' images, so we need to install Java manually.
RUN apt-get update && \
    apt-get install -y openjdk-21-jre-headless && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 4. Set JAVA_HOME environment variable
ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64

# 5. Install PySpark and JupyterLab
# We specify versions to ensure compatibility
RUN pip install --no-cache-dir \
    pyspark==4.1.0 \
    jupyterlab==4.0.9

# 6. Set the working directory
WORKDIR /workspace

# 7. Expose the Jupyter port
EXPOSE 8888

# 8. Start JupyterLab
# --ip=0.0.0.0 makes it accessible from outside the container
# --no-browser prevents trying to open a browser inside the container
# --allow-root allows running as root user (common in docker)
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]