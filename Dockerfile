
FROM python:3.12-bookworm

COPY requirements.txt requirements.txt
#COPY .sqlpass .sqlpass
COPY phpmyadmin_sql_backup.py phpmyadmin_sql_backup.py
COPY get_db_docker.sh get_db_docker.sh

#RUN apt-get install -y wget vim git zip unzip zlib1g-dev libzip-dev libpng-dev libicu-dev
RUN pip install -r requirements.txt

CMD ["./get_db_docker.sh"]
