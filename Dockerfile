FROM python:3.11
ENV PYTHONUNBUFFERED=1

# Install GDAL dependencies
RUN apt-get update && \
    apt-get install -y libgdal-dev libgeos-dev

# Set GDAL environment variables (replace with the appropriate paths)
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal:/usr/include/geos
ENV C_INCLUDE_PATH=/usr/include/gdal:/usr/include/geos

WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . .
RUN rm -f requirements.txt

# Run the Django app using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "rqm.wsgi:application"]