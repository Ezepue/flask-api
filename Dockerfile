# Start with a base Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy your project files to the working directory
COPY . /app

# Install the necessary Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your app will run on (e.g., 5000)
EXPOSE 5000

# Command to start your Flask app
CMD ["python", "app.py"]
