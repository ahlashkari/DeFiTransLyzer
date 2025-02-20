import json

def parse_token_holdings(json_file_path):
    """
    Parses token holdings from the given JSON file.
    Works for both ERC-20 and ERC-721 tokens.
    For ERC-20 tokens, also captures 'TokenDivisor' if available.
    """
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    
    # Verify valid JSON response.
    if data.get("status") != "1" or not data.get("result"):
        return None
    
    tokens = []
    for token in data["result"]:
        token_info = {
            "TokenAddress": token.get("TokenAddress"),
            "TokenName": token.get("TokenName"),
            "TokenSymbol": token.get("TokenSymbol"),
            "TokenQuantity": token.get("TokenQuantity")
        }
        # Include TokenDivisor for ERC-20 tokens if present.
        if "TokenDivisor" in token:
            token_info["TokenDivisor"] = token.get("TokenDivisor")
        tokens.append(token_info)
    return tokens
