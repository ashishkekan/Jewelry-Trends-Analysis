from django.shortcuts import render

from .models import JewelryInventory, JewelrySales
from .utils import (
    adjust_for_unsold,
    frequent_pattern_mining,
    get_transactions,
    pointwise_mutual_information,
)


def home(request):
    return render(request, "home.html")


def analyze_trends(request):
    sales_transactions = get_transactions(JewelrySales)
    inventory_transactions = get_transactions(JewelryInventory)

    frequent_patterns = frequent_pattern_mining(sales_transactions, min_support=0.1)
    adjusted_patterns = adjust_for_unsold(frequent_patterns, inventory_transactions)

    pmi_results = pointwise_mutual_information(sales_transactions, min_pmi=0.5)

    heatmap_data = []
    labels = set()
    for pattern, support in adjusted_patterns.items():
        labels.update(pattern)
    labels = sorted(labels)
    matrix = [[0] * len(labels) for _ in range(len(labels))]
    for pattern, support in adjusted_patterns.items():
        if len(pattern) == 2:
            i = labels.index(list(pattern)[0])
            j = labels.index(list(pattern)[1])
            matrix[i][j] = matrix[j][i] = support
    heatmap_data = {"labels": labels, "matrix": matrix}

    context = {
        "frequent_patterns": [(list(k), v) for k, v in adjusted_patterns.items()],
        "pmi_results": [(list(k), v) for k, v in pmi_results],
        "heatmap_data": heatmap_data,
    }
    return render(request, "trends.html", context)
