FROM maven:3.8.6-jdk-11

COPY run_maven_build.sh /run_maven_build.sh

RUN printenv
RUN chmod +x /run_maven_build.sh

RUN sed -i -e 's/\r$//' /run_maven_build.sh

# file to execute when the docker container starts up
ENTRYPOINT ["/bin/bash", "/run_maven_build.sh"]
