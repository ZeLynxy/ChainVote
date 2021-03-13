pragma solidity >=0.7.4;
pragma experimental ABIEncoderV2;

contract ChainVote {
    struct Candidate {
        bytes32 id;
        uint totalVotes;
        string firstname;
        string lastname;
        string politicalParty;
    }
    
    struct Voter {
        bytes32 id;
        string firstname;
        string lastname;
        string gender;
        string nationalId;
        bool hasVoted;
        
    }

    mapping (bytes32 => Candidate) candidates;
    mapping (bytes32 => Voter) voters;
    uint nbCandidates = 0;
    mapping (uint => bytes32) candidatesIds;
    uint nbVoters = 0;
    
    function addCandidate(string memory tmpCandidateID, string memory firstname, string memory lastname, string memory politicalParty) public {
        bytes32 id = keccak256(abi.encodePacked(tmpCandidateID));        
        candidates[id] = Candidate(id, 0, firstname, lastname, politicalParty);
        candidatesIds[nbCandidates] = id;
        nbCandidates++;
    }
    
    function getCandidates() external view returns (bytes32[] memory, string[] memory, string[] memory, string[] memory, uint[] memory) {
        
        bytes32[] memory ids = new bytes32[](nbCandidates);
        string[] memory firstnames = new string[](nbCandidates);
        string[] memory lastnames = new string[](nbCandidates);
        string[] memory politicalParties = new string[](nbCandidates);
        uint[] memory totalVotes = new uint[](nbCandidates);
        for (uint i = 0; i < nbCandidates; i++) {
            ids[i] = candidatesIds[i];
            firstnames[i] = candidates[candidatesIds[i]].firstname;
            lastnames[i] = candidates[candidatesIds[i]].lastname;
            politicalParties[i] = candidates[candidatesIds[i]].politicalParty;
            totalVotes[i] = candidates[candidatesIds[i]].totalVotes;
        }
        return (ids, firstnames, lastnames, politicalParties, totalVotes);
    }
    
    function addVoter(string memory voterID, string memory nationalId, string memory firstname, string memory lastname, string memory gender) public {
        bytes32 id = keccak256(abi.encodePacked(voterID));        
        voters[id] = Voter(id, firstname, lastname, gender, nationalId, false);
        nbVoters++;
    }
    
    function vote(string memory voterID, bytes32 candidateID) external {
        bytes32 id = keccak256(abi.encodePacked(voterID));
        bool success_status = false;
         if(bytes(voters[id].gender).length > 0){
            if(!voters[id].hasVoted){
                candidates[candidateID].totalVotes++;
                voters[id].hasVoted = true;
                success_status = true;
            }
             
         }
    }

    function hasVoted(string memory voterID) external view returns (bool) {
        bytes32 id = keccak256(abi.encodePacked(voterID));
        return voters[id].hasVoted;
    }
}