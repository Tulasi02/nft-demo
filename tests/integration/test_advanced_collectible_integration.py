from brownie import network
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, get_contract
from scripts.advanced_collectible.deploy_and_create import deploy_and_create
import pytest
import time


def test_can_create_advanced_collectible_integration():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for integration testing")
    advanced_collectible, creation_tx = deploy_and_create()
    time.sleep(180)
    # assert advanced_collectible.tokenCounter() == 1
    assert advanced_collectible.tokenCounter() == 1