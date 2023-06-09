# this is the maven image used in the building process
# cd ..
# docker build -t myproject-maven:3.8.4-jdk-17-slim -f docker/Maven.Dockerfile .
# docker tag myproject-maven:3.8.4-jdk-17-slim registry.xxxx.com/mynamespace/myproject-maven:3.8.4-jdk-17-slim

FROM maven:3.8.4-openjdk-17-slim

MAINTAINER david

WORKDIR /data/myproject-api-service

COPY . .

# copy internal m2 settings to maven builder image:
COPY docker/settings.xml /root/.m2/

# precache all maven dependencies to ~/.m2
RUN mvn -Dmaven.test.skip clean package && cd /data && rm -rf /data/myproject-api-service

ENTRYPOINT ["/usr/local/bin/mvn-entrypoint.sh"]
CMD ["mvn"]
