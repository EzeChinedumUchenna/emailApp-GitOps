# our base image
# FROM alpine:3.5

# Install python and pip
# RUN apk add --update py2-pip

# install Python modules needed by the Python app
# COPY requirements.txt /usr/src/app/
#RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt

# copy files required for the app to run
#COPY app.py /usr/src/app/
#COPY templates/index.html /usr/src/app/templates/

# tell the port number the container should expose
#EXPOSE 5000

# run the application
#CMD ["python", "/usr/src/app/app.py"]



FROM python:3.8
  
# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "app.py"]
