# Dockerfile, image, container
# - dockerfile = blueprint for creating an image
# - image      = executable package with all dependencies for container
# - container  = The process that runs on the computer


#Set python version
FROM python:3.9

#Add main.py to our base directory in the image
ADD main.py .

#Install dependencies
RUN pip install requests beautifulsoup4

#Command to run python script
CMD ["python", "./main.py"]