FROM python

WORKDIR /open_brewery_project/
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD python -m pytest /open_brewery_project/tests