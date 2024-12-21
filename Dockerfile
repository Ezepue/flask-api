# Step 1: Use an official Python runtime as a parent image
FROM python:3.10-slim

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy the current directory contents into the container
COPY . /app

# Step 4: Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Expose the port the app runs on
EXPOSE 5000

# Step 6: Define the command to run the application
CMD ["flask", "run", "--host=0.0.0.0"]
