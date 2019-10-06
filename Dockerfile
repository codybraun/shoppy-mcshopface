FROM python
RUN mkdir /usr/shoppy
WORKDIR /usr/shoppy
COPY . /usr/shoppy
RUN pip install -r requirements.txt
EXPOSE 5000
CMD FLASK_APP=shoppy.py flask run --host=0.0.0.0
