FROM python:3.9-slim

WORKDIR /app

# Copy the requirements file and install dependencies
COPY ./App/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY ./App /app
COPY ./Database /app/Database

# Expose port 5000
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
