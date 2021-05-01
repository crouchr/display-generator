# based on Debian Buster
FROM python:3.8.5-buster
LABEL author="Richard Crouch"
LABEL description="Display Generator Daemon"

# generate logs in unbuffered mode
ENV PYTHONUNBUFFERED=1

RUN apt -y update
#RUN apt -y upgrade
RUN apt -y install joe nmap build-essential libasound2 libasound2-dev

# Install Python dependencies
RUN pip3 install pipenv
COPY Pipfile* ./
RUN pipenv install --system --deploy

# Copy application and files
RUN mkdir /app
COPY app/*.py /app/
WORKDIR /app

# run Python unbuffered so the logs are flushed
CMD ["python3", "-u", "display_generator_main.py"]
