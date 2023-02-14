# https://www.docker.elastic.co/
# https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html#docker-cli-run-dev-mode

FROM docker.elastic.co/elasticsearch/elasticsearch:7.15.1

COPY elasticsearch.yml /usr/share/elasticsearch/config/
COPY jvm-heap-size.options /usr/share/elasticsearch/config/jvm.options.d/

EXPOSE 9200 9300
