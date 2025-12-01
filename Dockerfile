FROM python:3.11-alpine

# install deps
RUN apk add --no-cache build-base libffi-dev

WORKDIR /app
COPY app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app /app

# non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

EXPOSE 80
CMD ["python", "app.py"]

