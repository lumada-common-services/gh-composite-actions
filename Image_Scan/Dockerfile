# Base image 
FROM pnt-docker.repo.orl.eng.hitachivantara.com/blackducksoftware/detect:7.14.0

RUN	apk add --no-cache \
  bash \
  ca-certificates \
  curl \
  jq

# updates coreutils
RUN apk add --update coreutils
RUN apk update && apk add --no-cache docker-cli
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools
RUN pip3 install blackduck
RUN pip3 install autopep8

# Copies scripts to the filesystem 
COPY run_component_scan.sh /run_component_scan.sh
COPY detect7.sh /detect7.sh
COPY scan_docker_image_layer.py /scan_docker_image_layer.py
COPY .restconfig.json /.restconfig.json

# change permission to execute the script and
RUN chmod +x /run_component_scan.sh

# file to execute when the docker container starts up
ENTRYPOINT ["/run_component_scan.sh"]
