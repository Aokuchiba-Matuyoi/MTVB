import os

path = 'E:\PYcharm\PROGRAM\my 2022 summervacation program\TEST'
i = 1
for filename in os.listdir(path):
    newname = str(i) + ".jpg"
    os.rename('TEST/' + filename, "TEST/" + newname)
    i += 1
