# Blackduck Scan GitHub Action

GitHub Action to scan a Docker image, upload the results to the designated Blackduck server to the Project that is defined

There are 3 modes the Script works:

1. Build the Dockerfile(s) & Scan the Docker image(s).
2. Dont build the Dockerfile(s) & Just Scan the Docker image(s).
3. Just pull the image from the Docker repo(s) and Scan the image(s).
(Note: In 1st and 2nd scenarios, Given Docker image is not pulled. However Scan is common in all the scenarios)

1. To build the Dockerfile, pass value to Dockerfile in the strategy section. For ex, find the code snippet below:
      strategy:
      fail-fast: false
        matrix: 
          include:
          - dockerfile: ./assemblies/foundry/dataflow-manager/docker/dataflow-manager/src/main/docker/Dockerfile
            image: dataflow-manager/data-flow-studio
          - dockerfile: ./assemblies/foundry/dataflow-manager/docker/dataflow-manager/src/main/docker-debug/Dockerfile
            image: dataflow-manager/data-flow-studio-migrator
          - dockerfile: ./assemblies/foundry/dataflow-manager/docker/migrator/src/main/docker/Dockerfile
            image: dataflow-manager/data-flow-studio-worker-nodes-provider

2. If Dockerfile build should be avoided and only already built image has to be scanned, Just dont give the dockerfile in the strategy section, Ex below:

    strategy:
      fail-fast: false
      matrix: 
        include:
          - image: data-flow-studio
          - image: data-flow-studio-migrator
          - image: data-flow-studio-worker-nodes-provider

(Note:- In both First and Second scenarios, Pulling the Docker image is automatically disabled. The script looks for the image that exist locally)

3. If the Docker image have to be pulled from the Docker repo(s), Pass the pull_image value as Yes. In the pull_image value is set to yes, building Dockerfile is automatically disabled and the image is pulled from the Dockerrepo(s) and scanned.

(Note:- image value should be passed in any scenario. Its mandatory)

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
  --pull-image=                 Yes (or) No. If the image has to be pulled instead of scanning the locally existing image, give this value as Yes.
