import json

def parse_project_info_and_social_links(json_file_path):
    """
    Parses project information and social media links from the given JSON file.
    Expected fields include contractAddress, tokenName, symbol, tokenType, etc.
    """
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    
    # Verify valid JSON response.
    if data.get("status") != "1" or not data.get("result"):
        return None
    
    info = data["result"][0]
    project_info = {
        "contractAddress": info.get("contractAddress"),
        "tokenName": info.get("tokenName"),
        "symbol": info.get("symbol"),
        "divisor": info.get("divisor"),
        "tokenType": info.get("tokenType"),
        "totalSupply": info.get("totalSupply"),
        "blueCheckmark": info.get("blueCheckmark"),
        "description": info.get("description"),
        "website": info.get("website"),
        "email": info.get("email"),
        "blog": info.get("blog"),
        "reddit": info.get("reddit"),
        "slack": info.get("slack"),
        "facebook": info.get("facebook"),
        "twitter": info.get("twitter"),
        "bitcointalk": info.get("bitcointalk"),
        "github": info.get("github"),
        "telegram": info.get("telegram"),
        "wechat": info.get("wechat"),
        "linkedin": info.get("linkedin"),
        "discord": info.get("discord"),
        "whitepaper": info.get("whitepaper"),
        "tokenPriceUSD": info.get("tokenPriceUSD")
    }
    return project_info
