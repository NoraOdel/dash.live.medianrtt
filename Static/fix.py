import os
import math


def fixer():

    for file in os.listdir('TempFiles/'):
        if 'atlas-results.csv' in file:
            os.remove('TempFiles/' + file)

    print("\nLeftover files deleted if any existed\n")


def meta_fixer():
    for file in os.listdir('TempFiles/'):
        if 'probemetadata.json.gz' in file:
            os.remove('TempFiles/' + file)


def draw():
    print('\n--------------------------------------------------')
    radius = 5

    for i in range((2 * radius) + 1):
        if i == 3:
            break
        for j in range((2 * radius) + 1):

            dist = math.sqrt((i - radius) * (i - radius) +
                             (j - radius) * (j - radius))

            if radius + 0.5**radius+0.5 > dist > radius - 1**radius:
                print("*", end="")
            else:
                print(" ", end="")
        print()

    print("//___/ __\\\\")

    lightning_len = 13
    for num in range(lightning_len):
        if num <= 0:
            continue
        elif num == 1:
            print('/' + ' ' * 4 + ' ' * num + '°' * num + ' ' * 3 + '\\')
        else:
            print(' '*5 + ' '*num + '°'*num)

    print(' '*23 + 'O/')
    print(' '*22 + '/|')
    print(' '*20 + 'Goodbye'.upper())

    print('--------------------------------------------------\n')

fixer()
meta_fixer()