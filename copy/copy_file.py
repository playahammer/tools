# coding:utf-8

import os, argparse
from shutil import copyfile


def exec_cp(src_dir, dst_dir):

    dirs = [src_dir, dst_dir]

    for d in dirs:
        if not os.path.isdir(d):
            print('[-] Error: "%s" is not directory' % src_dir)
            return

        if not os.path.exists(d):
            print('[-] Error: "%s" is not exists' % src_dir)
            return

    count = 0
    def recursion(path):
        nonlocal count
        list_file = os.listdir(path)

        for file_name in list_file:
            abs_path = os.path.join(path, file_name)

            if os.path.isdir(abs_path):
                print('[+] Enter directory %s' % abs_path)
                recursion(abs_path)

            if os.path.isfile(abs_path):
                count += 1
                print('[+] File: %s' % abs_path)
                print('[+] Execute copying file to %s' % dst_dir)
                try:
                    copyfile(abs_path, os.path.join(dst_dir, file_name))
                except OSError as e:
                    print(
                        '[-] Copying failed, err: %s' % e.args
                    )
                    return
                else:
                    print(
                        '[+] Copying success'
                    )

    recursion(src_dir)
    print('File total count: %d' % count)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('s', help='source directory path', type=str)
    parser.add_argument('d', help='destination directory path', type=str)
    args = parser.parse_args()
    if args.s and args.d:
        exec_cp(args.s, args.d)