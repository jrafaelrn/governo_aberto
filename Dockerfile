FROM ubuntu:22.04

WORKDIR /app
COPY ./requirements.txt /app

# Update and install python3.10.0 and pip
RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y install python3 python3-pip

# Install requirements
RUN pip install -r requirements.txt


# Run the application
ENTRYPOINT ["python3", "src/bot.py"]