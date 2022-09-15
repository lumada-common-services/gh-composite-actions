#!/bin/bash

set -eo pipefail
# Uncomment this to download the component scan script.
# bash <(curl -k1 https://detect.synopsys.com/detect.sh -o ./utils/detect.sh)
# chmod 777 ./utils/detect.sh

# This is called when '--help' argument is passed
function usage() {
  local scriptName=$(basename $0)
  cat <<EOF
Usage: $scriptName [parameters]

Required Parameters:

  --blackduck-url=              Blackduck server URL.
  --blackduck-project-version=  The blackduck project version to associate the scan.
  --commit-id=                  Commit ID to use teh value in Docker Tag. It will be automatically taken from the GitHub inbuilt values.
  --build-id=                   Build No
  --blackduck-source-directory= Source Directory of BlackDuck. Usually its the Repo Source Directory and will be automatically detected based on the GitHub In-built values.
  --snippet.matching=           False (or) True. Identifies if Snippet Matching has to be enable dor not during the scan.
  --docker-file=                Dockerfile that has to be built during the build. Its an optional parameter.
  --project-name=               Project Name. This value will be used while running the scan and a project with the same will be created in BlackDuck server.
  --docker.image=               Name of the Docker image
  --docker.tag=                 Docker Tag to be used. This option has to be passed if the option chosen only is to scan the image.
  --pull-image=                 If the image has to be pulled instead of scanning the locally existing image, give this value as Yes.

  --help                 Show help.

EOF
}

# tags them and pushes them to the remote registry.
function handleDockerImages() {
  local localDockerImg="$(docker images --format "{{.ID}} {{.Tag}} {{.Repository}} {{.Repository}}:{{.Tag}}" | grep "$Blackduck_Image" | head -1)"

  if [ $Dockerfile != No ] || [ $PullImage == No ]; then
    echo "Pulling Image is disabled"
    if [[ "$localDockerImg" == "" ]]; then
       echo "Error: $Blackduck_Image doesn't exist"
       exit 1
    fi
  else
    echo "Pulling Image is enabled"
    for dockerRepo in  $(echo "$dockerRepos" | sed "s/,/ /g")
    do
      DockerImgPath="$dockerRepo/$Blackduck_Image"
      echo "Docker image not found locally. Pulling from '$dockerRepo'"
      echo "DockerImgPath: $DockerImgPath"
      if docker pull "${DockerImgPath}"; then
        break
      else
        continue
      fi
    done

    localDockerImg="$(docker images --format "{{.ID}} {{.Tag}} {{.Repository}} {{.Repository}}:{{.Tag}}" | grep "$Blackduck_Image" | head -1)"

    if [[ "$localDockerImg" == "" ]]; then
      echo "Couldn't pull image from any of known docker repositories. Exiting now!"
      exit 1
    else
      Blackduck_Image=${DockerImgPath}
    fi

  fi

  echo "Running Blackduck Scan with the below values:"
  echo "Blackduck_Image: $Blackduck_Image"
  echo "Blackduck_Project: $Blackduck_Project"

  python3 ./scan_docker_image_layer.py $Blackduck_Image ${Blackduck_Project} ${SnippetMatching}

}

function BuildDockerImage() {
  SHA=$commitId
  SHORT_SHA=$(echo $SHA | cut -c 1-8)
  set_version=$blackduckProjectVersion-$buildId-$SHORT_SHA
  tag=$DockerImage:$set_version
  echo "Building the Docker image with the below values:"
  echo "Tag: $tag"
  echo "Dockerfile: $Dockerfile"
  echo "Set_Version: $set_version"
  echo "ProjectName: ${ProjectName}"
  chmod +x $Dockerfile
  docker build -t $tag -f $Dockerfile .
  Blackduck_Image=$tag
}

main() {
  # inputs
  local dockerRegistry=""
  local blackduckUrl=""
  local blackduckUser=""
  local blackduckPassword=""
  local blackduckProjectVersion=""  
  local commitId=""
  local buildId=""
  local blackduckSourceDirectory=""
  local codedxServerUrl=""
  local codedxServerApiKey=""
  local codedxServerProjectId=""
  local SnippetMatching=""  
  local Dockerfile=""  
  local ProjectName=""  
  local DockerImage=""    
  local DockerTag=""      
  local dockerRepos="docker.repo.wal.eng.hitachivantara.com,docker.repo.orl.eng.hitachivantara.com"

  local args=$@

  for i in $@; do
    case $i in
    --help*)
      usage
      exit
      ;;
    --blackduck-url=*)
      blackduckUrl="${i#*=}" && shift
      ;;      
    --blackduck-project-version=*)
      blackduckProjectVersion="${i#*=}" && shift
      ;;
    --commit-id=*)
      commitId="${i#*=}" && shift
      ;;
    --build-id=*)
      buildId="${i#*=}" && shift
      ;;                
    --blackduck-source-directory=*)
      blackduckSourceDirectory="${i#*=}" && shift
      ;;      
    --snippet.matching=*)
      SnippetMatching="${i#*=}" && shift
      ;;
    --docker-file=*)
      Dockerfile="${i#*=}" && shift
      ;;      
    --project-name=*)
      ProjectName="${i#*=}" && shift
      ;;                  
    --docker.image=*)
      DockerImage="${i#*=}" && shift
      ;;
    --docker.tag=*)
      DockerTag="${i#*=}" && shift
      ;;            
    --pull-image=*)
      PullImage="${i#*=}" && shift
      ;;
    *)
      echo "${*} is an unknown parameter"
      exit 1
      ;;
    esac
  done

  if [[ -z ${blackduckUrl} ]]; then
    echo "--blackduck-url= is a required parameter"
    usage
    exit 1
  fi
  if [[ -z ${blackduckProjectVersion} ]]; then
    echo "--project-version= is a required parameter"
    usage
    exit 1
  fi  
  if [[ -z ${commitId} ]]; then
    echo "--commit-id= is a required parameter"
    usage
    exit 1
  fi  
  if [[ -z ${buildId} ]]; then
    echo "--build-id= is a required parameter"
    usage
    exit 1
  fi    
  if [[ -z ${blackduckSourceDirectory} ]]; then
    echo "--blackduck-source-directory= is a required parameter"
    usage
    exit 1
  fi
  if [[ -z ${SnippetMatching} ]]; then
    echo "--snippet.matching= is a required parameter"
    usage
    exit 1
  fi
  if [[ -z ${Dockerfile} ]]; then
    echo "--docker-file= is a required parameter"
    usage
    exit 1  
  fi
  if [[ -z ${ProjectName} ]]; then
    echo "--project-name= is a required parameter"
    usage
    exit 1
  fi
  if [[ -z ${DockerImage} ]]; then
    echo "--docker.image= is a required parameter"
    usage
    exit 1
  fi
  if [[ -z ${DockerTag} ]]; then
    echo "--docker.tag= is a required parameter"
    usage
    exit 1
  fi  
  if [[ -z ${PullImage} ]]; then
    echo "--pull-image= is a required parameter"
    usage
    exit 1
  fi  

  localDockerCont="$(docker ps --format "{{.ID}} {{.Command}} {{.Names}} {{.Image}}" | grep "/run_component_scan" | head -1)"
  ContainerID=$(echo $localDockerCont | cut -d ' ' -f1)
  docker cp $ContainerID:/detect7.sh .
  docker cp $ContainerID:/scan_docker_image_layer.py .
  docker cp $ContainerID:/.restconfig.json .
  chmod +x detect7.sh
  chmod +x scan_docker_image_layer.py
  chmod +x .restconfig.json
  
  echo "Checking the Synopsys Detect Jar file"
  if [ ! -f "$HOME/synopsys-detect/download/synopsys-detect-7.10.0.jar" ]; then
     if [ ! -f "synopsys-detect-7.10.0.jar" ]; then
        echo "Downloading synopsys-detect-7.10.0.jar from Artifactory"
        curl -Lo synopsys-detect-7.10.0.jar https://repo.orl.eng.hitachivantara.com/artifactory/cicd-oci-dev-orl/blackduck-scanner/7.10.0/synopsys-detect-7.10.0.jar
     else
        echo "synopsys-detect-7.10.0.jar already exists locally"
     fi
     mkdir -p "$HOME/synopsys-detect/download"
     cp synopsys-detect-7.10.0.jar "$HOME/synopsys-detect/download/"
  else
    echo "synopsys-detect-7.10.0.jar already exists"
  fi
  
  if [[ "$Dockerfile" != "No" ]]; then
     PullImage="No"
     echo "Dockerfile build is required"
     BuildDockerImage
  else
     Blackduck_Image="${DockerImage}:${DockerTag}"
  fi
  
  Blackduck_Project="${ProjectName}/${DockerImage}/${blackduckProjectVersion}"
  echo "Processing the Docker Image"
  handleDockerImages

  echo "*** The end! ***"
}

# Starting point.
time main "$@"
