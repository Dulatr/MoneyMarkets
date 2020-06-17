from cx_Freeze import setup, Executable

base = None    

executables = [Executable("money.py", base=base)]

packages = ["selenium","os","json"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "money",
    options = options,
    version = "v0.2.2-a3",
    description = 'basic description',
    executables = executables
)