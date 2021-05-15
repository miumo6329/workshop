import os
import re
import shutil
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS


def get_key_from_value(d, val):
    keys = [k for k, v in d.items() if v == val]
    if keys:
        return keys[0]
    return None


def get_exif(img_path):

    img = Image.open(img_path)
    exif = img._getexif()

    exif_data = {}
    for key, value in exif.items():
        exif_data[TAGS.get(key)] = value
    return exif_data


def main():
    import_root = 'G:\\DCIM'
    export_root = 'F:\\Picture'

    # 取り込み対象フォルダを全検索し、ファイルパスをリスト化
    import_list = []
    for root, dirs, files in os.walk(import_root):
        for name in files:
            import_list.append(os.path.join(root, name))

    # 既存フォルダの検索
    export_existing_list = []
    for year_dir in os.listdir(export_root):
        if re.compile('\d{4}$').match(year_dir):
            for year_day_dir in os.listdir(os.path.join(export_root, year_dir)):
                if re.compile('\d{8}\_').match(year_day_dir):
                    export_existing_list.append(year_day_dir)

    # 最新フォルダの日付取得
    # export_existing_list = [e.split('_')[0] + '_' for e in export_existing_list]
    last_update = sorted(export_existing_list)[-1]
    last_update = last_update.split('_')[0]

    for target in sorted(import_list):
        unix_time = os.path.getctime(target)
        dt = datetime.fromtimestamp(unix_time)

        # 移動先フォルダ作成
        export_dir = os.path.join(export_root, str(dt.year), dt.strftime('%Y%m%d'))

        # 終端フォルダ(YYYYMMDD_イベント名)のリストを取得
        end_dirs = [end_dir for end_dir in os.listdir(os.path.join(export_root, str(dt.year)))]

        # 対象ファイルの更新日フォルダがなかった場合、新規作成
        if not dt.strftime('%Y%m%d') in [d.split('_')[0] for d in end_dirs]:
            os.mkdir(export_dir + '_')
        # あった場合、フォルダ名を特定し移動先フォルダを更新
        else:
            for d in end_dirs:
                if dt.strftime('%Y%m%d') == d.split('_')[0]:
                    export_dir = os.path.join(export_root, str(dt.year), d)

        if target.endswith('.JPG') or target.endswith('.MOV'):
            if os.path.isfile(os.path.join(export_dir, os.path.basename(target))):
                print('既存ファイル :', os.path.join(export_dir, os.path.basename(target)))
            else:
                print('移動対象！　:', os.path.join(export_dir, os.path.basename(target)))
                shutil.copy2(target, os.path.join(export_dir, os.path.basename(target)))
        elif target.endswith('.RAF'):
            if not os.path.isdir(os.path.join(export_dir, 'RAW')):
                os.mkdir(os.path.join(export_dir, 'RAW'))
            if os.path.isfile(os.path.join(export_dir, 'RAW', os.path.basename(target))):
                print('既存ファイル :', os.path.join(export_dir, 'RAW', os.path.basename(target)))
            else:
                print('移動対象！　:', os.path.join(export_dir, 'RAW', os.path.basename(target)))
                shutil.copy2(target, os.path.join(export_dir, 'RAW', os.path.basename(target)))


if __name__ == '__main__':
    main()
