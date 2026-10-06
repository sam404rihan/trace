# The Trace web server. Your code still runs in a separate, locked-down sandbox
# container per Run (runner/Dockerfile); this image only needs Python and the Docker CLI
# to start those sandboxes through the host's Docker socket.
FROM python:3.12-slim

COPY --from=docker:27-cli /usr/local/bin/docker /usr/local/bin/docker
COPY --from=docker/buildx-bin:latest /buildx /usr/libexec/docker/cli-plugins/docker-buildx

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# The project itself is bind-mounted at /app (see docker-compose.yml), so edits to
# the course, the web UI and your saved work all live on your machine.
WORKDIR /app
EXPOSE 8000
CMD ["python", "server.py", "--host", "0.0.0.0", "--no-browser"]
