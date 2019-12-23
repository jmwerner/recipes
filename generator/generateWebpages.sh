#!/bin/bash

git_root=`git rev-parse --show-toplevel`

# Regenerate webpages
docker run --mount src=$git_root,target=/recipes,type=bind -it generator

if [[ -n "$1" ]]; then
    if [[ "$1" = "--test" ]]; then
        docker run --mount src=$git_root,target=/recipes,type=bind -it recipes_tests
    fi
fi
