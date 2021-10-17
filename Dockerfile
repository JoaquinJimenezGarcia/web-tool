FROM python:3

WORKDIR /usr/src/app

RUN apt-get update && apt-get -y install cron vim

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

# Copy hello-cron file to the cron.d directory
COPY info-cron /etc/cron.d/info-cron
 
# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/info-cron

# Apply cron job
RUN crontab /etc/cron.d/info-cron
 
# Create the log file to be able to run tail
RUN touch /var/log/cron.log
 
# Run the command on container startup
CMD cron && python3 api.py
