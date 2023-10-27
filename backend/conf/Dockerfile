FROM python:3.11
ENV PYTHONUNBUFFERED 1

COPY conf/requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

RUN rm -rf /var/cache/apk/* \
           /root/.cache/* \
           /usr/lib/python*/ensurepip \
           /tmp/*

RUN python -m spacy download en_core_web_sm

WORKDIR /code