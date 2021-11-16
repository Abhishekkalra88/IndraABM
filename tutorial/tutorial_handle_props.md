# Tutorial of handling props

> Since handling props in Indra system requires advanced skills to fully understand, 
> we make another video delving into it.
>
> This file is served as a script and a document of tutorial video for handling props.

## Main structure
1. introduce the structure of the `[MODEL_NAME].props.json`
2. analyse and explain handling props
3. change code and show how handling props works(setting parameters in the terminal lines)
4. mention handling props on the web

## Intro
This is a short but more advanced tutorial for Indra system that focus mainly on dealing with user defined props, 
as we will dig deep into the code on all the places that you can customize for parameters.  
We will also introduce the frontend interface for our Indra System.  
If you want a general walk through on how to create an ABM from Indra, please watch our general tutorial video, which will also cover the basics of handling props. 

## Introduction of `[MODEL_NAME].props.json`
Handling props is basically setting values of the parameters in the model. In Indra system, you are asked several
questions to set parameters when you run the model in the terminal mode. The parameters and the questions are 
defined in the `[MODEL_NAME].props.json` file.  

Next I will show you one example to help you understand the general structure/format of the file.  
`screen on segregation.props.json`  
Let's have a look at the props file of segregation model.
It is actually a two-layer dictionary. The key of outer dictionary is the parameter, and the value is an inner
dictionary with attribute as key and value of the attribute as value.
For the keys of outer dictionary, there is not much to talk about. They are the parameters you are going to set in your
model.  
`highlight the line`  
For inner dictionary. First you set a default value of the parameter or in other words, the fallback value of the
parameter when you press enter. The attribute name is "val", and we set a default value 40 for grid_height.  
`highlight the line`  
The second attribute is "question" which is the question you design to ask in the terminal. 
It is better to compose a clear question since the parameter name itself might be confusing.  
`highlight the line`  
The third one is "atype" which defines the data type of the parameter. There are several options: "INT" which represents
integer, "DBL" which represents double, "BOOL" which represents boolean, "STR" which represents string.  
`highlight two lines`  
And the last two attributes "hival" and "lowval" which defines the 
highest and lowest value of the parameter are for numeric types "INT" and "DBL".
You can set these two attributes based on the specific restrictions in your model.
```
"grid_height": {
    "val": 40,
    "question": "What is the grid height?",
    "atype": "INT",
    "hival": 100,
    "lowval": 2
},
```

## Analyse and explain handling props
Notes:
1. Retrieve user type from env variable (USER_TYPE_VAR)
2. If user type is API, skip questions.
3. Call `init_props()` to init props and store as self.props, passing `self.module`(model name), `props`(prop_dict with default value None)
   and `model_dir`(directory of model with default value "models")
4. If `props` is passed, then call `PropArgs.create_props(prop_dict=props)` meaning create props from this parameter `props`  
   Else, then call `PropArgs.create_props(ds_file=props_file)` meaning create props from the `[MODEL_NAME].props.json` file
   `model_dir` and `self.module` is used to generate path of the `[MODEL_NAME].props.json` file
5. By calling `PropArgs.create_props()`, we will get an instance of class PropArgs whose class variable `props` is initialized with the parameters we passed.   
   Then we can get the value of each parameter in the model by `self.props.get(prop_nm, default_value)`. 
   It is actually enclosed in a function `get_prop(prop_nm, default_value)` to hide props structure

self.props in class PropArgs:    
We mainly focus on the variable `self.props` in class PropArgs. There are two ways to initialize `self.props`: from file or from a dictionary.  
If we pass a props file, we will call `json.load()` first to convert the content of the json file into a props dictionary.
Then we call `set_props_from_dict()` to retrieve the values in the props dictionary and put them into `self.props`  
If we pass a props dictionary, we directly call `set_props_from_dict()` to put values into `self.props`
Remind that if we pass both props file and props dict, values set by the props file will be overwritten by the values in
the props dict since values in the props dict is set after the props file.

set_props_from_dict(prop_args, prop_dict):

## Handling props from the web
`open browser and copy and paste in url https://tandondevops.github.io/IndraFrontend/#/`  
We also have a web-based frontend interface to show our ABMs. You can see it directly from here, that we have a drop-down menu for the user to select a model. 
Those models can be prepopulated from the configuration, which means you can have your own customized model to be shown here if you want!

`select forest fire from drop-down menu`  
If we proceed with selecting the forest fire model here, our page will show us four questions that are the same as the questions that we will get from terminal.  
These questions are read from the same configuration file which is the `[MODEL_NAME].props.json` file. 

`mouse point to one of the input box's gray default value`  
We can see in the input box, we have the default value in gray, like grid height & width should be 40.   
If we do want to specify a value, we can type in the input box, just like we will type in a customized value in terminal before we hit enter.

`click on submit and click on run with the default 10 periods`  
Here we can see a more visual-friendly graph than on the terminal.   
We have the output from the terminal in the section of model status shown on the right, as well as the scatter plot at the bottom. 

Basically, we keep the workflow consistent throughout both terminal and web. This should just be a brief overview to get you know we have the web option to get to show your models!
