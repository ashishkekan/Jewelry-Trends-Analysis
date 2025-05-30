from collections import Counter
from itertools import combinations
from math import log2

import numpy as np
import pandas as pd

from .models import JewelryInventory, JewelrySales


def get_transactions(model):
    return [item.product_tags.split(",") for item in model.objects.all()]


def frequent_pattern_mining(transactions, min_support=0.1):
    item_counts = Counter()
    for transaction in transactions:
        for item in transaction:
            item_counts[item] += 1
    total = len(transactions)
    frequent_items = {
        frozenset([item]): count / total
        for item, count in item_counts.items()
        if count / total >= min_support
    }

    k = 2
    frequent_k_itemsets = frequent_items
    all_frequent = frequent_items.copy()

    while frequent_k_itemsets:
        candidates = {}
        items = list(frequent_k_itemsets.keys())
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                union = items[i] | items[j]
                if len(union) == k:
                    candidates[union] = 0
        for transaction in transactions:
            transaction_set = frozenset(transaction)
            for candidate in candidates:
                if candidate.issubset(transaction_set):
                    candidates[candidate] += 1
        frequent_k_itemsets = {
            k: v / total for k, v in candidates.items() if v / total >= min_support
        }
        all_frequent.update(frequent_k_itemsets)
        k += 1
    return all_frequent


def pointwise_mutual_information(transactions, min_pmi=0.5):
    total = len(transactions)
    item_counts = Counter()
    pair_counts = Counter()
    triplet_counts = Counter()

    for transaction in transactions:
        transaction_set = frozenset(transaction)
        for item in transaction:
            item_counts[item] += 1
        for pair in combinations(transaction, 2):
            pair_counts[frozenset(pair)] += 1
        for triplet in combinations(transaction, 3):
            triplet_counts[frozenset(triplet)] += 1

    pmi_results = []
    for pair, count in pair_counts.items():
        p_pair = count / total
        items = list(pair)
        p_a = item_counts[items[0]] / total
        p_b = item_counts[items[1]] / total
        pmi = log2(p_pair / (p_a * p_b)) if p_pair > 0 and p_a * p_b > 0 else 0
        if pmi >= min_pmi:
            pmi_results.append((pair, pmi))

    for triplet, count in triplet_counts.items():
        p_triplet = count / total
        items = list(triplet)
        p_a = item_counts[items[0]] / total
        p_b = item_counts[items[1]] / total
        p_c = item_counts[items[2]] / total
        pmi = (
            log2(p_triplet / (p_a * p_b * p_c))
            if p_triplet > 0 and p_a * p_b * p_c > 0
            else 0
        )
        if pmi >= min_pmi:
            pmi_results.append((triplet, pmi))

    return sorted(pmi_results, key=lambda x: x[1], reverse=True)


def adjust_for_unsold(frequent_patterns, unsold_transactions, penalty=0.5):
    unsold_counts = Counter()
    for transaction in unsold_transactions:
        transaction_set = frozenset(transaction)
        for pattern in frequent_patterns:
            if pattern.issubset(transaction_set):
                unsold_counts[pattern] += 1
    total_unsold = len(unsold_transactions)
    adjusted = {}
    for pattern, support in frequent_patterns.items():
        unsold_support = (
            unsold_counts.get(pattern, 0) / total_unsold if total_unsold > 0 else 0
        )
        adjusted[pattern] = support * (1 - penalty * unsold_support)
    return adjusted
