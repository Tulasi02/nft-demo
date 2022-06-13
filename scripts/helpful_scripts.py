from brownie import accounts, network, config, VRFCoordinatorMock, LinkToken, Contract
from web3 import Web3
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache", "mainnet-fork"]
OPENSEA_URL = "https://testnets.opensea.io/assets/rinkeby/{}/{}"
BREED_MAPPING = {0: "PUG", 1: "SHIBA_INU", 2: "ST_BERNARD"}
contract_to_mock = {
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}


def get_breed(breed_number):
    return BREED_MAPPING[breed_number]

def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    if id:
        return accounts.load(id)
    return accounts.add(config["wallets"]["from_key"])


def get_contract(contract_name):
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


def deploy_mocks():
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks....")
    account = get_account()
    print("Deploying Mock LinkToken....")
    link_token = LinkToken.deploy({"from": account})
    print(f"LinkToken deployed to {link_token}")
    print("Deploying Mock VRF Coordinator....")
    vrf_coordinator = VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print("VRF Coordinator deployed to {vrf_coordinator}")


def fund_with_link(contract_address, account=None, link_token=None, amount=Web3.toWei(1, "ether")):  # 0.1 LINK
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address, amount, {"from": account})
    # link_token_contract = interface.LinkTokenInterface(link_token.address)
    # tx = link_token_contract.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print("Fund contract!")
    return tx
