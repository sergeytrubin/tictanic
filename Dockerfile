FROM python:3.8

ENV INSTALL_PATH /tictanic
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

RUN pip install --upgrade pip

COPY ./Pipfile $WORKDIR/Pipfile
COPY ./Pipfile.lock $WORKDIR/Pipfile.lock

RUN pip install pipenv
RUN cd $WORKDIR && pipenv install --system --deploy

COPY . .

CMD gunicorn -d 0.0.0.0:5000 --access-logfile -  "tictanic.app:create_app()"