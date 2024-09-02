# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install necessary packages
RUN apt-get clean && apt-get update && \
    apt-get install -y wget curl unzip gnupg2 libnss3 libgconf-2-4 --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get clean && apt-get update && \
    apt-get install -y libxi6 libxrandr2 libxss1 libxcursor1 --no-install-recommends && \
    rm -rf /var/lib/apt/lists/* \

RUN apt-get clean && apt-get update && \
    apt-get install -y libxcomposite1 libasound2 libxdamage1 libxtst6 --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get clean && apt-get update && \
    apt-get install -y libglib2.0-0 xvfb x11-xkb-utils xfonts-100dpi --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*




# Install Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Install ChromeDriver
RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip

# Set display port for Xvfb
ENV DISPLAY=:99

# Set working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Install web driver manager
RUN pip install webdriver-manager

# Expose the port the app runs on
EXPOSE 8080

# Run the bot
CMD ["python", "main.py"]
