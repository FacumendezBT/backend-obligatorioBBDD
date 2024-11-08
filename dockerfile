FROM python:bookworm
WORKDIR /bd_backend/app
COPY requirements.txt .

RUN apt update && apt upgrade -y && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Specify the command to run the application
CMD ["fastapi", "run", "src/main.py"]
