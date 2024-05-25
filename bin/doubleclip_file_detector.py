import hashlib
import os
import time
from collections import defaultdict


def count(path):
    jisuan = hashlib.sha1()
    try:
        file = open(fr'{path}', 'rb')  # 打开文件
    except:
        print("错误：无法打开文件，请检查文件路径")
        return main()
    while True:
        read = file.read(256000)  # 分块读取文件，避免内存溢出
        jisuan.update(read)
        if not read:
            break
    file.close()
    output = jisuan.hexdigest()  # 计算哈希值
    return output


def read_file(path):
    global each_folder_files
    for root, dirs, files in os.walk(path):
        if len(files) > 0:
            each_folder_files = [os.path.join(root, x) for x in files]
    return each_folder_files


def compare(origin, new):
    hash_origin = defaultdict(str)
    hash_new = defaultdict(str)
    clipped = defaultdict(str)
    for i in origin:
        hash1 = count(i)
        hash_origin[hash1] = i
    for i in new:
        hash2 = count(i)
        hash_new[hash2] = i
    for y in hash_new:
        if y in hash_origin:
            clipped[y] = hash_new[y]
            continue
    return clipped



def manage(clipped):
    while True:
        print("选择操作：")
        print("1：全部删除")
        print("2:列出文件路径")
        print("3:回到主菜单")
        choose = int(input(""))
        if choose == 1:
            for i in clipped:
                fail = 0
                file_num = 0
                rm_file = clipped[i]
                print("正在删除", rm_file)
                try:
                    os.remove(rm_file)
                except:
                    print("删除", rm_file, "失败，请检查文件或权限")
                    fail += 1
                finally:
                    file_num += 1
            print("执行完成，成功删除", file_num - fail, "个文件，失败", fail, "个文件" )
        elif choose == 2:
            for i in clipped:
                show_file = clipped[i]
                print(show_file)
        elif choose == 3:
            return False
        else:
            continue

def main():
    while True:
        print("文件查重（测试）")
        print("1:开始查重")
        print("2:退出程序")
        choose = int(input(""))
        if choose == 1:
            origin_path = []
            new_path = []
            path_origin = input("源文件路径（文件夹）")
            path_new = input("放入文件路径（文件夹）")
            time0 = time.time()
            origin_path.extend(read_file(path_origin))
            new_path.extend((read_file(path_new)))
            clipped = compare(origin_path, new_path)
            time1 = time.time()
            print("计算完成, 用时", time1 - time0)
            manage(clipped)
        elif choose == 2:
            return False
        else:
            continue



main()
