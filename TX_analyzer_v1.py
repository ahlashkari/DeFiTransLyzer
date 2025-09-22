import json
import os 
import re
from address_analyzer import math_features_calc

def merge_nested_dicts(d):
    """
    Merge nested dictionaries into a single level.
    """
    flat_dict = {}
    for key, value in d.items():
        if isinstance(value, dict):
            # Add the nested dictionary directly to the flat dictionary
            flat_dict.update(value)
        else:
            # Add the key-value pair as is
            flat_dict[key] = value
    return flat_dict


def extract_combined_features(path_of_file):
    match = re.search(r"_(0x[a-fA-F0-9]+)\.json", path_of_file)
    if match:
        extracted_part = match.group(1) 

    if os.path.exists(path_of_file):  
        with open(path_of_file, 'r') as json_file:
            data = json.load(json_file)  

    extracted_features = []
    first_transaction_hash = extracted_part
    gas_used = 0
    effective_gas_price = 0
    cumulative_gas_used = 0
    tx_value = 0
    tx_index = 0
    gas_price = 0
    event_activity_flag = 0
    log_removed = None # not exist!
    log_index = 'n/a' # not exist!
    length_log = None
    token_transfer_amount = 0
    merged_logs = {}

    for result in data['result']:
        if isinstance(result, dict):
            if first_transaction_hash is None:
                first_transaction_hash = result.get("transactionHash")

            if gas_used == 0:
                gas_used = int(result["gasUsed"], 16) if "gasUsed" in result else 0

            if effective_gas_price == 0:
                effective_gas_price = int(result.get("effectiveGasPrice", "0"), 16) if "effectiveGasPrice" in result else 0

            if cumulative_gas_used == 0:
                cumulative_gas_used = int(result.get("cumulativeGasUsed", "0"), 16) if "cumulativeGasUsed" in result else 0

            if tx_value == 0:
                tx_value = int(result.get("value", "0"), 16) if "value" in result else 0

            if tx_index == 0:
                tx_index = int(result.get("transactionIndex", "0"), 16) if "transactionIndex" in result else 0

            if gas_price == 0:
                gas_price = int(result.get("gasPrice", "0"), 16) if "gasPrice" in result else 0

            if "logsBloom" in result:
                emit_add = "0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
                event_activity_flag = 1 if result.get("logsBloom") != emit_add else 0

            log_count = len(result.get("logs", [])) if "logs" in result else 0


            if "logs" in result and result["logs"]:
                logs = result["logs"]
                

                for log in logs:
                    for key, value in log.items():
                        # Process specific keys for merging
                        if key == "topics":
                            value = len(value)  # Calculate length of topics
                            key = "length_log"  # Rename key for clarity
                        
                        if key == "data":
                            if value not in ["", "0x", None]:
                                hex_value = value.replace("0x", "")
                                value = int(hex_value, 16)
                            else:
                                value = 0  # Default to 0 if 'data' is empty or invalid
                            key = "token_transfer_amount"  # Rename key for clarity
                        
                        if key == "removed":
                            value = 0 if value == False else 1
                            key = "log_removed"  # Rename key for clarity
                        
                        # Add to the merged_logs dictionary
                        if key not in merged_logs:
                            merged_logs[key] = []
                        merged_logs[key].append(value)

            total_gas_cost = gas_used * effective_gas_price if gas_used and effective_gas_price else 0
            chain_id = int(result.get("chainId", "1"), 16) if "chainId" in result else 0
            from_address = result.get("from")

            to_address = result.get("to", result.get("contractAddress", None))

            is_same_address = 1 if from_address and to_address and from_address.lower() == to_address.lower() else 0

            if token_transfer_amount and cumulative_gas_used:
                if token_transfer_amount > 1e18:
                    token_transfer_amount = int(1e18)
                if cumulative_gas_used > 1e18:
                    cumulative_gas_used = int(1e18)

                normalized_token_transfer = float(token_transfer_amount) / float(cumulative_gas_used)
            else:
                normalized_token_transfer = 0

            flattened_features = {
                "transaction_hash": first_transaction_hash,
                "length_transaction_hash": len(first_transaction_hash),
                "block_number": int(result.get("blockNumber", "0"), 16) if "blockNumber" in result else None,
                # "from": from_address,
                "length_from": len(from_address) if from_address else None,
                # "to": to_address,
                "length_to": len(to_address) if to_address else None,
                "is_same_address": is_same_address,
                "gas_used": gas_used,
                "effective_gas_price": effective_gas_price,
                "total_gas_cost": total_gas_cost,
                "gas_per_log_event": gas_used / log_count if gas_used and log_count else 0,
                "token_transfer_amount": token_transfer_amount,
                "cumulative_gas_used": cumulative_gas_used,
                "gas_price_ratio": effective_gas_price / gas_price if gas_price!=0 else None,
                "gas_efficiency": cumulative_gas_used / gas_used if gas_used!=0 else None,
                "log_removed": log_removed,
                "value": tx_value,
                "index": tx_index,
                "log_count": log_count,
                "log_index": log_index,
                "length_log": length_log,
                "chain_id": chain_id,
                "event_activity_flag": event_activity_flag,
                "is_contract_creation": True if result.get("contractAddress") else False,
                "normalized_token_transfer": normalized_token_transfer,
                "status": "Success" if data.get('status', ["0"])[0] == "1" else "Failed"
            }

            flattened_features = {k: v if v is not None else 0 for k, v in flattened_features.items()}
            extracted_features.append(flattened_features)

        elif result == 'Error!' and 'Error!' in data:
            extracted_features.append({'Error!': data['Error!']})

    top_level_message = data.get("message", [None])[0]

    if 'error' in data:
        extracted_features.append({'Error!': data['error'][0]})
    else:
        extracted_features.append({'Error!': None})
    if top_level_message:
        for feature in extracted_features:
            feature['message'] = top_level_message

    flattened_extracted_features = {k: v for feature in extracted_features for k, v in feature.items()}

    for key, values in merged_logs.items():
        if len(values) > 1:
            if key == 'length_log':
                # flattened_extracted_features[key] = math_features_calc(values,'length_log_')
                flattened_extracted_features[key] = sum(values)

            if key == 'token_transfer_amount':
                # flattened_extracted_features[key] = math_features_calc(values,'token_transfer_amount_')
                flattened_extracted_features[key] = sum(values)

            if key == 'log_removed':
                log_removed_xor = 0
                for value in values:
                    log_removed_xor ^= value
                flattened_extracted_features[key] = log_removed_xor
        else:
            # flattened_extracted_features[key] = values[0]
            continue
    return merge_nested_dicts(flattened_extracted_features)
