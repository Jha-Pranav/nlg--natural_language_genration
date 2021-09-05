# base image
FROM gramener/gramex:latest

RUN mkdir /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

RUN python -m spacy download en_core_web_sm


#---------------- ISOLATED BUILD INSTRUCTIONS ---------------------

# You have to be in the root directory of nlg-service while running the command. This is where the Dockerfile is present.

# Build docker image (allow build from cache):
# docker build -t nlg-service .
#         OR
# Build docker image (strict rebuild without using cache):
# docker build --no-cache -t nlg-service .


# Run the docker image using command: 
# docker run -it -p 9988:9988 -v %cd%/app:/app -w /app nlg-service gramex