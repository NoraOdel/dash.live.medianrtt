import os


def fixer():
    for file in os.listdir():
        if 'atlas-results.csv' in file:
            os.remove(file)

    print('\nRelax, take it easy!')
    print('It should be fine now.\n')