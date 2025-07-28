FROM python:3.13.2

# Install ffmpeg and git
RUN apt-get update && \
    apt-get install -y ffmpeg git && \
    rm -rf /var/lib/apt/lists/*

# Configure git with rebase true
RUN git config --global pull.rebase true

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create startup script that pulls latest changes and runs the app
RUN echo '#!/bin/bash\nif [ -d ".git" ]; then\n  echo "Pulling latest changes..."\n  git pull\nfi\necho "Starting application..."\npython3 main.py' > start.sh && \
    chmod +x start.sh

# Default command
CMD ["./start.sh"]
