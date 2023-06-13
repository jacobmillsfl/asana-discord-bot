FROM python:3

# Set shell
SHELL ["/bin/bash", "-c"]

# Install dependencies
RUN apt update
RUN apt install -y python3-dev build-essential libssl-dev libffi-dev python3-setuptools
RUN apt remove -y uwsgi

# Create app user
RUN useradd --create-home --shell /bin/bash appuser
WORKDIR /home/appuser
USER appuser

# Make an app directory
# RUN mkdir ./app
# WORKDIR ./app

# Install Python requirements
# RUN python3 -m venv /asanaenv
# RUN source /asanaenv/bin/activate
RUN pip install --upgrade pip
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
RUN pip uninstall uwsgi
RUN pip install uwsgi

# Copy the code
COPY app.py ./app.py
COPY uwsgi.ini ./uwsgi.ini
COPY wsgi.py ./wsgi.py
COPY init_script.sh ./init_script.sh
COPY src ./src

# Expose port
EXPOSE 5000

ENV PATH="${PATH}:/home/appuser/.local/bin/" 

# Run API
#CMD ["python3", "./app.py"]
#CMD ["uwsgi", "--ini", "uwsgi.ini", "--socket", "0.0.0.0:5000", "--enable-threads", "--protocol=http", "-w", "wsgi:app"]
CMD ["bash", "init_script.sh"]