FROM python:2
COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt
COPY . /tmp/
CMD [ "python", "/tmp/telegram-bot-kievradar.py" ]
