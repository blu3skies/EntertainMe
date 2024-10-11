FROM python:3.12-slim

WORKDIR /app

# Copy the app code into the container
COPY . /app

# Copy wait-for-it.sh into the container
COPY wait-for-it.sh /usr/local/bin/wait-for

# Make the wait-for script executable
RUN chmod +x /usr/local/bin/wait-for

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run Flask with wait-for
CMD ["wait-for", "db:3306", "--", "flask", "run", "--host=0.0.0.0"]
