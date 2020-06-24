from cx_Freeze import setup, Executable

base = None    

executables = [Executable("money.py", base=base)]

packages = ["selenium","os","json","time","sys"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "money",
    options = options,
    version = "v0.2.6-a3",
    description = 'Money Markets CLI applicatio.',
    executables = executables
)