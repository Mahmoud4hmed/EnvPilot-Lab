FROM python:3.13.14-slim-bookworm
RUN pip install --no-cache-dir ansible-core==2.21.5
WORKDIR /work
CMD ["ansible-playbook", "-i", "localhost,", "-c", "local", "playbook.yml"]
