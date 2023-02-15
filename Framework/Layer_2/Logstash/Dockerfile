# https://www.docker.elastic.co/
FROM docker.elastic.co/logstash/logstash:7.17.6

USER logstash

ENV LS_JAVA_OPTS=-Xmx1024m

RUN rm -f /usr/share/logstash/pipeline/logstash.conf

ADD logstash.yml /usr/share/logstash/config/
ADD public.conf /usr/share/logstash/pipeline/
ADD jvm.options /usr/share/logstash/config/