import os, cv2

directory = 'D:\Testing/ari thesis for testing/ari-combined'
source_directory = 'D:\Testing/ari thesis for testing/'


def make_dirs():
    for i in range(ord('A'), ord('Z') + 1):
        if not os.path.exists(directory + chr(i)):
            os.makedirs(directory + chr(i))
        else:
            print(chr(i) + ' folder exists!')


def rename_images():
    start = 0
    end = 25
    count = 0
    for i in range(ord('A'), ord('Z') + 1):
        for j in range(3):
            for z in range(start, end):
                os.rename(source_directory + str(j) + '/greyscale/' + chr(i) + '/' + str(count) + '.jpg',
                          directory + chr(i) + '/' + str(z) + '.jpg')
                count += 1
            count = 0
            start += 25
            end += 25
        count = 0
        start = 0
        end = 25

def combine_testing():
    for x in os.walk(source_directory):



def greyscale_images():
    #for i in range(ord('A'), ord('Z') + 1):
    for i in os.walk(source_directory):
        for j in range(25):
            image = cv2.imread(source_directory + '/' + chr(i) +'/'+ str(j) + '.jpg')
            print(source_directory + '/' + chr(i)+'/' + str(j) + '.jpg')
            grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            print('done')
            cv2.imwrite(directory + '/' + chr(i) + '/' + str(j) + '.jpg', grey_image)
            print(directory + '/' + chr(i) + '/' + str(j) + '.jpg')


def check_directories():
    for x in os.walk(source_directory):
        print(x)

#make_dirs()
#rename_images()
#greyscale_images()

check_directories()