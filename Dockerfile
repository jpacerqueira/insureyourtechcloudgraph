#
FROM neo4j:latest
#
run ls $HOME

EXPOSE map[7473/tcp:{} 7474/tcp:{} 7687/tcp:{}]

ENTRYPOINT ["tini" "-g" "--" "/startup/docker-entrypoint.sh"]

CMD ["neo4j"]
#
