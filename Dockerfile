FROM python:3.5
ENV PYTHONUNBUFFERED 1
RUN git clone https://github.com/a0919610611/Library.git
WORKDIR Library
RUN pip install -r requirements.txt
RUN ./init.sh
CMD ["python3","manage.py" ,"runserver","0.0.0.0:8080"]
