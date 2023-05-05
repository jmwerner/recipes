#!/bin/bash

git_root=`git rev-parse --show-toplevel`

# Access input website on localhost:8080
docker run -p 8080:8080 --mount src=$git_root,target=/recipes,type=bind -it recipes_input /bin/bash -c "pwd | R -e 'setwd(\"recipes/recipeInput\"); getwd(); library(shiny); shiny::runApp(\"inputApp.R\", port=8080, host=\"0.0.0.0\", launch.browser = FALSE)'"
