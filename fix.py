import os


def fixer():

    for file in os.listdir():
        if 'atlas-results.csv' in file:
            os.remove(file)

    print('\nRelax, take it easy!')
    print("We're all saved. \n")


def meta_fixer():
    for file in os.listdir():
        if 'probemetadata.json.gz' in file:
            os.remove(file)


fixer()
meta_fixer()
