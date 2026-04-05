# Use Python base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (for Gradio / HF Space)
EXPOSE 7860

# Run app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]