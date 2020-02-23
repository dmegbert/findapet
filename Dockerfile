FROM python:3.6.5

RUN apt-get update && apt-get install

# Run basic pip install of flask packages before checking requirements file. Add more here if you want to cache them.
RUN pip install Click==7.0 && pip install Flask==1.0.2 && pip install itsdangerous==1.1.0 && \
    pip install Jinja2==2.10 && pip install MarkupSafe==1.1.0 && pip install psycopg2==2.7.6.1 && \
    pip install Werkzeug==0.14.1

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./ /app

WORKDIR /app

EXPOSE 5000

CMD ["python", "./findapet_api.py"]
