# Stage 1: Build the intermediate image
FROM python:3.9 AS builder

# Set the working directory
WORKDIR /app

# Copy your Scrapy project files into the container
COPY ./flock_webscraper .

# Install Scrapy and any other dependencies using pip
RUN pip install --upgrade pip \
    && pip install --user scrapy


# Stage 2: Create the final image
FROM python:3.9-slim

# Copy the installed Scrapy from the builder image
COPY --from=builder /root/.local /root/.local

# Copy your Scrapy project files into the container
COPY --from=builder /app /app

# Set the working directory
WORKDIR /app

# Make sure the scripts in .local are used
ENV PATH=/root/.local/bin:$PATH

# Run the Scrapy spider using the environment variables
CMD ["scrapy", "runspider", "flock_spider.py"]
