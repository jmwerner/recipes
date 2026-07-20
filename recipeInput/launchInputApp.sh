#!/bin/bash

git_root=`git rev-parse --show-toplevel`

# Access input website on localhost:8080
docker run -p 3838:3838 --mount src=$git_root,target=/recipes,type=bind -it recipes_input