import os


def fixer():
    for file in os.listdir():
        if 'atlas-results.csv' in file:
            os.remove(file)


if __name__ == '__main__':
    fixer()
    print('\nRelax, take it easy!')
    print('It should be fine now.\n')
