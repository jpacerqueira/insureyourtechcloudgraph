#
FROM neo4j:latest
#

EXPOSE 7473/tcp
EXPOSE 7474/tcp
EXPOSE 7687/tcp

ENTRYPOINT ["tini" "-g" "--" "/startup/docker-entrypoint.sh"]

CMD ["neo4j"]
#
