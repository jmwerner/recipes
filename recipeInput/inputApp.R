library(shiny)
library(jsonlite)

numberOfIngredients = 15

ingredient_field_names = c(paste0("ingredient_number_", 1:numberOfIngredients),
                           paste0("ingredient_units_", 1:numberOfIngredients),
                           paste0("ingredient_name_", 1:numberOfIngredients))

# which fields get saved 
fieldsAll = c("recipeName", "recipeCategory", "recipeSource", "directions", "notes", ingredient_field_names)

# which fields are mandatory
fieldsMandatory = c("recipeName", "recipeCategory", "recipeSource", "directions")

# add an asterisk to an input label
labelMandatory = function(label) {
    tagList(label, span("*", class = "mandatory_star"))
}

# get current Epoch time
epochTime = function() {
    return(as.integer(Sys.time()))
}

humanTime = function() {
    format(Sys.time(), "%Y%m%d-%H%M%OS")
}

removeSpaces = function(input) {
    gsub("[[:blank:]]", "", input)
}

# save the results to a json file
# This code is very dependent on id names, be careful when
#  changing structure of the app! 
saveData = function(data) {

    data = data.frame(data)

    system(paste0("mkdir -p ../allRecipes/", removeSpaces(data$recipeCategory)))

    fileName = paste0(data$recipeName, ".json")
    filePath = file.path(paste0("../allRecipes/", data$recipeCategory), fileName) 

    ingredientsSubset = data[,grepl("ingredient", names(data))]

    nameFrame = do.call(rbind, strsplit(names(ingredientsSubset), "_"))
    maxIngredientNumber = max(as.numeric(nameFrame[,3]))
    
    ingredientsList = list()
    for(i in 1:maxIngredientNumber) {
        ingredientsList[[i]] = list(
            "number" = ingredientsSubset[[paste0("ingredient_number_", i)]],
            "units" = ingredientsSubset[[paste0("ingredient_units_", i)]],
            "name" = ingredientsSubset[[paste0("ingredient_name_", i)]]
        )        
    }

    output = list(
        "recipeName" = data$recipeName,
        "recipeCategory" = data$recipeCategory,
        "recipeSource" = data$recipeSource,
        "directions" = data$directions,
        "timestamp" = data$timestamp,
        "notes" = data$notes,
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
                    "Ounces(s)" = "Ounces(s)",
                    "Clove(s)" = "Clove(s)")


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
            textInput("recipeSource", label = labelMandatory("Recipe Source (url)"), value = "")
        )
    ),


    titlePanel("Ingredients"),

    wellPanel(
        fluidRow(
            column(2,
                mainPanel("#")
            ),
            column(2,
                mainPanel("Units")
            ),
            column(3,
                mainPanel("Ingredient")
            )
        ),
        lapply(1:numberOfIngredients, function(i) {
            fluidRow(
                column(2,
                    textInput(paste0("ingredient_number_", i), label = NA, value = "")
                ),
                column(2,
                    selectInput(paste0("ingredient_units_", i), label = NA, 
                        choices = unitsOptions, 
                        selected = "")
                ),
                column(3,
                    textInput(paste0("ingredient_name_", i), label = NA, value = "")
                )
            )
        })
    ),

    titlePanel("Directions"),

    wellPanel(
        tags$textarea(id="directions", rows=15, cols=100, "")

    ),

    titlePanel("Notes"),

    wellPanel(
        tags$textarea(id="notes", rows=10, cols=100, "")

    ),

    actionButton("submit", "Submit", class = "btn-primary"),
        
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

  server = function(input, output, session) {
    
    # Enable the Submit button when all mandatory fields are filled out
    observe({
      mandatoryFilled =
        vapply(fieldsMandatory,
               function(x) {
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
      error = function(err) {
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