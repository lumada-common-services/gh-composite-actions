FROM sonarsource/sonar-scanner-cli:4.7

COPY run_sonar.sh /run_sonar.sh

RUN chmod +x /run_sonar.sh

RUN sed -i -e 's/\r$//' /run_sonar.sh

# file to execute when the docker container starts up.
ENTRYPOINT ["/run_sonar.sh"]
