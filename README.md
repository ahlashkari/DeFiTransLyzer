# DeFiTranLyzer
# DeFi Security: DeFi Transaction Analyzer and Feature Extractor (DeFiTranLyzer-V1.0)

As part of the Understanding Cybersecurity Series (UCS), DeFiTransLyzer is an open-source Python framework developed to extract and analyze features from Ethereum wallets and transactions for DeFi research.

The Wallet Analyzer module processes JSON-based wallet records and generates a comprehensive summary of wallet behaviors. It computes statistical measures such as averages, variance, skewness, and coefficients of variation for key elements like gas price, cumulative gas usage, and transaction values. It also captures wallet-specific dynamics, including transaction durations, error rates, and the distribution of unique interacting addresses. The output is delivered as a flattened feature dictionary that encapsulates wallet-level activities in a structured and interpretable format.

The Transaction Analyzer module complements this process by parsing individual transaction data. It extracts gas usage metrics, transaction values, effective gas prices, and cumulative gas consumption, while also processing event logs and token transfers. By normalizing transfer amounts and computing ratios such as gas price-to-efficiency, it provides a nuanced view of transaction efficiency. The module further incorporates structural insights by identifying contract creation events, self-interacting addresses, and detailed log characteristics such as log counts, removed states, and normalized transfer values. The processed results are returned as a flattened dictionary that provides a structured snapshot of transaction-level behaviors.

Together, the Wallet Analyzer and Transaction Analyzer offer a unified toolchain for profiling Ethereum blockchain activity. By systematically capturing both wallet- and transaction-level features, DeFiTransLyzer provides a detailed analytical framework that supports vulnerability research, behavioral modeling, and the broader study of decentralized finance ecosystems.

![](https://github.com/ahlashkari/DeFiTransLyzer/blob/main/DeFiTranLyzer_architecture.jpg)

# Table of Contents

- [Installation](#installation)
- [Extracted Features](#extracted-features)
  * [DeFiTransLyzer Features Details: Transaction](#Transaction)
  * [DeFiTranLyzer Features Details: Wallet](#Wallet)
  * [Statistical Information Calculation](#statistical-information-calculation)
- [Output](#output)
- [Copyright (c) 2023](#copyright-c-2023)
- [Contributing](#contributing)
- [Project Team Members](#project-team-members)
- [Acknowledgment](#acknowledgment)


You must install the requirements in your system before you can begin installing or running anything. To do so, you can easily run this command:

```bash
sudo pip3 install -r requirements.txt
```

You are now ready to execute DeFiTransLyzer-, run this command:

```bash
python main.py path_to_solidity_source_file.sol
```
Also, this project has been successfully tested on Windows10, OS X. 

# Extracted Features

![](https://github.com/ahlashkari/DeFiTransLyzer/blob/main/DeFiTransLyzer_features.jpg)

## Transaction
Transaction-level features capture the intrinsic properties of **individual Ethereum transactions**, including address characteristics, gas consumption, log details, block metadata, execution status, and token transfers. These features are primarily descriptive, though some involve direct calculations such as total gas cost ($\text{gasused} \times \text{effectivegasprice}$) or gas efficiency ($\text{value}/\text{gasused}$). Together, they provide a fine-grained view of how each transaction behaves on-chain.

➡️ *See the table below for full feature details.*


| SubCat.                     | Feature name            | Description                                                       |
|----------------------------|-------------------------|-------------------------------------------------------------------|
| Address Related            | length__from_address       | The length of the 'from' address in the transaction.              |
|                            | length_to_address         | The length of the 'to' address in the transaction.                |
|                            | from_is_same_as_to_address   | Boolean indicating if the 'from' and 'to' addresses are the same. |
| Gas Related                | gasused                 | The amount of gas used for the transaction.                       |
|                            | effectivegasprice       | The price per unit of gas paid in the transaction.                |
|                            | totalgascost            | The total cost of gas used (gasused * effectivegasprice).         |
|                            | gasperlogevent          | Gas used per log event in the transaction.                        |
|                            | cumulativegasused       | Total gas used in the block up to this transaction.               |
|                            | gaspriceratio           | Ratio of gas price to some baseline or previous price.            |
|                            | gasefficiency           | A measure of transaction efficiency based on gas usage.           |
| Log Related                | logcount                | Number of log entries in the transaction.                         |
|                            | logremoved              | Indicates whether any logs were removed.                          |
|                            | logindex                | Index of the log within the transaction.                          |
|                            | lengthlog               | Length of the log data.                                           |
| Block Related              | value                   | The value transferred in the transaction.                         |
|                            | index                   | Transaction index in the block.                                   |
|                            | chainid                 | Identifier of the blockchain network.                             |
|                            | blocknumber             | The block number in which the transaction is recorded.            |
|                            | comingfromcontract      | Boolean indicating if the transaction originated from a contract. |
|                            | lengthtransactionhash   | Length of the transaction hash.                                   |
| Transaction Status Related | eventactivityflag       | Flag indicating specific event activity.                          |
|                            | message                 | Message associated with the transaction.                          |
|                            | status                  | Status of the transaction (e.g., success, fail).                  |
|                            | Error!                  | Any errors returned by the transaction execution.                 |
| Token Related              | tokentransferamount     | Amount of tokens transferred in the transaction.                  |
|                            | normalizedtokentransfer | Normalized value of tokens transferred.                           |

## Wallet
Wallet-level features represent aggregated statistics derived from all transactions associated with a given wallet. Instead of raw values, they summarize behavioral patterns across transactions using statistical measures such as summation, average, median, variance, standard deviation, skewness, and coefficient of variation. These allow deeper profiling of wallet activity over time, highlighting trends and anomalies such as unusually high gas costs, irregular nonce increments, or abnormal value transfers.

➡️ *See the table below for full feature details.*

| SubCat.                     | Feture name                             | Description                                                |
|-----------------------------|-----------------------------------------|------------------------------------------------------------|
| Error Related               | numberoferrors                          | Total number of errors     encountered.                    |
|                             | errorrate                               | Proportion of transactions that resulted in errors.        |
| GasUsed Related             | gasusedsummation                        | Sum of gas used across     transactions.                   |
|                             | gasusedaverage                          | Average gas used per transaction.                          |
|                             | gasusedmedian                           | Median gas used per transaction.                           |
|                             | gasusedstandarddeviation                | Standard deviation of gas used.                            |
|                             | gasusedmaximumval                       | Maximum gas used in a single     transaction.              |
|                             | gasusedminimumval                       | Minimum gas used across     transactions.                  |
|                             | gasusedvariance                         | Variance of gas used across     transactions.              |
|                             | gasusedrangevalue                       | Range between maximum and minimum     gas used.            |
|                             | gasusedskewness                         | Skewness of the gas used distribution.                     |
|                             | gasusedmode                             | Mode of the gas used across transactions.                  |
|                             | gasusedcoefficientofvariation           | Coefficient of variation of gas used.                      |
| Gas Prices Related          | gaspricessummation                      | Sum of gas prices across     transactions.                 |
|                             | gaspricesaverage                        | Average gas prices per     transaction.                    |
|                             | gaspricesmedian                         | Median gas prices per transaction.                         |
|                             | gaspricesstandarddeviation              | Standard deviation of gas prices.                          |
|                             | gaspricesmaximumval                     | Maximum gas price in a single     transaction.             |
|                             | gaspricesminimumval                     | Minimum gas prices across     transactions.                |
|                             | gaspricesvariance                       | Variance of gas prices across     transactions.            |
|                             | gaspricesrangevalue                     | Range between maximum and minimum     gas prices.          |
|                             | gaspricesskewness                       | Skewness of the gas prices     distribution.               |
|                             | gaspricesmode                           | Mode of the gas prices across     transactions.            |
|                             | gaspricescoefficientofvariation         | Coefficient of variation of gas     prices.                |
| Cumulative Gas Used Related | cumulativeGasUsedsummation              | Sum of cumulative gas used across     transactions.        |
|                             | cumulativeGasUsedaverage                | Average cumulative gas used per     transaction.           |
|                             | cumulativeGasUsedmedian                 | Median cumulative gas used per     transaction.            |
|                             | cumulativeGasUsedstandarddeviation      | Standard deviation of cumulative     gas used.             |
|                             | cumulativeGasUsedmaximumval             | Maximum cumulative gas used in a     single transaction.   |
|                             | cumulativeGasUsedminimumval             | Minimum cumulative gas used across     transactions.       |
|                             | cumulativeGasUsedvariance               | Variance of cumulative gas used     across transactions.   |
|                             | cumulativeGasUsedrangevalue             | Range between maximum and minimum     cumulative gas used. |
|                             | cumulativeGasUsedskewness               | Skewness of the cumulative gas     used distribution.      |
|                             | cumulativeGasUsedmode                   | Mode of the cumulative gas used     across transactions.   |
|                             | cumulativeGasUsedcoefficientofvariation | Coefficient of variation of     cumulative gas used.       |
| Values Related              | valuessummation                         | Sum of values transferred across     transactions.         |
|                             | valuesaverage                           | Average value transferred per     transaction.             |
|                             | valuesmedian                            | Median value transferred per     transaction.              |
|                             | valuesstandarddeviation                 | Standard deviation of values     transferred.              |
|                             | valuesmaximumval                        | Maximum value transferred in a     single transaction.     |
|                             | valuesminimumval                        | Minimum value transferred across     transactions.         |
|                             | valuesvariance                          | Variance of values transferred     across transactions.    |
|                             | valuesrangevalue                        | Range between maximum and minimum     values transferred.  |
|                             | valuesskewness                          | Skewness of the values transferred     distribution.       |
|                             | valuesmode                              | Mode of the values transferred     across transactions.    |
|                             | valuescoefficientofvariation            | Coefficient of variation of values     transferred.        |
| Nonce Related               | noncesummation                          | Sum of nonce values used across     transactions.          |
|                             | nonceaverage                            | Average nonce used per     transaction.                    |
|                             | noncemedian                             | Median nonce used per transaction.                         |
|                             | noncestandarddeviation                  | Standard deviation of nonce used.                          |
|                             | noncemaximumval                         | Maximum nonce used in a single     transaction.            |
|                             | nonceminimumval                         | Minimum nonce used across     transactions.                |
|                             | noncevariance                           | Variance of nonce used across     transactions.            |
|                             | noncerangevalue                         | Range between maximum and minimum     nonce used.          |
|                             | nonceskewness                           | Skewness of the nonce used     distribution.               |
|                             | noncemode                               | Mode of the nonce used across     transactions.            |
|                             | noncecoefficientofvariation             | Coefficient of variation of nonce used.                    |
| Count Related               | numberoffromaddress                     | Total number of 'from' addresses used.                     |
|                             | numberofuniquefromaddress               | Number of unique 'from' addresses.                         |
|                             | numberoftoaddress                       | Total number of 'to' addresses     involved.               |
|                             | numberofuniquetoaddress                 | Number of unique 'to' addresses.                           |
|                             | numtransaction                          | Total number of transactions.                              |
|                             | duration                                | Time duration from the first to     the last transaction.  |

## Statistical Information Calculation
The following statistical parameters are used across wallet-level features:

* **Summation ($\sum x_i$)**: Total of all values.
* **Average / Mean ($\mu = \frac{1}{n}\sum x_i$)**: Central tendency.
* **Median**: Middle value in the ordered distribution.
* **Standard Deviation ($\sigma = \sqrt{\frac{1}{n}\sum (x_i - \mu)^2}$)**: Dispersion around the mean.
* **Variance ($\sigma^2$)**: Squared deviation measure.
* **Range ($\max(x) - \min(x)$)**: Spread between maximum and minimum values.
* **Skewness**: Degree of asymmetry in the distribution.
* **Mode**: Most frequent value.
* **Coefficient of Variation (CV = $\sigma / \mu$)**: Normalized variability relative to the mean.

# Copyright (c) 2023

DeFiTransLyzer V1.0: For citation in your works and also understanding DeFiTransLyzer V1.0 completely, you can find below-published papers:

[Arash Habibi Lashkari, Sepideh Hajihosseinkhani, Joshua Duarte, Isabella Lopez, Ziba Habibi Lashkari, Sergio Rios-Aguilar, “Advanced Genetic Algorithm and Penalty Fitness Function for Enhancing DeFi Security and Detecting Ethereum Fraud Transactions”, Blockchain: Research and Applications, Available online 3 September 2025]((https://www.sciencedirect.com/science/article/pii/S2096720925001034))


### Project Team members 

* [**Arash Habibi Lashkari:**](http://ahlashkari.com/index.asp) Founder and Project Owner 

* [**Sepideh HajHosseinkhani:**](https://github.com/Sepid-99) Researcher and Developer 

### Acknowledgement 
This project has been made possible through funding from the Natural Sciences and Engineering Research Council of Canada — NSERC (#RGPIN-2020-04701) and Canada Research Chair (Tier II) - (#CRC-2021-00340) to Arash Habibi Lashkari.

