import time
import random
from random import randint, shuffle
from web3 import Account
from web3 import Web3
from web3.auto import w3
from termcolor import cprint
from tqdm import tqdm

#################################################################################################################
#                                                   Настройки                                                   #
#################################################################################################################
POVTOR = 3 # повтор транзакций
Min_Tranz = 50 #время между транзакциями
Max_Tranz = 100
Min_Chain = 60 #время между сетями
Max_Chain = 120
Min_Akaunt = 30 #время между аккаунтами
Max_Akaunt = 60

#################################################################################################################
#                                           Все параметры и контракты                                           #
#################################################################################################################

# Chain Parametrs
DATA = {
    'optimism'      : {'w3': Web3(Web3.HTTPProvider('https://rpc.ankr.com/optimism')),           'scan': 'https://optimistic.etherscan.io/tx'},
    'bsc'           : {'w3': Web3(Web3.HTTPProvider('https://rpc.ankr.com/bsc')),                'scan': 'https://bscscan.com/tx'},
    'polygon'       : {'w3': Web3(Web3.HTTPProvider('https://rpc.ankr.com/polygon')),            'scan': 'https://polygonscan.com/tx'},
    'arbitrum'      : {'w3': Web3(Web3.HTTPProvider('https://rpc.ankr.com/arbitrum')),           'scan': 'https://arbiscan.io/tx'},
    'avalanche'     : {'w3': Web3(Web3.HTTPProvider('https://rpc.ankr.com/avalanche')),          'scan': 'https://snowtrace.io/tx'},
    'fantom'        : {'w3': Web3(Web3.HTTPProvider('https://rpc.ankr.com/fantom')),             'scan': 'https://ftmscan.com/tx'},
    'gnosis'        : {'w3': Web3(Web3.HTTPProvider('https://rpc.ankr.com/gnosis')),             'scan': 'https://gnosisscan.io/tx'},
    'celo'          : {'w3': Web3(Web3.HTTPProvider('https://rpc.ankr.com/celo')),               'scan': 'https://celoscan.io/tx'},
    'zksync'        : {'w3': Web3(Web3.HTTPProvider('https://mainnet.era.zksync.io')),           'scan': 'https://mainnet.era.zksync.io/tx'},
    'zkevm'         : {'w3': Web3(Web3.HTTPProvider('https://rpc.ankr.com/polygon_zkevm')),      'scan': 'https://zkevm.polygonscan.com/tx'},
    'aurora'        : {'w3': Web3(Web3.HTTPProvider('https://mainnet.aurora.dev')),              'scan': 'https://explorer.aurora.dev/tx'},
    'ethereum'      : {'w3': Web3(Web3.HTTPProvider('https://rpc.ankr.com/eth')),                'scan': 'https://etherscan.io/tx'}
}

chain_ID_bungee = {
    'optimism' : 10,            'bsc'      : 56,
    'polygon'  : 137,           'arbitrum' : 42161,
    'avalanche': 43114,         'fantom'   : 250,
    'gnosis'   : 100,           'celo'     : 42220,
    'zksync'   : 324,           'zkevm'    : 1101,
    'ethereum' : 1,             'aurora'   : 1313161554
}

chain_ID = {
    '1'  : 'arbitrum',   '2' : 'optimism',  '3'  : 'bsc',
    '4'  : 'polygon',    '5' : 'avalanche', '6'  : 'fantom',
    '7'  : 'ethereum',   '8' : 'zkevm',     '9'  : 'zksync',
    '10' : 'aurora',    '11' : 'gnosis'
}

contract_address_bungee = {
    'optimism' : w3.to_checksum_address('0x5800249621da520adfdca16da20d8a5fc0f814d8'),       'bsc'      : w3.to_checksum_address('0xBE51D38547992293c89CC589105784ab60b004A9'),
    'polygon'  : w3.to_checksum_address('0xAC313d7491910516E06FBfC2A0b5BB49bb072D91'),       'arbitrum' : w3.to_checksum_address('0xc0E02AA55d10e38855e13B64A8E1387A04681A00'),
    'avalanche': w3.to_checksum_address('0x040993fbF458b95871Cd2D73Ee2E09F4AF6d56bB'),       'fantom'   : w3.to_checksum_address('0x040993fbF458b95871Cd2D73Ee2E09F4AF6d56bB'),
    'gnosis'   : w3.to_checksum_address('0xBE51D38547992293c89CC589105784ab60b004A9'),       'aurora'   : w3.to_checksum_address('0x2b42AFFD4b7C14d9B7C2579229495c052672Ccd3'),
    'ethereum' : w3.to_checksum_address('0xb584D4bE1A5470CA1a8778E9B86c81e165204599')
}

abi_bungee = '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"destinationReceiver","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"destinationChainId","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Donation","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"sender","type":"address"}],"name":"GrantSender","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Paused","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"sender","type":"address"}],"name":"RevokeSender","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"receiver","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"bytes32","name":"srcChainTxHash","type":"bytes32"}],"name":"Send","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Unpaused","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"receiver","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Withdrawal","type":"event"},{"inputs":[{"components":[{"internalType":"uint256","name":"chainId","type":"uint256"},{"internalType":"bool","name":"isEnabled","type":"bool"}],"internalType":"struct GasMovr.ChainData[]","name":"_routes","type":"tuple[]"}],"name":"addRoutes","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address payable[]","name":"receivers","type":"address[]"},{"internalType":"uint256[]","name":"amounts","type":"uint256[]"},{"internalType":"bytes32[]","name":"srcChainTxHashes","type":"bytes32[]"},{"internalType":"uint256","name":"perUserGasAmount","type":"uint256"},{"internalType":"uint256","name":"maxLimit","type":"uint256"}],"name":"batchSendNativeToken","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"chainConfig","outputs":[{"internalType":"uint256","name":"chainId","type":"uint256"},{"internalType":"bool","name":"isEnabled","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"destinationChainId","type":"uint256"},{"internalType":"address","name":"_to","type":"address"}],"name":"depositNativeToken","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"chainId","type":"uint256"}],"name":"getChainData","outputs":[{"components":[{"internalType":"uint256","name":"chainId","type":"uint256"},{"internalType":"bool","name":"isEnabled","type":"bool"}],"internalType":"struct GasMovr.ChainData","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"}],"name":"grantSenderRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"paused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"name":"processedHashes","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"}],"name":"revokeSenderRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address payable","name":"receiver","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"bytes32","name":"srcChainTxHash","type":"bytes32"},{"internalType":"uint256","name":"perUserGasAmount","type":"uint256"},{"internalType":"uint256","name":"maxLimit","type":"uint256"}],"name":"sendNativeToken","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"senders","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"chainId","type":"uint256"},{"internalType":"bool","name":"_isEnabled","type":"bool"}],"name":"setIsEnabled","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"setPause","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"setUnPause","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"withdrawBalance","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_to","type":"address"}],"name":"withdrawFullBalance","outputs":[],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]'

contract_bungee = {
    'optimism' : DATA['optimism']       ['w3'].eth.contract(address=contract_address_bungee['optimism'],   abi=abi_bungee),
    'bsc'      : DATA['bsc']            ['w3'].eth.contract(address=contract_address_bungee['bsc'],        abi=abi_bungee),
    'polygon'  : DATA['polygon']        ['w3'].eth.contract(address=contract_address_bungee['polygon'],    abi=abi_bungee),
    'arbitrum' : DATA['arbitrum']       ['w3'].eth.contract(address=contract_address_bungee['arbitrum'],   abi=abi_bungee),
    'avalanche': DATA['avalanche']      ['w3'].eth.contract(address=contract_address_bungee['avalanche'],  abi=abi_bungee),
    'fantom'   : DATA['fantom']         ['w3'].eth.contract(address=contract_address_bungee['fantom'],     abi=abi_bungee),
    'gnosis'   : DATA['gnosis']         ['w3'].eth.contract(address=contract_address_bungee['gnosis'],     abi=abi_bungee),
    'aurora'   : DATA['aurora']         ['w3'].eth.contract(address=contract_address_bungee['aurora'],     abi=abi_bungee),
    'ethereum' : DATA['ethereum']       ['w3'].eth.contract(address=contract_address_bungee['ethereum'],   abi=abi_bungee)
}


def sleeping(from_sleep, to_sleep):
    x = random.randint(from_sleep, to_sleep)
    for _ in tqdm(range(x), desc='sleep ', bar_format='{desc}: {n_fmt}/{total_fmt}'):
        time.sleep(1)

def reful_main(from_chain, to_chain, count):
    chain_w3 = DATA[from_chain]['w3']
    contract = contract_bungee[from_chain]

    with open('keys.txt', 'r') as keys_file:
        accounts = [Account.from_key(line.replace("\n", "")) for line in keys_file.readlines()]
    max_accaunts = accounts.__len__()
    number_accounts = 0
    count_old = count
    if count == 777:
        sbor_babla = True
    else:
        sbor_babla = False
    for account in accounts:
        number_accounts +=1
        address = w3.to_checksum_address(account.address)
        if sbor_babla:
            balance_ = chain_w3.eth.get_balance(account.address)
            count = chain_w3.from_wei(balance_, "ether")
            if from_chain == 'fantom':
                random_ = random.randint(20, 30) #разброс +-10%
                minus = float(random_/1000)
            if from_chain == 'avalanche':
                random_ = random.randint(500, 600)
                minus = float(random_ / 100000)
            if from_chain == 'bsc':
                random_ = random.randint(300, 400)
                minus = float(random_ / 1000000)
            count = float(count) - minus
        else:
            random_ = random.randint(1, 20) #разброс +-10%
            count = count_old * (110-random_)/100

        dest_chain = chain_ID_bungee[to_chain]
        source_chain = chain_ID_bungee[from_chain]

        retry = 0
        vihod = False
        while not vihod:
            try:
                swap_txn = contract.functions.depositNativeToken(dest_chain, address).build_transaction({
                    'gasPrice': chain_w3.eth.gas_price,
                    'value': Web3.to_wei(count, 'ether'),
                    'nonce': chain_w3.eth.get_transaction_count(address),
                    'chainId': source_chain})

                gasLimit = chain_w3.eth.estimate_gas(swap_txn)
                swap_txn['gas'] = int(gasLimit + gasLimit * 0.5)

                signed_swap_txn = chain_w3.eth.account.sign_transaction(swap_txn, account.key)
                swap_txn_hash = chain_w3.eth.send_raw_transaction(signed_swap_txn.rawTransaction)
                status = chain_w3.eth.wait_for_transaction_receipt(swap_txn_hash, timeout=300).status
                if status != 1:
                    raise ValueError(f'bad tx status: {status}')
                else:
                    print(f"{DATA[from_chain]['scan']}/{swap_txn_hash.hex()}")
                    cprint(f'[{account.address}] Successfully refull to [{to_chain}]!', 'green')
                    vihod = True
            except Exception as err:
                retry += 1
                cprint(f'[{account.address}] refull error: {type(err).__name__} {err}', 'red')
                if retry < POVTOR:
                    cprint(f'[{retry}/{POVTOR}] trying again...', 'yellow')
                    sleeping(15, 15)
                else:
                    vihod = True
        rnd_time = random.randint(Min_Akaunt, Max_Akaunt)  # время между аккаунтами
        if number_accounts < max_accaunts:
            print(f"Сон {rnd_time} секунд до {number_accounts + 1}/{max_accaunts} аккаунта\t")
            sleeping(rnd_time, rnd_time)

if __name__ == '__main__':
    while True:
        cprint('Выбери сеть откуда заправляем: ','blue')
        print('1. Arbitrum')
        print('2. Optimism')
        print('3. BSC')
        print('4. Polygon')
        print('5. Avalanche')
        print('6. Fantom')
        cprint('0. Закончить работу', 'red')
        nomer_from_chain = input('Номер сети: ')
        if nomer_from_chain == '0':
            break

        from_chain = chain_ID[nomer_from_chain]

        cprint('Выбери сеть куда заправляем: ', 'blue')
        print('1. Arbitrum')
        print('2. Optimism')
        print('3. BSC')
        print('4. Polygon')
        print('5. Avalanche')
        print('6. Fantom')
        print('7. Ethereum')
        print('8. Zkevm')
        print('9. Zksync Era')
        print('10. Aurora')
        print('11. Gnosis')

        nomer_to_chain = input('Номер сети: ')
        to_chain = chain_ID[nomer_to_chain]

        cprint(f'Сейчас надо будет ввести количество. Оно вводится в количестве нативного токена сети источника. Если это BSC, то, например, "0.01". И он возьмет 0.01 BNB. Разброс будет +-10%. Чтобы не палиться, минималки бери на сайте.', 'yellow')
        count = float(input('Количество нативного токена источника: '))

        reful_main(from_chain, to_chain, count)

    print("Скрипт закончил работу.")