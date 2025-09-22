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
  * [Definitions](#definitions)
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

![](https://github.com/ahlashkari/DeFiTransLyzer/blob/main/DeFiTranLyzer_architecture.jpg)
