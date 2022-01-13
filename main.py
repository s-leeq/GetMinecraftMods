import requests
import wget
import os
import yaml


def cf_mod_download(envdir, mcgameversion, modid, apikey):
    api_root = 'https://api.curseforge.com'
    api_headers = {
        'Accept': 'application/json',
        'x-api-key': apikey
    }
    mod_url = api_root + '/v1/mods/' + str(modid)
    download_dir = envdir + '/' + mcgameversion + '/'

    api_get_mod = requests.get(mod_url, headers=api_headers).json()  # 调用 API 并转换为 Python Dictionary 类型

    if not os.path.exists(download_dir):  # 判断游戏版本文件夹是否存在
        os.mkdir(download_dir)
    exist_files_index = os.listdir(download_dir)  # 获取已下载文件名, 以供判断版本更新之需

    latest_files_indexes = api_get_mod['data']['latestFilesIndexes']  # API 中的 mod 文件索引
    latest_files = api_get_mod['data']['latestFiles']  # API 中的 mod 文件详情
    for index in latest_files_indexes:
        if index['modLoader'] == 4 and index['releaseType'] != 3 and index['gameVersion'] == mcgameversion:
            for file in latest_files:
                if file['id'] == index['fileId']:
                    if not os.path.exists(download_dir+'/'+file['fileName']):
                        wget.download(file['downloadUrl'],
                                      out=download_dir + index['filename'])  # 无新版本, 跳过
                        for exist_file in exist_files_index:
                            if exist_file[0:6] == index['filename'][0:6] and exist_file != index['filename'][0:6]:
                                os.remove(download_dir+exist_file)  # 有新版本, 下载并删除旧版本


def main():
    env_dir = os.getcwd()

    index = open(env_dir+'/index.yaml')
    index_dict = yaml.load(index.read(), Loader=yaml.FullLoader)
    index.close()

    mc_game_version = index_dict['minecraft_version']
    download_path = index_dict['download_path']
    cf_mods = index_dict['cf_mods']
    api_key = index_dict['api_key']

    for mod_id in cf_mods.values():
        cf_mod_download(download_path, mc_game_version, mod_id, api_key)


if __name__ == '__main__':
    main()
