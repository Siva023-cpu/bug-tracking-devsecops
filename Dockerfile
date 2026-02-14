# Step 1: Use official Python image
FROM python:3.11-slim

# Step 2: Set working directory
WORKDIR /app

# Step 3: Copy requirements first (for caching)
COPY requirements.txt .

ENV MAIL_USERNAME=mssk6304445254@gmail.com
ENV MAIL_PASSWORD=vnjuaxvyllatrdvm

# Step 4: Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy application code
COPY . .

# Step 6: Expose Flask port
EXPOSE 5000


# Step 7: Run the application
CMD ["gunicorn", "wsgi:app", "--bind", "0.0.0.0:5000"]


