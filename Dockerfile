FROM python:3
ADD . .
CMD [ "python", "epidemic.py" ]