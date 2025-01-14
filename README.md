analysis_scripts
- tool kits to analyze signals
- Note: input file name must be made by json file as the <basename>.json, <basename> is the basename of corresponding script, without extention .py.
- Note: Please clone nasu package from GitHub as submodule.
- Note: Make config.json file to teach working directory, temporal directory, output directory, inputs directory, and auto output directory. 

- contents
  - __init__.py
  - .gitignore
  - .gitmodules
  - config.json : made by yourself
  - README.md
  - showfig.py
  - nasu : cloned as submodule
  - templates_pickleoutput
    - template_pickleinput.py
    - template.py
  - test
    - __init__.py
    - bandpassfilter_design.py
    - coherence_noise.py
  - eg
    - __init__.py
    - inputs
      - check_ece_chs.json
    - check_ece_chs.py
  - d3d
  - labcom

example of config.json
{
	"wd" : "C:/pythonProject/analysis_scripts",
	"tmp_dir" : "C:/python_temp", 
	"base_output_dir" : "C:/python_data", 
	"inputs_dir" : "inputs", 
	"auto_output_dir" : "auto"
}
