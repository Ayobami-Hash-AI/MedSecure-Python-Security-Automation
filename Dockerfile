FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY src/ ./src/
COPY sample_logs/ ./sample_logs/

RUN mkdir -p /app/reports \
    && useradd --create-home --uid 10001 medsecure \
    && chown -R medsecure:medsecure /app/reports

USER medsecure

CMD ["python", "src/monitor.py"]