
scalingValues = ["1", "2", "3", "1/2"]

recipeIterator = 0

function rescaleRecipe(){
    recipeIterator = (recipeIterator + 1) % scalingValues.length;
    var button = document.getElementById("scalingButton");
    button.innerText = scalingValues[recipeIterator] + "X";
    updateRecipeNumbers(scalingValues[recipeIterator])
 }


function updateRecipeNumbers(scaling_factor){
    var elements = document.getElementsByClassName("recipeNumber");
    for(i = 0; i < elements.length; i++){
        raw_fraction = processInputNumber(elements[i].attributes.value.value)
        scaling_fraction = processInputNumber(scaling_factor)
        raw_fraction[0] *= scaling_fraction[0]
        raw_fraction[1] *= scaling_fraction[1]
        elements[i].innerText = processOutputNumber(raw_fraction)
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
        output_string += String(fraction_numerator) + "/" + String(input_array[1])
    }
    return output_string
}

