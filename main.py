# Лебедев Евгений name-сервис для создания профилей пользователей в IPFS

import sys
import ipfsApi
import os
from brownie import Contract, accounts, network
import webbrowser
from PIL import Image
                    

def add_to_ipfs(filename):
    """Добавляет файл в IPFS, возвращает ipfs-link"""

    check_file = os.path.exists(f'{file_name}')
    if (check_file):
        api = ipfsApi.Client('127.0.0.1', 5001)  # требует ipfs-daemon заранее
        res = api.add(f'{filename}')  # добавление в ipfs
    
        ipfs_link = res["Hash"]

        return ipfs_link

    else:
        return "No such file"


def add_to_contract(contract_address, ipfs_hash, account_id):
    """Добавляет ipsf-hash в контракт"""

    network.connect('ropsten')
    accounts.load(f'{account_id}')

    contract = Contract(f'{contract_address}')
    contract.addHash(ipfs_hash, {'from': accounts[0]})


def get_from_ipfs(contract_address, address, account_id):
    """Загружает hash из контракта по адресу, загружает из ipfs, возвращает имя нового файла"""

    api = ipfsApi.Client('127.0.0.1', 5001)  # требует ipfs-daemon заранее

    network.connect('ropsten')
    accounts.load(f'{account_id}')

    contract = Contract(contract_address)
    ipfs_hash = contract.getHash(address, {'from': accounts[0]})

    bin_file = open(f'{ipfs_hash}.bin', "w")

    os.system(f'ipfs cat /ipfs/{ipfs_hash} >> {ipfs_hash}.bin')  # возвращает data из ipfs в бинарный файл
    return f'{ipfs_hash}.bin'


def show(filename):
    """Демонстрирует файл, скачанный из ipfs, в браузере, а также открывает его в средстве просмотра изображений"""

    img = Image.open(filename)
    img.show()
    webbrowser.open(f'{filename}')


if __name__ == "__main__":

    try: 
        (sys.argv[1])
    except IndexError:
        # Для отладки через IDE
        file_name = "slava_kpss.png"
        contract_address = "0x4d2E468ECED124faC29bB00D8Df49062bAA18A0F"
        command = "get"
    else:
        if sys.argv[1] == "--add":
            file_name = sys.argv[2]
            contract_address = sys.argv[3]
            account_id = sys.argv[4]
            command = "add"
        elif sys.argv[1] == "--get":
            address = sys.argv[2]
            contract_address = sys.argv[3]
            account_id = sys.argv[4]
            command = "get"
    

    # --- Режим добавления файла в ipfs и записи ipfs_hash в контракт
    if command=="add":
        ipfs_link = add_to_ipfs(file_name)

        print(f'Ipfs hash: {ipfs_link}')

        if (ipfs_link != "No such file"):
            add_to_contract(contract_address, ipfs_link, account_id)


    # --- Режим запроса ipfs_hash по адресу из контракта и возвращения данных из ipfs
    if command == "get":
        file_from_ipfs = get_from_ipfs(contract_address, address, account_id)
        print (f'File: {file_from_ipfs}')

        show(file_from_ipfs)