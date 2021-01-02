library(shiny)
library(jsonlite)

numberOfIngredients = 15

numberOfDirections = 10

ingredient_field_names = c(paste0("ingredient_number_", 1:numberOfIngredients),
                           paste0("ingredient_units_", 1:numberOfIngredients),
                           paste0("ingredient_name_", 1:numberOfIngredients),
                           paste0("ingredient_category_", 1:numberOfIngredients))

directions_field_names = paste0("directions_", 1:numberOfDirections)

# which fields get saved 
fieldsAll = c("recipeName", "recipeCategory", "recipeSource", "recipeLink", 
              "notes", "winePairing", "glassType",
              ingredient_field_names, directions_field_names)

# which fields are mandatory
fieldsMandatory = c("recipeName", "recipeCategory", "directions_1")

# add an asterisk to an input label
labelMandatory = function(label){
    tagList(label, span("*", class = "mandatory_star"))
}

# get current Epoch time
epochTime = function(){
    return(as.integer(Sys.time()))
}

humanTime = function(){
    format(Sys.time(), "%Y%m%d-%H%M%OS")
}

removeSpaces = function(input){
    gsub("[[:blank:]]", "", input)
}

textareaInput = function(inputId, label, value = "", placeholder = "", rows = 2){
    tagList(
        div(strong(label), style = "margin-top: 5px;"),
        tags$style(type = "text/css", "textarea {width:100%; margin-top: 5px;}"),
        tags$textarea(id = inputId, placeholder = placeholder, rows = rows, value)
    )
}

titleCase = function(x){
    s <- strsplit(as.character(x), " ")[[1]]
    paste(toupper(substring(s, 1,1)), substring(s, 2), sep = "", collapse = " ")
}

# save the results to a json file
# This code is very dependent on id names, be careful when
#  changing structure of the app! 
saveData = function(data){

    data = data.frame(data)

    system(paste0("mkdir -p ../allRecipes/", removeSpaces(data$recipeCategory)))

    fileName = paste0(removeSpaces(titleCase(data$recipeName)), ".json")
    filePath = file.path(paste0("../allRecipes/", removeSpaces(data$recipeCategory)), fileName) 

    ingredientsSubset = data[,grepl("ingredient", names(data))]

    nameFrame = do.call(rbind, strsplit(names(ingredientsSubset), "_"))
    maxIngredientNumber = max(as.numeric(nameFrame[,3]))
    
    ingredientsList = list()
    for(i in 1:maxIngredientNumber){
        ingredientsList[[i]] = list(
            "number" = ingredientsSubset[[paste0("ingredient_number_", i)]],
            "units" = ingredientsSubset[[paste0("ingredient_units_", i)]],
            "name" = ingredientsSubset[[paste0("ingredient_name_", i)]],
            "category" = ingredientsSubset[[paste0("ingredient_category_", i)]]
        )        
    }

    directionsList = list()
    for(i in 1:numberOfDirections){
        single_direction = eval(parse(text = paste0("data$directions_", i)))
        if(!is.null(single_direction)){
            directionsList[[i]] = single_direction
        }
    }

    output = list(
        "recipeName" = data$recipeName[[1]],
        "recipeCategory" = data$recipeCategory[[1]],
        "recipeSource" = data$recipeSource[[1]],
        "recipeLink" = data$recipeLink[[1]],
        "directions" = toJSON(directionsList),
        "timestamp" = data$timestamp[[1]],
        "notes" = data$notes[[1]],
        "winePairing" = data$winePairing[[1]],
        "glassType" = data$glassType[[1]],
        "ingredients" = toJSON(ingredientsList)
    )

    outputJSON = toJSON(output, pretty = 4)

    write(outputJSON, file = filePath)

}

# directory where responses get stored
responsesDir = file.path("responses")

# CSS to use in the app
appCSS =
  ".mandatory_star { color: red; }
   .shiny-input-container { margin-top: 25px; }
   #submit_msg { margin-left: 15px; }
   #error { color: red; }
   body { background: #fcfcfc; }
   #header { background: #fff; border-bottom: 1px solid #ddd; margin: -20px -15px 0; padding: 15px 15px 10px; }
  "


unitsOptions = list(" " = "",
                    "Cup(s)" = "Cup(s)", 
                    "Tablespoon(s)" = "Tablespoon(s)",
                    "Teaspoon(s)" = "Teaspoon(s)",
                    "Pound(s)" = "Pound(s)", 
                    "Whole" = "Whole",
                    "Can(s)" = "Can(s)",
                    "Ounce(s)" = "Ounce(s)",
                    "Clove(s)" = "Clove(s)",
                    "Pinch(es)" = "Pinch(es)",
                    "Dash(es)" = "Dash(es)",
                    "Bottle(s)" = "Bottle(s)")

glassesOptions = list(" " = "",
                      "coffee-cup" = "coffee-cup",
                      "coffee-irish" = "coffee-irish",
                      "coupe" = "coupe",
                      "flute" = "flute",
                      "hurricane" = "hurricane",
                      "margarita" = "margarita",
                      "martini" = "martini",
                      "mug" = "mug",
                      "pint" = "pint",
                      "port" = "port",
                      "rocks" = "rocks",
                      "shot" = "shot",
                      "snifter" = "snifter",
                      "tiki" = "tiki",
                      "weiss" = "weiss",
                      "wine" = "wine")


shinyApp(
  ui = fluidPage(
    shinyjs::useShinyjs(),
    shinyjs::inlineCSS(appCSS),
    title = "Recipe Input App",


    titlePanel("Recipe Input App"),

    hr(),

    wellPanel(
        fluidRow(
            textInput("recipeName", label = labelMandatory("Recipe Name"), value = "")
        )
    ),

    wellPanel(
        fluidRow(
            textInput("recipeCategory", label = labelMandatory("Recipe Category"), value = "")
        )
    ),

    wellPanel(
        fluidRow(
            textInput("recipeSource", label = "Recipe Source (person)", value = "")
        )
    ),

    wellPanel(
        fluidRow(
            textInput("recipeLink", label = "Recipe Link (url)", value = "")
        )
    ),


    titlePanel("Ingredients"),

    wellPanel(
        fluidRow(
            column(2,
                mainPanel("#")
            ),
            column(3,
                mainPanel("Units")
            ),
            column(3,
                mainPanel("Ingredient")
            ),
            column(3,
                mainPanel("IngredientCategory")
            )
        ),
        lapply(1:numberOfIngredients, function(i){
            fluidRow(
                column(2,
                    textInput(paste0("ingredient_number_", i), label = "", value = "")
                ),
                column(2,
                    selectInput(paste0("ingredient_units_", i), label = "", 
                        choices = unitsOptions, 
                        selected = "")
                ),
                column(3,
                    textInput(paste0("ingredient_name_", i), label = "", value = "")
                ),
                column(3,
                    textInput(paste0("ingredient_category_", i), label = "", value = "")
                )
            )
        })
    ),

    titlePanel("Directions"),

    wellPanel(
        lapply(1:numberOfDirections, function(i){
            textareaInput(paste0("directions_", i), label = i)
        })
    ),

    titlePanel("Wine Pairing"),

    wellPanel(
        tags$textarea(id="winePairing", rows=1, cols=100, "")

    ),

    titlePanel("Glass Type (cocktails only)"),

    wellPanel(
        selectInput("glassType", label = "", 
                        choices = glassesOptions, 
                        selected = "")
    ),

    titlePanel("Notes"),

    wellPanel(
        tags$textarea(id="notes", rows=10, cols=100, "")

    ),

    actionButton("submit", "Submit", class = "btn-primary"),
        
    br(),
    br(),

    shinyjs::hidden(
      span(id = "submit_msg", "Submitting..."),
        div(id = "error",
            div(br(), tags$b("Error: "), span(id = "error_msg"))
        )
      ),

    shinyjs::hidden(
      div(
        id = "thankyou_msg",
        h3("Thanks, your response was submitted successfully!"),
        actionLink("submit_another", "Submit another response")
      )
    )
  ),

  server = function(input, output, session){
    
    # Enable the Submit button when all mandatory fields are filled out
    observe({
      mandatoryFilled =
        vapply(fieldsMandatory,
               function(x){
                 !is.null(input[[x]]) && input[[x]] != ""
               },
               logical(1))
      mandatoryFilled = all(mandatoryFilled)
      
      shinyjs::toggleState(id = "submit", condition = mandatoryFilled)
    })
    
    # Gather all the form inputs (and add timestamp)
    formData = reactive({
      data = sapply(fieldsAll, function(x) input[[x]])
      data = c(data, timestamp = humanTime())
      data = t(data)
      data
    })    
    
    # When the Submit button is clicked, submit the response
    observeEvent(input$submit, {
      
      # User-experience stuff
      shinyjs::disable("submit")
      shinyjs::show("submit_msg")
      shinyjs::hide("error")
      
      # Save the data (show an error message in case of error)
      tryCatch({
        saveData(formData())
        shinyjs::reset("form")
        shinyjs::hide("form")
        shinyjs::show("thankyou_msg")
      },
      error = function(err){
        shinyjs::html("error_msg", err$message)
        shinyjs::show(id = "error", anim = TRUE, animType = "fade")
      },
      finally = {
        shinyjs::enable("submit")
        shinyjs::hide("submit_msg")
      })
    })
    
    # submit another response
    observeEvent(input$submit_another, {
      shinyjs::show("form")
      shinyjs::hide("thankyou_msg")
    })

  }
)