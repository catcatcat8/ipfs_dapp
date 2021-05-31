#!/usr/bin/python3

from brownie import Ipfs, accounts


def main():
    acct = accounts.load('666')
    return Ipfs.deploy({'from': acct})
