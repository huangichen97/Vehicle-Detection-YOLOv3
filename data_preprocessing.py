from simpleimage import Image
import pandas as pd

FILE = 'MIO-TCD-Localization/MIO-TCD-Localization'

classes = ['articulated_truck', 'bicycle', 'bus', 'car', 'motorcycle',
           'motorized_vehicle', 'non-motorized_vehicle', 'pedestrian',
           'pickup_truck', 'single_unit_truck', 'work_van']
d = {}


def main():
    df = pd.read_csv('gt_train_v2.csv')
    # image width
    df['img_w'] = 1
    # image height
    df['img_h'] = 1

    # (first file, last file +1)
    for i in range(110593, 115119):
        # print(round(100*i/110592), 0)
        w, h = find_wh(i)
        if (w, h) != (0, 0):
            df.loc[df['index'] == i, 'img_w'] = w
            df.loc[df['index'] == i, 'img_h'] = h
    df['x_c'] /= df['img_w']
    df['y_c'] /= df['img_h']
    df['block_w'] /= df['img_w']
    df['block_h'] /= df['img_h']
    print(df[['index', 'x_c', 'y_c', 'block_w', 'block_h', 'img_w', 'img_h']].head(200))
    print(create_dict(df))
    txt_generator(d)


def find_wh(i):
    try:
        str_i = str(i)
        while len(str_i) < 8:
            str_i = '0' + str_i
        # filename = f'{str_i}.jpg'
        # print(filename)
        # img = Image(FILE+f'/train/{str_i}.jpg')
        img = Image(f'images/test_4500/{str_i}.jpg')
        width = img.getWidth()
        height = img.getHeight()
        return width, height
    except FileNotFoundError:
        return 0, 0


def create_dict(df):
    # (first file's first row -2, (last file +1)'s first row -2)
    for i in range(67043, 70178):
        filename = str(df.iloc[i, df.columns.get_loc('index')]) + '.txt'

        while len(filename) < 12:
            filename = str(0) + filename

        if filename not in d:
            d[filename] = [[classes.index(df.iloc[i, df.columns.get_loc('category')]),
                            df.iloc[i, df.columns.get_loc('x_c')],
                            df.iloc[i, df.columns.get_loc('y_c')],
                            df.iloc[i, df.columns.get_loc('block_w')],
                            df.iloc[i, df.columns.get_loc('block_h')]]]
        else:
            d[filename] += [[classes.index(df.iloc[i, df.columns.get_loc('category')]),
                            df.iloc[i, df.columns.get_loc('x_c')],
                            df.iloc[i, df.columns.get_loc('y_c')],
                            df.iloc[i, df.columns.get_loc('block_w')],
                            df.iloc[i, df.columns.get_loc('block_h')]]]
    return d


def txt_generator(d):
    for filename in d:
        print(filename)
        with open(filename, 'w') as out:
            for i in range(len(d[filename])):
                # every single line
                line = ''
                for item in d[filename][i]:
                    # line = str(d[filename][i])[1:len(str(d[filename][i]))-1]
                    line = line + str(item) + ' '
                line = line[:len(line)-1]
                out.write(line+'\n')


if __name__ == '__main__':
    main()
