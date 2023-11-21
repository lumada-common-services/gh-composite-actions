#!/bin/bash

# Script to manage a static tag on a specific branch in a Git repository
# Usage: ./script_name.sh <branch_name> <static_tag_name>

# Branch to checkout (provided as the first command line argument)
git checkout $1
git pull

# Tag name which is considered static (provided as the second command line argument)
stable_tag_name=$2

# Get the latest tag and commit associated with the tag
latest_commit=$(git rev-list -n 1 $(git describe --tags --abbrev=0))
echo "Latest commit ID on the given branch: $latest_commit"

# Check if the stable tag exists
if git rev-parse -q --verify "refs/tags/$stable_tag_name" >/dev/null; then
    echo "Stable tag found."

    # Get the commit hash for the stable tag
    stable_tag_commit=$(git rev-list -n 1 $stable_tag_name)
    echo "Commit associated with the stable tag '$stable_tag_name': $stable_tag_commit"

    # Check if the stable tag is already pointing to the latest commit
    if [ "$stable_tag_commit" == "$latest_commit" ]; then
        echo "Stable tag already points to the latest commit. Skipping..."
        exit 0
    else
        echo "Updating the commit associated with the stable tag..."
        git tag -f $stable_tag_name $latest_commit
    fi
else
    # Create a new static tag
    echo "Creating a new stable tag '$stable_tag_name'..."
    git tag $stable_tag_name $latest_commit
fi

# Push the updated or new tag only
git push -f origin $stable_tag_name
