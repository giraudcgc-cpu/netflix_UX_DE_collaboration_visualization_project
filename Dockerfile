# Netflix Analytics DE/UX — Dev Container
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy dependency
COPY requirements.txt .

# Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Says which Streamlit port we will use
EXPOSE 8501

# Default command: run Streamlit app
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]

# PowerBi is a windows product and is "outside"