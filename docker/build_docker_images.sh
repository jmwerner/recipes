#!/bin/bash

git_root=`git rev-parse --show-toplevel`


# Build dockerfile with tag
docker build -f $git_root/docker/Dockerfile_recipe_input -t recipe_input .



