import json


class ChainVoteContractBridge:
    def __init__(self, w3_instance):
        self.w3 = w3_instance
        with open("../chainvote_contract.json", "r") as f:
            contract_data = json.load(f)
            abi = contract_data["abi"]
            self.contract_address = contract_data["contract_address"]

            self.chainvote_contract = self.w3.eth.contract(address=self.w3.toChecksumAddress(self.contract_address), abi=abi)
            print(self.chainvote_contract.address)

    def add_candidate(self, tmpCandidateID, firstname, lastname, politicalParty):
        print(tmpCandidateID)
        tx_hash = self.chainvote_contract.functions.addCandidate(tmpCandidateID, firstname, lastname, politicalParty).transact()
        receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        return receipt
    
    def get_candidates(self):
        candidates_data = self.chainvote_contract.functions.getCandidates().call()
        #print(self.w3.eth.waitForTransactionReceipt(candidates_data) )  
        #receipt = self.w3.eth.waitForTransactionReceipt(candidates_data)
        candidates_ids, candidates_firstnames, candidates_lastnames, candidates_political_parties, candidates_total_votes = candidates_data
        *candidates_ids, = map(lambda x: x.hex(), candidates_ids)
        *l, = zip (candidates_ids, candidates_firstnames, candidates_lastnames, candidates_political_parties, candidates_total_votes)
        print(l)
        return l
    
    def add_voter(self, voterID, nationalId, firstname, lastname, gender):
        tx_hash = self.chainvote_contract.functions.addVoter(voterID, nationalId, firstname, lastname, gender).transact()
        receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)    
        return receipt
    
    def vote(self, voter_id, candidate_id):
        canVote = not self.chainvote_contract.functions.hasVoted(voter_id).call()
        if canVote:
            candidate_id = bytes.fromhex(candidate_id)
            tx_hash = self.chainvote_contract.functions.vote(voter_id, candidate_id).transact()
            receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
            print(receipt)
            hasVoted = self.chainvote_contract.functions.hasVoted(voter_id).call()
            return {"canVote": canVote, "hasVoted": hasVoted}
        else:
            return {"canVote": canVote}
    


