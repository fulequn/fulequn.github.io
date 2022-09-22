import os
import sys


def directory(directory):
    """单独一个目录"""
    files_list = []
    files_path_list = []
    if os.path.exists(directory):
        pass
    else:
        print("%s 不是一个有效的目录！！！" % directory)
        sys.exit()
    # 遍历目录下读取可读文件
    all_files_directory = os.walk(directory, topdown=True, followlinks=True)
    for root, dirs, files in all_files_directory:
        # 获取文件路径
        for f_name in files:
            file_path = os.path.join(root, f_name)
            files_path_list.append(file_path)
    return files_path_list, files_list


def replace_url(f_l):
    for f in f_l:
        if ".md" in f:
            with open(f, "r", encoding='utf-8') as fr:
                all = fr.read()
                # 替换图片链接中的gitee地址为阿里云oss地址
                down = all.replace("https://flqgraph-1302174199.cos.ap-nanjing.myqcloud.com/img/",
                                   "https://flqgraph-1302174199.cos.ap-nanjing.myqcloud.com/")
                fr.close()
            with open(f, "w", encoding='utf-8') as fr1:
                fr1.write(down)
            print("%s 完成替换！！！" % f)
        else:
            pass


if __name__ == "__main__":
    # windows 路径需要双反斜杠c:\\笔记\\
    a, b = directory("D:\\workspace\\myBlog\\source\\_posts")
    replace_url(a)

