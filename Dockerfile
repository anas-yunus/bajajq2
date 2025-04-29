# Use the official Python image
FROM python:3.9-slim

# Install Tesseract OCR
RUN apt-get update && apt-get install -y tesseract-ocr

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app/

# Check the contents of the app directory
RUN ls -la /app

# Install the required Python packages
RUN pip install --no-cache-dir -r /app/requirements.txt

# Expose port 8080
EXPOSE 8080

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
