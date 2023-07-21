FROM python:3.11
ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y \
    gcc \
    libgdal-dev \
    gdal-bin
# ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
# ENV C_INCLUDE_PATH=/usr/include/gdal
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . .
RUN rm -f requirements.txt