FROM python:3.12-slim-bullseye
WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
ARG POSTGRES_USER=yogesh
ARG POSTGRES_PASSWORD={h94h@nb!gn}
ARG POSTGRES_DB=inventory
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    gnupg \
    && curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor | tee /etc/apt/trusted.gpg.d/pgdg.gpg >/dev/null \
    && echo "deb http://apt.postgresql.org/pub/repos/apt bullseye-pgdg main" > /etc/apt/sources.list.d/pgdg.list \
    && apt-get update && apt-get install -y \
    postgresql-17 \
    postgresql-contrib-17 \
    apache2 \
    libapache2-mod-wsgi-py3 \
    certbot \
    python3-certbot-apache \
    && apt-get clean
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN service postgresql start && \
    su - postgres -c "psql -c \"CREATE USER $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASSWORD';\"" && \
    su - postgres -c "psql -c \"CREATE DATABASE $POSTGRES_DB OWNER $POSTGRES_USER;\"" && \
    service postgresql stop
RUN mkdir -p /app/logs && chmod -R 777 /app/logs
RUN mkdir -p /app/Files && chmod -R 755 /app/Files
RUN python manage.py collectstatic --noinput
COPY apache2.conf /etc/apache2/sites-available/000-default.conf
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf
RUN a2enmod proxy proxy_http ssl rewrite headers 
# Enable rewrite module
EXPOSE 80 443
CMD ["sh", "-c", "service postgresql start && python manage.py migrate && gunicorn inventory_system.wsgi:application --bind 127.0.0.1:8000 --workers 2 & apache2ctl -D FOREGROUND"]


