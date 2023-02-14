# Docker-Image Composite Action
#### This composite action can be used to build, push and tag any docker image.
---
Aim to centralize and parameterise the main steps of the bootstrap image builder/publisher workflow :

Available input parameters:
- `ARTIFACTORY`: Name of the artifactory where docker image will get publish.
- `ARTIFACTORY_USER`: Username for the artifactory.
- `ARTIFACTORY_KEY`: Access token for the artifactory.
- `IMAGE_PREFIX`: If a prefix is needed to distinguish git tags for docker image build.
- `DOCKERFILE_PATH`: Path where the dockerfile resides in github repository. 
- `TAG_SUFFIX`: If present, it will be added to the image tag. 
<br><br>
## Usage examples

### 
```
- name: Bootstrap Image Composite action
  uses: lumada-common-services/gh-composite-actions@bootstrap-image
  with:
    ARTIFACTORY: cicd-oci-release-orl.repo.orl.eng.hitachivantara.com         # Name of the artifactory
    ARTIFACTORY_USER: ${{ secrets.LDOS_ARTIFACTORY_USER }} 
    ARTIFACTORY_KEY: ${{ secrets.LDOS_ARTIFACTORY_API_KEY }}
    IMAGE_PREFIX: build-image                                                 # Image prefix for git tag
    DOCKERFILE_PATH: ${GITHUB_WORKSPACE}/.github/bootstrap-image/Dockerfile   # Dockerfile path 
    TAG_SUFFIX:maven                                                          # it's a optional parameter.if present, it will be added to the image tag
          
```
