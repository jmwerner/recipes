
scalingValues = ["1", "2", "3", "1/2"]

// Both plural to plural and non-plural to plural
plural_mappings = {"Cups": "Cups", 
                   "Tablespoons": "Tablespoons",
                   "Teaspoons": "Teaspoons",
                   "Pounds": "Pounds", 
                   "Cans": "Cans",
                   "Ounces": "Ounces",
                   "Cloves": "Cloves",
                   "Pinches": "Pinches",
                   "Dashes": "Dashes",
                   "Bottles": "Bottles",
                   "Cup": "Cups", 
                   "Tablespoon": "Tablespoons",
                   "Teaspoon": "Teaspoons",
                   "Pound": "Pounds", 
                   "Can": "Cans",
                   "Ounce": "Ounces",
                   "Clove": "Cloves",
                   "Pinch": "Pinches",
                   "Dash": "Dashes",
                   "Bottle": "Bottles",
                   "Grams": "Grams"}

// Both plural to non-plural and non-plural to non-plural
non_plural_mappings = {"Cups": "Cup", 
                       "Tablespoons": "Tablespoon",
                       "Teaspoons": "Teaspoon",
                       "Pounds": "Pound", 
                       "Cans": "Can",
                       "Ounces": "Ounce",
                       "Cloves": "Clove",
                       "Pinches": "Pinch",
                       "Dashes": "Dash",
                       "Bottles": "Bottle",
                       "Cup": "Cup", 
                       "Tablespoon": "Tablespoon",
                       "Teaspoon": "Teaspoon",
                       "Pound": "Pound", 
                       "Can": "Can",
                       "Ounce": "Ounce",
                       "Clove": "Clove",
                       "Pinch": "Pinch",
                       "Dash": "Dash",
                       "Bottle": "Bottle",
                       "Gram": "Gram"}

recipeIterator = 0

function rescaleRecipe(){
    recipeIterator = (recipeIterator + 1) % scalingValues.length;
    var button = document.getElementById("scalingButton");
    button.innerText = scalingValues[recipeIterator] + "X";
    updateRecipe(scalingValues[recipeIterator])
 }


function updateRecipe(scaling_factor){
    var elements = document.getElementsByClassName("recipeNumber");
    for(i = 0; i < elements.length; i++){
        raw_fraction = processInputNumber(elements[i].attributes.value.value)
        scaling_fraction = processInputNumber(scaling_factor)
        raw_fraction[0] *= scaling_fraction[0]
        raw_fraction[1] *= scaling_fraction[1]
        elements[i].innerText = processOutputNumber(raw_fraction)

        is_plural = raw_fraction[0] > raw_fraction[1]
        unit_id = elements[i].id.replace('recipeNumber', 'recipeUnit')
        unit_element = document.getElementById(unit_id)
        unit_element.innerText = handlePlural(unit_element.innerText, is_plural)
    }   
}

function handlePlural(input_text, plural_logical){
    input_text = input_text.trim()
    if(input_text == "Whole"){
        return("Whole")
    }
    if(plural_logical){
        return(plural_mappings[input_text])
    }else{
        return(non_plural_mappings[input_text])
    }
}




// Function for cleaning split arrays
Array.prototype.clean = function(deleteValue) {
  for (var i = 0; i < this.length; i++) {
    if (this[i] == deleteValue) {         
      this.splice(i, 1);
      i--;
    }
  }
  return this;
};


// Takes string and returns [numerator, denominator]
function processInputNumber(string){
    var splits = string.split(" ").clean("")
    if(splits.length == 1){
        inner_splits = splits[0].split("/")
        if(inner_splits.length == 1){
            return [Number(inner_splits[0]), 1.0]
        }else{
            if(inner_splits.length == 2){
                return [Number(inner_splits[0]), Number(inner_splits[1])]
            }else{
                throw "Improper string, can't parse " + splits[0]
            }
        }
    }else{
        if(splits.length == 2){
            processed_numbers = processInputNumber(splits[1])
            output_numerator = processed_numbers[0] + Number(splits[0]) * processed_numbers[1]
            return [output_numerator, processed_numbers[1]]
        }else{
            throw "Improper string, can't parse " + string
        }
    }
}

// This function was adapted from a hero on Stack Overflow
function reduce_fraction(numerator,denominator){
    var find_greatest_common_divisor = function find_greatest_common_divisor(a,b){
        return b ? find_greatest_common_divisor(b, a%b) : a;
    };
    greatest_common_divisor = find_greatest_common_divisor(numerator,denominator);
    return [numerator/greatest_common_divisor, denominator/greatest_common_divisor];
}

// Takes [numerator, denominator] and returns string of mixed number
function processOutputNumber(input_array){
    var leading_integer = parseInt(input_array[0] / input_array[1])
    var fraction_numerator = input_array[0] % input_array[1]
    var output_string = ""
    if(leading_integer > 0){
        output_string += String(leading_integer)
        if(fraction_numerator > 0){
            output_string += " "
        }
    }
    if(fraction_numerator > 0){
        fraction_denominator = input_array[1]
        reduced_fraction = reduce_fraction(fraction_numerator, fraction_denominator)
        output_string += String(reduced_fraction[0]) + "/" + String(reduced_fraction[1])
    }
    return output_string
}

