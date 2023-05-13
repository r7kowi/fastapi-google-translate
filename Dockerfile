FROM python:3.10-slim

WORKDIR /app
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .

EXPOSE 8000

#run the app with uvicorn
CMD ["uvicorn", "api.translateAPI:app", "--host", "0.0.0.0", "--port", "8000"]




