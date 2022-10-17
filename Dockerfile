ARG image=node:14
FROM ${image}

ARG LINT_IMAGE

ENV NPM_CONFIG_LOGLEVEL warn
ENV PORT=3000
ENV LINT_IMAGE=$LINT_IMAGE

COPY run_code_lint.sh /run_code_lint.sh

RUN chmod +x /run_code_lint.sh

RUN sed -i -e 's/\r$//' /run_code_lint.sh

RUN printenv

# file to execute when the docker container starts up
ENTRYPOINT ["/bin/bash", "/run_code_lint.sh"]
