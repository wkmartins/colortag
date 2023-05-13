# Colortag
colortag is a Python library for adding ANSI colors to the terminal output using a simple syntax
## Installation
Not avaliable on pip yet
## Usage
Use `cprint` function if you want to print the text directly
```python
from colortag import cprint, c

cprint("Hello! <This: yellow;line> is an <example: red;bold> text")
cprint("This one have a <blue: bluebg> background")
```
![image](https://github.com/wagnerkaue/colortag/assets/121360920/18a03856-fd3d-44b3-8562-34cbe9155c94)

You can also use it with f-strings to put variables inside it
```python
from colortag import cprint, c

name = "John"
age = "20"
cprint(f"Your name is <{name}: yellow;bold> and you are <{age}: blue;line> years old")
```
![image](https://github.com/wagnerkaue/colortag/assets/121360920/12f3020c-0fa9-497e-9fda-48010c544082)