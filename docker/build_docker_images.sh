#!/bin/bash

export parent_git_root=`git rev-parse --show-toplevel`

# Build dockerfile with tag
docker build -f $parent_git_root/docker/Dockerfile_recipes_input -t recipes_input .

docker build -f $parent_git_root/docker/Dockerfile_recipes_generator -t recipes_generator .

docker build -f $parent_git_root/docker/Dockerfile_recipes_tests -t recipes_tests .

