# video to image code

import cv2
import os
import argparse
import glob
from tqdm import tqdm

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)


parser = argparse.ArgumentParser()
parser.add_argument('-d', '--directory', dest='dir', help="setting dir", action='store')
parser.add_argument('-f', '--framesave', dest='fps', help="setting save frame", action='store')
args = parser.parse_args()

dir = args.dir
fps = int(args.fps)
createFolder(dir + '_shot')
save_dir = dir + '_shot\\'
video = '*.mp4'

for vid in tqdm(glob.glob(dir + '\\' + video)):
    cap = cv2.VideoCapture(vid)
    img = save_dir + vid.split('.')[0].split('\\')[-1]
    createFolder(img)

    flag = False
    i = 0

    while (cap.isOpened()):
        ret, frame = cap.read()

        if ret:
            if (i % fps) == 0:
                cv2.imwrite(img + '\\img_' + str(i) + '.jpg', frame)
                f=open(img + '\\img_' + str(i) + '.txt', 'wt')
                f.close()
            i += 1

        else:
            flag = True
            break

    if flag:
        print('Finished Video to Image : ' + vid)
    else:
        print('Not exist File : ' + vid)

    cap.release()
    cv2.destroyAllWindows()