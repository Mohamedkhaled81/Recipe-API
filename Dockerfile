# Base Image or the parent image as an initial layer with specific tag
FROM python:3.9-alpine3.13

# Define the maintainer
LABEL maintainer="Mohamed Khaled"

# Recommended when you are running Python in a docker container
# What it does is telling python that you don't want to buffer the output
# The output from python will be printed directly to the console, which prevents any delays of messages
# getting from our python running application to the screen so we can see the logs immediatly in the screen as they running
ENV PYTHONUNBUFFERED 1

# Copy our requirments on a text file from our local machine to /tmp/requirment.txt [ into the docker container ]
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

# The default directory that we are going to use it in any sybsequent instructions as ADD/COPY/RUN
WORKDIR /app

# Copy the app directory [ the django app that we are going to make in a moment ] into /app inside the container
COPY ./app .


# This exposes Port 8000 from our container to our machine when we run the container
# it allows us to access that port on container that's runningfrom our image
# and this way we can connect to the django development server 
EXPOSE 8000

ARG DEV=false
# Running Scripts, We spicify a single run commanad and we break it down onto multiple lines using this \ and the reason for that
# is to make the building of our images as a bit more efficient
# Because it doesnt create so many layers on our system
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt; \
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# This updates the environment variable inside the image and we are updating the path environment variable
# It defines all of the data trees where executables can be run 
ENV PATH="/py/bin:$PATH"

# Switching the image's user to django-user any time that you run something from this image
# It's going to run as django-user it's not going to have that full root privileges that we need for setting up the Docker Image 
USER django-user
