def api_ballot(ballot: dict):
    ballot["_id"] = str(ballot["_id"])
    if ballot.get("candidates", []):
        for candidate in ballot.get("candidates"):
            candidate["_id"] = str(candidate["_id"])
    return ballot
