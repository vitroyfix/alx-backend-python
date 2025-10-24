# Dockerfile for a custom Jenkins image with Python to fix the "python3: not found" error

FROM jenkins/jenkins:lts-jdk21

# Switch to root to install packages
USER root

# Install Python3, pip, git, and Docker CLI with compose plugin
RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates curl gnupg python3 python3-pip git && \
    install -m 0755 -d /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
    chmod a+r /etc/apt/keyrings/docker.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian $(. /etc/os-release && echo $VERSION_CODENAME) stable" > /etc/apt/sources.list.d/docker.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends docker-ce-cli docker-compose-plugin && \
    rm -rf /var/lib/apt/lists/* && \
    groupadd -f docker && \
    usermod -aG docker jenkins

# Switch back to the jenkins user
USER jenkins