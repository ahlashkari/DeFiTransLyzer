#!/usr/bin/env python3
# main.py
"""
Run DeFiTransLyzer analyzers.

Scenarios:
  1) Address only:
     python main.py --address path/to/address.json
     -> DeFiTransLyzer_address_<address-stem>.csv

  2) Transaction only:
     python main.py --tx path/to/tx.json
     -> DeFiTransLyzer_transaction_<tx-stem>.csv

  3) Both:
     python main.py --address path/to/address.json --tx path/to/tx.json
     -> DeFiTransLyzer_details_<address-stem>__<tx-stem>.csv

Optional:
  --outdir DIR   (default: ".")
"""

import argparse
import os
import sys
import json
from typing import Any, Dict, Iterable, Tuple, List

import pandas as pd

# Your uploaded analyzers
from TX_analyzer import extract_combined_features
from address_analyzer import Address_Analyzer


# ---------------------------
# Utilities
# ---------------------------
def _basename_stem(path: str) -> str:
    """Return filename without directories and extension."""
    base = os.path.basename(path)
    stem, _ = os.path.splitext(base)
    return stem


def _flatten(obj: Any, parent_key: str = "", sep: str = ".") -> Dict[str, Any]:
    """
    Flatten nested dicts/lists into a single-level dict.
    - Dicts become key.key
    - Lists become key[idx]
    """
    items: List[Tuple[str, Any]] = []

    if isinstance(obj, dict):
        for k, v in obj.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else str(k)
            items.extend(_flatten(v, new_key, sep=sep).items())
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            new_key = f"{parent_key}[{i}]"
            items.extend(_flatten(v, new_key, sep=sep).items())
    else:
        items.append((parent_key, obj))

    # Remove empty parent_key if obj is scalar at top-level
    return {k: v for k, v in items if k}


def _to_single_row_csv(data: Dict[str, Any], outpath: str) -> None:
    """Write a single feature dict to CSV (1 row)."""
    flat = _flatten(data)
    df = pd.DataFrame([flat])
    # Make sure directory exists
    os.makedirs(os.path.dirname(os.path.abspath(outpath)), exist_ok=True)
    df.to_csv(outpath, index=False, encoding="utf-8")
    print(f"[OK] Wrote {outpath} with {df.shape[1]} columns.")


def _merge_with_prefix(addr_feats: Dict[str, Any], tx_feats: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge two dicts into one row with prefixes to avoid collisions.
    """
    out: Dict[str, Any] = {}
    for k, v in addr_feats.items():
        out[f"addr_{k}"] = v
    for k, v in tx_feats.items():
        out[f"tx_{k}"] = v
    return out


# ---------------------------
# Runners
# ---------------------------
def run_address(path: str) -> Dict[str, Any]:
    try:
        feats = Address_Analyzer(path)
        if not isinstance(feats, dict):
            raise ValueError("Address_Analyzer did not return a dict.")
        feats["_source_file"] = os.path.basename(path)
        return feats
    except Exception as e:
        sys.stderr.write(f"[ERROR][ADDRESS] {path}: {e}\n")
        return {}


def run_tx(path: str) -> Dict[str, Any]:
    try:
        feats = extract_combined_features(path)
        if not isinstance(feats, dict):
            raise ValueError("extract_combined_features did not return a dict.")
        feats["_source_file"] = os.path.basename(path)
        return feats
    except Exception as e:
        sys.stderr.write(f"[ERROR][TX] {path}: {e}\n")
        return {}


# ---------------------------
# Main
# ---------------------------
def main():
    parser = argparse.ArgumentParser(description="DeFiTransLyzer main runner.")
    parser.add_argument("--address", help="Path to a single wallet/address JSON file.")
    parser.add_argument("--tx", help="Path to a single transaction JSON file.")
    parser.add_argument("--outdir", default=".", help="Output directory (default: current working dir).")

    args = parser.parse_args()

    if not args.address and not args.tx:
        parser.error("Provide at least one of --address or --tx (each expects a single JSON file).")

    # Validate provided paths
    if args.address and (not os.path.isfile(args.address) or not args.address.lower().endswith(".json")):
        parser.error(f"--address must be a valid .json file: {args.address}")
    if args.tx and (not os.path.isfile(args.tx) or not args.tx.lower().endswith(".json")):
        parser.error(f"--tx must be a valid .json file: {args.tx}")

    outdir = args.outdir
    os.makedirs(outdir, exist_ok=True)

    addr_feats: Dict[str, Any] = {}
    tx_feats: Dict[str, Any] = {}

    if args.address:
        addr_feats = run_address(args.address)
        stem = _basename_stem(args.address)
        if addr_feats:
            outpath = os.path.join(outdir, f"DeFiTransLyzer_address_{stem}.csv")
            _to_single_row_csv(addr_feats, outpath)
        else:
            sys.stderr.write("[WARN] No address features produced; CSV not written.\n")

    if args.tx:
        tx_feats = run_tx(args.tx)
        stem = _basename_stem(args.tx)
        if tx_feats:
            outpath = os.path.join(outdir, f"DeFiTransLyzer_transaction_{stem}.csv")
            _to_single_row_csv(tx_feats, outpath)
        else:
            sys.stderr.write("[WARN] No transaction features produced; CSV not written.\n")

    # If both provided, also emit a combined, single CSV
    if args.address and args.tx and addr_feats and tx_feats:
        addr_stem = _basename_stem(args.address)
        tx_stem = _basename_stem(args.tx)
        combined = _merge_with_prefix(addr_feats, tx_feats)
        outpath = os.path.join(outdir, f"DeFiTransLyzer_details_{addr_stem}__{tx_stem}.csv")
        _to_single_row_csv(combined, outpath)


if __name__ == "__main__":
    main()
