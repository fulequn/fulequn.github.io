import os
import re


def update_image_links(file_path):
    """
    更新Markdown文件中的图片链接，将其按年份和文件夹进行管理。

    :param file_path: Markdown文件路径
    """
    # 读取Markdown文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 正则表达式查找图片链接
    # pattern = re.compile(r'https://raw\.githubusercontent\.com/fulequn/oss_img/master/(\d{4})(\d{10})\.(png|jpg|svg)')
    pattern = re.compile(
        r'https://raw\.githubusercontent\.com/fulequn/oss_img/master/(\d{4})(\d{10,11})\.(png|jpg|svg)')

    # def replace_link(match):
    #     year = match.group(1)
    #     img_name = match.group(2)
    #     extension = match.group(3)
    #     folder_prefix = 1  # 假设每年只有一个文件夹，你可以根据需要调整逻辑
    #     new_link = f'https://raw.githubusercontent.com/fulequn/oss_img/master/img{year[-2:]}{folder_prefix}/{year}{img_name}.{extension}'
    #     return new_link

    def replace_link(match):
        year = match.group(1)
        img_name = match.group(2)
        extension = match.group(3)
        folder_prefix = 1  # 假设每年只有一个文件夹，你可以根据需要调整逻辑
        new_link = f'https://raw.githubusercontent.com/fulequn/oss_img/master/img{year[-2:]}{folder_prefix}/{year}{img_name}.{extension}'
        return new_link

    # 替换图片链接
    new_content = pattern.sub(replace_link, content)

    # 将更新后的内容写回Markdown文件
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(new_content)


def update_all_files(directory):
    """
    更新指定目录下所有Markdown文件中的图片链接。

    :param directory: 目录路径
    """
    for root, _, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith('.md'):
                file_path = os.path.join(root, file_name)
                update_image_links(file_path)


if __name__ == "__main__":
    directory_path = 'D:\\workspace\\myblog\\source\\_posts'  # 替换为你的Markdown文件所在目录
    update_all_files(directory_path)
