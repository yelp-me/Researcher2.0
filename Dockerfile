FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy everything into the container
COPY . /app

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose default Streamlit port
EXPOSE 8501

# Run the app
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
