FROM python:3.9-slim

LABEL author="John Doe"

ENV PORT=8080

COPY server.py /server.py

CMD ["python", "/server.py"]
