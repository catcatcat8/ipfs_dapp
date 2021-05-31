#!/usr/bin/python3

import brownie

def test_add_get_hash(ipfs, accounts):
    our_hash = "our_hash"
    ipfs.addHash(our_hash, {'from': accounts[0]})

    assert ipfs.getHash(accounts[0]) == our_hash