FROM python:3.12
RUN apt-get update && apt-get install -y git
RUN git clone --branch List_10 https://github.com/Justna2024/SoftwareEngineeringLab4.git
WORKDIR /SoftwareEngineeringLab4
RUN pip install -r requirements.txt
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
EXPOSE 9999
CMD ["python", "manage.py", "runserver", "0.0.0.0:9999"]