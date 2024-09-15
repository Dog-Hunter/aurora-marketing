# Use the official Python 3.12.5 image as the base image
FROM python:3.12.5-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the bot code into the container
COPY . .

# Expose the port that the bot will run on (if needed)
EXPOSE 80

# Command to run the bot
CMD ["python", "__init__.py"]