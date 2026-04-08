# 1. Use an official Python image
FROM python:3.10-slim

# 2. Set the working directory
WORKDIR /app

# 3. Copy everything from your computer into the container
COPY . .

# 4. Install the libraries
RUN pip install --no-cache-dir -r requirements.txt

# 5. Set the PYTHONPATH so the container can find 'models' and 'server'
ENV PYTHONPATH=/app

# 6. Run the app on port 7860 (Hugging Face's default)
CMD ["python", "app.py"]
