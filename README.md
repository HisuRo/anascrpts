analysis_scripts
- tool kits to analyze signals
- Note: input file name must be made by json file as the <basename>.json, <basename> is the basename of corresponding script, without extention .py.
- Note: Please clone gsrc package from GitHub as submodule. 
- Note: Please make config.json file to teach working directory, temporal directory, output directory, inputs directory, and auto output directory. 

- contents
  - __init__.py
  - .gitignore
  - .gitmodules
  - config.json : made by yourself
  - README.md
  - showfig.py
  - gsrc : cloned as submodule
  - templates_pickleoutput
    - template_pickleinput.py
    - template.py
  - test
    - __init__.py
    - helloworld.py

example of config.json
{
	"wd" : "C:/anascrpts",
	"tmp_dir" : "C:/python_temp", 
	"base_output_dir" : "C:/python_data", 
	"inputs_dir" : "inputs", 
	"auto_output_dir" : "auto"
}
