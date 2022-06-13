from brownie import AdvancedCollectible
from scripts.helpful_scripts import fund_with_link, get_account
from web3 import Web3

def main():
    account = get_account()
    advance_collectible = AdvancedCollectible[-1]
    fund_with_link(advance_collectible.address)
    creation_transaction = advance_collectible.createCollectible({"from": account})
    creation_transaction.wait(1)
    print("Collectible Created!")