# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY ./apps/Backend/requirements.txt .
RUN pip install -r requirements.txt

# Copy SSL certificates
COPY ./nginx/ssl /etc/nginx/ssl

# Copy the rest of the application code into the container
COPY . .

# Expose the port that Flask runs on
EXPOSE 5000

# Command to run the application
CMD ["python3", "-m", "flask", "run", "--host=hair-orama.local", "--port=5000", "--cert=/etc/nginx/ssl/hair-orama.local.crt", "--key=/etc/nginx/ssl/hair-orama.local.key"]
# CMD [ "python3", "-m" , "app.py"]
