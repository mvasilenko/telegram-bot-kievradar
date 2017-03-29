FROM python:3
COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt
COPY . /tmp/
CMD [ "python", "/tmp/telegram_bot_kievradar.py" ]
