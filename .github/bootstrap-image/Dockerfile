FROM one.hitachivantara.com/docker/sonarsource/sonar-scanner-cli:5.0.1

COPY run_sonar.sh /run_sonar.sh

RUN chmod +x /run_sonar.sh

RUN sed -i -e 's/\r$//' /run_sonar.sh

# file to execute when the docker container starts up
ENTRYPOINT ["/run_sonar.sh"]
