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

    latest_files_indexes = api_get_mod['data']['latestFilesIndexes']  # API 中的 mod 文件索引
    latest_files = api_get_mod['data']['latestFiles']  # API 中的 mod 文件详情
    for index in latest_files_indexes:
        if index['modLoader'] == 4 and index['releaseType'] != 3 and index['gameVersion'] == mcgameversion:
            if not os.path.exists(download_dir):
                os.mkdir(download_dir)
            for file in latest_files:
                if file['id'] == index['fileId']:
                    wget.download(file['downloadUrl'],
                                  out=download_dir + index['filename'])


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
