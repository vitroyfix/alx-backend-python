# Dockerfile for a custom Jenkins image with Python to fix the "python3: not found" error

FROM jenkins/jenkins:lts-jdk21-alpine

# Switch to root to install packages
USER root

# Install Python3, pip, git, and Docker CLI using Alpine's package manager 'apk'
# Also upgrade existing packages for security
RUN apk update && \
    apk upgrade && \
    apk add --no-cache python3 py3-pip git docker-cli && \
    rm -rf /var/cache/apk/*

# Switch back to the jenkins user
USER jenkins