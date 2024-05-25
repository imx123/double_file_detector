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
    while True:
        read = file.read(256000)  # 分块读取文件，避免内存溢出
        jisuan.update(read)
        if not read:  # 读完继续
            break
    file.close()
    output = jisuan.hexdigest()  # 计算哈希值
    print(path, "计算完成", output)
    return output


def read_file(path):
    each_folder_files = []  # 清空赋值
    for root, dirs, files in os.walk(path):
        if len(files) > 0:  # 有文件就读取，没文件就跳过
            each_folder_files = each_folder_files + [os.path.join(root, x) for x in files]  # 把每次遍历的文件夹里的文件加到同一个list里
            # print(each_folder_files, "1") # debug
    if len(each_folder_files) == 0:  # 防止空list进入下一步
        print("错误：文件夹中没有文件")
        return main()
    try:  # 以防万一
        return each_folder_files
    except:
        print("错误：文件夹中没有文件")
        return main()


def compare(origin, new):
    hash_all = defaultdict(list)  # 赋值
    clipped = defaultdict(list)
    # print(origin, new)  # debug
    for i in origin:
        hash1 = count(i)  # 调用计算
        hash_all[hash1].append(i)  # 将哈希值作为key,把对应的文件路径放进字典里
    for i in new:
        hash2 = count(i)
        hash_all[hash2].append(i)
    print("sha1计算完成，正在比对")
    for y in hash_all:  # 将每个哈希对应的文件list提取出来
        files = hash_all[y]
        if len(files) == 1:  # 一个哈希一个文件，没重复
            continue
        elif len(files) > 1:  # 多于一个，有重复
            files.append(len(files))  # 将重复文件个数加进list里
            clipped[y].append(files)  # 将文件路径和个数的list放进总的disc里输出,以哈希为key
            continue
        else:
            print("比对出错！")
    return clipped


def compare_e(path):  # 针对同文件夹做的专用函数（事实上可以和原来的合并
    hash_all = defaultdict(list)
    clipped = defaultdict(list)
    for i in path:
        hash_e = count(i)
        hash_all[hash_e].append(i)
    print("sha1计算完成，正在比对")
    for y in hash_all:
        files = hash_all[y]
        if len(files) == 1:
            continue
        elif len(files) > 1:
            files.append(len(files))
            clipped[y].append(files)
            continue
        else:
            print("比对出错！")
    return clipped


def manage(clipped):  # 操作管理重复文件
    while True:
        print("选择操作：")
        print("1：全部删除")
        print("2:列出文件路径")
        print("3:回到主菜单")
        choose = int(input(""))
        if choose == 1:  # 判断选择
            fail = 0  # 清除赋值，定义变量
            file_num = 0
            for i in clipped:
                for n in range(1, clipped[i][0][-1]):  # 从disc里提取重复文件的数量为重复次数（因为多套了一层list导致有个额外的[0]），从1开始是为了剔除掉第一个作为原本
                    rm_file = clipped[i][0][n]  # 从disc里提取对应重复样本删除
                    print("正在删除", rm_file)
                    try:  # 删除失败时的错误处理
                        os.remove(rm_file)
                    except:
                        fail += 1  # 统计删除失败数量
                        print("删除", rm_file, "失败，请检查文件或权限")
                    finally:
                        file_num += 1  # 统计文件数量
            print("执行完成，成功删除", file_num - fail, "个文件，失败", fail, "个文件")
        elif choose == 2:
            for i in clipped:  # 遍历哈希值
                show_file = clipped[i][0][0]  # 从disc提取每个哈希对应列表第一个作为原本
                show_file_origin = clipped[i][0][1:-1]  # 将每个哈希对应的列表剩余的文件路径输出
                print(show_file, '-->', show_file_origin)
        elif choose == 3:  # 退出循环，回到主程序
            return False
        else:
            continue


def main():  # 主程序（主菜单
    while True:
        print("文件查重（测试）")
        print("1:开始查重(增加）")
        print("2:开始查重（已有）")
        print("3:退出程序")
        choose = int(input(""))
        if choose == 1:  # 判断选择
            origin_path = []  # 清空赋值，定义函数
            new_path = []
            path_origin = input("源文件路径（文件夹）")
            path_new = input("放入文件路径（文件夹）")
            time0 = time.time()  # 记录开始时间
            print("正在读取文件")
            origin_path.extend(read_file(path_origin))  # 读取文件，作为列表存储
            new_path.extend((read_file(path_new)))
            print('准备进行计算')
            clipped = compare(origin_path, new_path)  # 将文件列表输入比较函数
            time1 = time.time()  # 记录结束时间
            print("比对完成, 用时", round(time1 - time0, 3), "秒")  # 计算用时
            manage(clipped)  # 进入文件管理
        elif choose == 2:  # 为单文件夹简化的版本
            path = []  # 清空赋值（定义函数
            path_exist = input("文件夹路径")  # 读取文件，作为列表存储
            time0 = time.time()  # 记录开始时间
            path.extend(read_file(path_exist))
            clipped = compare_e(path)  # 将文件列表输入比较函数（为单文件夹简化的版本
            time1 = time.time()
            print("比对完成, 用时", round(time1 - time0, 3), "秒")  # 计算用时
            manage(clipped)  # 进入文件管理
        elif choose == 3:  # 退出程序
            return False
        else:
            continue


main()  # 主程序调用
