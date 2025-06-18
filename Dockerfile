# გამოიყენეთ ოფიციალური Python-ის რანტაიმი როგორც მშობელი სურათი (Use an official Python runtime as a parent image)
FROM python:3.10-slim-buster

# გარემოს ცვლადების დაყენება (Set environment variables)
ENV PYTHONUNBUFFERED 1

# სამუშაო დირექტორიის დაყენება (Set work directory)
WORKDIR /app

# სისტემური დამოკიდებულებების დაყენება (Install system dependencies)
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    libjpeg-dev \
    zlib1g-dev \
    netcat-traditional && rm -rf /var/lib/apt/lists/*

# requirements ფაილის კოპირება (Copy requirements file)
COPY requirements.txt /app/

# Python-ის დამოკიდებულებების დაყენება (Install Python dependencies)
RUN pip install --no-cache-dir -r requirements.txt --trusted-host pypi.python.org --trusted-host pypi.org --trusted-host files.pythonhosted.org

# პროექტის კოპირება (Copy project)
COPY . /app/

# პორტის გამოაშკარავება (Expose port)
EXPOSE 8000

# სტატიკური ფაილების შეგროვება (Run collectstatic for static files)
# RUN python manage.py collectstatic --noinput

# Django აპლიკაციის გაშვება (Run the Django application)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]