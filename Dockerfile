# Use an appropriate Python base image
FROM python:3.9

# Install GDAL dependencies
RUN apt-get update && apt-get install -y \
    binutils \
    libproj-dev \
    gdal-bin \
    libgdal-dev


# Set environment variables required for GDAL
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal
ENV GDAL_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu/libgdal.so

# Set environment variable to avoid buffering
ENV PYTHONUNBUFFERED=1

# Install GDAL dependencies
RUN apt-get update && \
    apt-get install -y libgdal-dev libgeos-dev

# Set GDAL environment variables (replace with the appropriate paths)
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal:/usr/include/geos
ENV C_INCLUDE_PATH=/usr/include/gdal:/usr/include/geos

WORKDIR /code

# Copy the requirements file and install Python dependencies
COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . .
RUN rm -f requirements.txt

# Run the Django app using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "rqm.wsgi:application"]
