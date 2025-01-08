import json
import numpy as np
from datetime import datetime
import statistics
import scipy

def flatten_dict(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = f'{parent_key}{sep}{k}' if parent_key else k
        if isinstance(v, dict):
            # If the value is a dictionary, recursively flatten it
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            # If the value is a list, iterate over it and flatten
            for i, item in enumerate(v):
                if isinstance(item, dict):
                    items.extend(flatten_dict(item, f'{new_key}[{i}]', sep=sep).items())
                else:
                    items.append((f'{new_key}[{i}]', item))
        else:
            # If the value is not a dictionary or list, add it directly
            items.append((new_key, v))
    return dict(items)

def math_features_calc(list_of_parameters, prefix=''):
    # Ensure all values are numeric and prevent type issues
    list_of_parameters = np.array(list_of_parameters, dtype=np.float64)

    # Calculate basic statistics
    summation = sum(list_of_parameters)
    average = float(statistics.mean(list_of_parameters))
    median = float(statistics.median(list_of_parameters))
    standard_deviation = float(statistics.stdev(list_of_parameters))
    maximum_val = float(max(list_of_parameters))
    minimum_val = float(min(list_of_parameters))
    variance = float(statistics.variance(list_of_parameters))
    range_val = maximum_val - minimum_val
    mode_val = float(statistics.mode(list_of_parameters))
    coefficient_of_variation = standard_deviation / average if average != 0 else 0.0

    # Calculate skewness only if variance is above a small threshold
    if variance > 1e-9:  # Threshold to avoid precision issues
        skewness = float(scipy.stats.skew(list_of_parameters))
    else:
        skewness = 0.0

    return {
        f'{prefix}summation': summation, 
        f'{prefix}average': average, 
        f'{prefix}median': median, 
        f'{prefix}standard_deviation': standard_deviation, 
        f'{prefix}maximum_val': maximum_val, 
        f'{prefix}minimum_val': minimum_val,
        f'{prefix}variance': variance,
        f'{prefix}range_value': range_val,
        f'{prefix}skewness': skewness,
        f'{prefix}mode': mode_val,
        f'{prefix}coefficient_of_variation': coefficient_of_variation
    }

def Address_Analyzer(path):
    try:
        # Attempt to open and read the file
        with open(path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        # Handle the case where the file does not exist
        print(f"Error: The file '{path}' was not found.")
        return None
    except json.JSONDecodeError:
        # Handle the case where the file is not a valid JSON
        print(f"Error: The file '{path}' is not a valid JSON.")
        return None

    num_transfers = len(data['result[1]'])  # total transactions in the dataset  ---- WORKED!
    if num_transfers > 1:
        first_time_str = (data['result[1]'][0]['timeStamp'])
        last_time_str = (data['result[1]'][-1]['timeStamp'])
        first_time = datetime.fromtimestamp(int(first_time_str))
        last_time = datetime.fromtimestamp(int(last_time_str))
        duration = last_time-first_time # duration ---- WORKED!
        
        Txs_gas_prices_ls = []
        Txs_gas_used_ls = []
        Txs_cumulativeGasUsed_ls = []
        number_of_errors = 0
        values_ls = []
        nonce_ls = []
        from_addreses = []
        to_addresses = []
        for item in data['result[1]']:
            gas_used = int(item['gasUsed'])
            Txs_gas_used_ls.append(gas_used) 
            gas_price = int(item['gasPrice'])
            Tx_gas_price = gas_used*gas_price 
            Txs_gas_prices_ls.append(Tx_gas_price)
            Txs_cumulativeGasUsed_ls.append(int(item['cumulativeGasUsed']))
            try:
                nonce_ls.append(int(item['nonce']))
            except (ValueError, TypeError):
                nonce_ls.append(0)
            if item['isError']=='1':
                number_of_errors+=1
            values_ls.append(int(item['value']))
            error_rate = (number_of_errors/num_transfers)*100

            from_addreses.append(item['from'])
            to_addresses.append(item['to'])

        return flatten_dict({
            'num_transaction': num_transfers,
            'duration_seconds': duration.seconds, 
            'number_of_errors': number_of_errors, 'error_rate': error_rate, 
            'gas_used': math_features_calc(Txs_gas_used_ls,'gas_used_'), 
            'gas_prices': math_features_calc(Txs_gas_prices_ls,'gas_prices_'), 
            'cumulativeGasUsed': math_features_calc(Txs_cumulativeGasUsed_ls,'cumulativeGasUsed_'), 
            'values': math_features_calc(values_ls,'values_'),
            'nonce': math_features_calc(nonce_ls,'nonce_'),
            'number_of_from_address': len(from_addreses),
            'number_of_unique_from_address': len(set(from_addreses)),
            'number_of_to_address': len(to_addresses),
            'number_of_unique_to_address': len(set(to_addresses)),
            })
    else:
        return None

