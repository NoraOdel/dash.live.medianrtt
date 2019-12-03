import os


def fixer():

    for file in os.listdir('TempFiles/'):
        if 'atlas-results.csv' in file:
            os.remove('TempFiles/' + file)

    print('\nRelax, take it easy!')
    print("We're all saved. \n")


def meta_fixer():
    for file in os.listdir('TempFiles/'):
        if 'probemetadata.json.gz' in file:
            os.remove('TempFiles/' + file)


fixer()
meta_fixer()
