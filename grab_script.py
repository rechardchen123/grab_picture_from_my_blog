#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
# @Time : 3/12/2019 9:30 AM 
# @Author : Xiang Chen (Richard)
# @File : grab_script.py 
# @Software: PyCharm
import requests
import os
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/63.0.3239.132 Safari/537.36',
    'cookie': ''
}


def download_photo(each_album_link, album_photoNumber, album_name, album_id, person):
    '''
    Based on the album name, download the album
    :param each_album_link: <str> the link of album
    :param album_photoNumber: <int> the total number of photos in each album
    :param album_name: <str> the name of the album and use to create the same name folder
    :param album_id: <str> the ID of album
    :param person: <str> the name of the album
    :return: none
    '''
    n = 0
    while n < album_photoNumber:
        link_para = ''.format(int((n / 100) + 1))
        js_link = each_album_link.replace('v7', link_para)  # build the web of the album
        print(js_link)

        file_path = make_file(person, album_name, album_id)
        html_data = requests.get(js_link, headers=headers)
        try:
            json_data = html_data.json()['photoList']
            for i in range(0, len(json_data)):
                link = json_data[i]['url']  # get the link of each picture in the album
                if file_path is None:
                    return
                else:
                    if os.path.exists(file_path + '/' + str(i + n + 1) + '.jpg'):
                        pass
                    else:
                        with open(file_path + '/' + str(i + n + 1) + '.jpg', 'wb') as f:
                            f.write(requests.get(link, headers=headers).content)
        except:
            print('the call is prohibited,need password!')

        n = n + 100  # set the length of the visiting


def get_album_data(album_link):
    '''

    :param album_link: <str> the link of personal data
    :return: <list> the album name, id, pictures and album numbers
    '''
    html_data = requests.get(album_link, headers=headers)
    album_name = re.findall('"albumName":"(.*?)"', html_data.text, re.S)
    print('directly match the album name', album_name)
    album_id = re.findall('"albumId":"(.*?)"', html_data.text, re.S)
    album_photoNumber = re.findall('"photoCount":(.*?),', html_data.text, re.S)
    album_number = re.findall("albumCount': (.*?),", html_data.text, re.S)
    person = re.findall('<title>人人网 - (.*?)的相册</title>', html_data.text, re.S)
    print('各相册信息：', album_name, album_id, album_photoNumber, album_number, person)
    return album_name, album_id, album_photoNumber, album_number, person


def make_file(person, album_name, album_id):
    '''
    Build the parent folder and second folder, if the folder has existed, do not build.
    else build the folder and return key = 1 else reutun key = 0
    :param person: <str> the person name
    :param album_name: <str> the album name
    :param album_id: <str> the id
    :return: the address of the album
    '''
    file_path = ''
    album_name = album_name.encode('utf-8').decode('unicode_escape')
    if os.path.exists((os.getcwd() + '\人人网相册' + '/' + person)):
        key = 1
    else:
        try:
            os.mkdir(os.getcwd() + '\人人网相册' + '/' + person)
            key = 1
        except:
            key = 0
            print(key, '文件夹《' + person + '》创建失败，请查看命名方式！')

    if key == 1:
        file_path = os.getcwd() + '/人人网相册' + '/' + person + '/' + album_name + '_' + album_id
        if os.path.exists(file_path):
            pass
        else:
            try:
                os.mkdir(file_path)
            except:
                print(key, '文件夹《' + album_name + '_' + album_id + '》创建失败，请查看命名方式！')
                key = 0
    if key == 1:
        return file_path
    else:
        return None


def get_album_link(user_link):
    '''
    :param user_link: <str>
    :return: <str>
    '''
    html_data = requests.get(user_link, headers=headers)
    album_link = re.findall('"(.*?)">相册', html_data.text)[0] + '?showAll=1'  # get the personal album link
    print('personal album link: ', album_link)
    return album_link


if __name__ == '__main__':
    Host_url = 'http://www.renren.com/391684145/profile'
    Host_id = Host_url.split('/')[-2]
    data = get_album_data(get_album_link(Host_url))
    person = data[4][0]
    album_number = int(data[3][0])
    for i in range(0, album_number):
        each_album_link = 'http://photo.renren.com/photo/' + Host_id + 'album' + data[1][i] + '/v7'
    print(each_album_link)
    album_name = data[0][i]
    album_photoNumber = int(data[2][i])
    download_photo(each_album_link, album_photoNumber, album_name, data[1][i], person)
