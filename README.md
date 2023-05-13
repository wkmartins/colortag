# Colortag
Colortag is a Python library for adding ANSI colors to the terminal output using a simple syntax
## Installation
Not avaliable on pip yet
## Usage
- Use `cprint` function if you want to print the text directly
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
- Use `c` function to create a ColorTag object so you can use string methods in it
```python
from colortag import cprint, c

text = c("This is an <example: blue;bold;line> text everybody")
print("# ORIGINAL:")
print(text)
print("# UPPER:")
print(text.upper())
print("# CENTERED:")
print(text.center(50, "-"))
print("# SLICED:")
print(text[13:29])
print("# AND SO ON")
```
![image](https://github.com/wagnerkaue/colortag/assets/121360920/61236edf-1cec-4452-96ea-de4e84d1229d)

- ANSI attributes

![image](https://github.com/wagnerkaue/colortag/assets/121360920/0b2c6e3e-5a96-4baf-aa4a-7b419b617583)
