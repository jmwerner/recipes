# recipes

This is a repository and (soon coming) website to store our family's favorite recipes instead of simply having a chrome folder of 100+ old bookmarks. As with most things, this was inspired by a [repo from Hadley](https://github.com/hadley/recipes), but I wanted to write it by hand for sport instead of forking.

Because github pages only supports static content and I'm too cheap to pay for hosting and enable the use of a database, I will be deviating slightly from Hadley's setup with the following plan.

### Website generation plan
1. Local app that writes .json recipe file
    - Recipe .json is placed into correct folder that will indicate how it should be categorized within the website 
    - e.g. desserts -> cakes -> tresLechesCake.json
2. Local build script that takes all .json recipe files and generates a webpage that can be pushed to gh-pages 
