# ARG image
# ENV image node:12

FROM node:14

COPY run_code_lint.sh /run_code_lint.sh

RUN chmod +x /run_code_lint.sh

RUN sed -i -e 's/\r$//' /run_code_lint.sh

RUN printenv

# file to execute when the docker container starts up
ENTRYPOINT ["/bin/bash", "/run_code_lint.sh"]
