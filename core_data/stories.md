## story_greet
* greet 
 - utter_name
 
## story_goodbye
* goodbye
 - utter_goodbye

## story_thanks
* thanks
 - utter_thanks
 
## story_pain_low
* greet
 - utter_name
* name
 - utter_greet
 - utter_pain_query
* affirm
 - utter_pain_level_query
* pain_response
 - slot{"pain_level" : "low"}
 - utter_thankful
 - utter_pain_response_low

## story_pain_med
* greet
 - utter_name
* name
 - utter_greet
<<<<<<< HEAD
* joke
 - action_joke
* thanks
 - utter_thanks
* goodbye
 - utter_goodbye 

## story_surgery
* surgery
 - utter_surgeryname
 - utter_surgerytime
=======
 - utter_pain_query
* affirm
 - utter_pain_level_query
* pain_response
 - slot{"pain_level" : "medium"}
 - utter_pain_response_med

## story_pain_high
* greet
 - utter_name
* name
 - utter_greet
 - utter_pain_query
* affirm
 - utter_pain_level_query
* pain_response
 - slot{"pain_level" : "high"}
 - utter_pain_response_high

## story_pain_none
* greet
 - utter_name
* name
 - utter_greet
 - utter_pain_query
* deny
 - utter_thankful


## story_pain_low_shortcircuit
* greet
 - utter_name
* name
 - utter_greet
 - utter_pain_query
* pain_response
 - slot{"pain_level" : "low"}
 - utter_thankful
 - utter_pain_response_low

## story_pain_med_shortcircuit
* greet
 - utter_name
* name
 - utter_greet
 - utter_pain_query
* pain_response
 - slot{"pain_level" : "medium"}
 - utter_pain_response_med

## story_pain_high_shortcircuit
* greet
 - utter_name
* name
 - utter_greet
 - utter_pain_query
* pain_response
 - slot{"pain_level" : "high"}
 - utter_pain_response_high
>>>>>>> interactive/validate-intent
