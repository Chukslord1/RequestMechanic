# Use an appropriate Python base image
FROM python:3.8

# Install GDAL dependencies
RUN apt-get update && apt-get install -y \
    binutils \
    libproj-dev \
    gdal-bin \
    libgdal-dev \
    libgeos-dev


# Set environment variables required for GDAL
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal
ENV GDAL_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu/libgdal.so.32.3.6.2
ENV GEOS_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu/libgeos_c.so.1.17.1

# Set environment variable to avoid buffering
ENV PYTHONUNBUFFERED=1

WORKDIR /code

# Copy the requirements file and install Python dependencies
COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput
RUN rm -f requirements.txt

# Run the Django app using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "rqm.wsgi:application"]
