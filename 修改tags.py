import os
import sys
import re


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


def replace_tags(f_l):
    # 定义要合并的标签映射
    # 左边整合到右边
    tags_mapping = {
        "Docker": "docker",
        "Hexo": "hexo",
        "spark": "大数据技术",
        "HBase": "数据库",
        "DeepLearning": "机器学习",
        "ReinforcementLearning": "动态规划",
        "CentOS": "操作系统",
        "Linux": "操作系统",
        "MapReduce": "大数据技术",
        "MongoDB": "数据库",
        
    }

    for f in f_l:
        if ".md" in f:
            with open(f, "r", encoding='utf-8') as fr:
                content = fr.read()
                # 使用正则表达式查找标签
                tags_pattern = re.compile(r'tags:\n- .*?\n', re.DOTALL)
                tags_match = tags_pattern.search(content)
                if tags_match:
                    tags_str = tags_match.group()
                    # 替换标签
                    for old_tag, new_tag in tags_mapping.items():
                        tags_str = tags_str.replace(old_tag, new_tag)
                    content = content.replace(tags_match.group(), tags_str)
                fr.close()
            with open(f, "w", encoding='utf-8') as fr1:
                fr1.write(content)
            print("%s 完成替换！！！" % f)
        else:
            pass


if __name__ == "__main__":
    a, b = directory("C:\\my\\workspace\\myblog\\source\\_posts")
    replace_tags(a)
