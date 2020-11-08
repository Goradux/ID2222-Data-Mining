def read_baskets():
    baskets = []
    with open('T10I4D100K.dat') as f:
        for line in f:
            items = line.split(' ')
            items.remove('\n')
            baskets.append(list(map(int, items)))
    return baskets


def count_singletons(baskets):
    count = {}
    for basket in baskets:
        for item in basket:
            if item in count:
                count[item] += 1
            else:
                count[item] = 1
    return count


def filter_frequent_items(items_count, support):
    return [item for item in items_count if items_count[item] >= support]


def generate_candidates(items, singletons):
    candidates = {}
    for item in items:
        for singleton in singletons:
            if singleton[0] not in item:
                candidate = tuple(sorted(item + singleton))
                if candidate not in candidates:
                    candidates[candidate] = 0
    return candidates


# SLOW IMPLEMENTATION: Check if each item of candidate tuples exists in basket
# def count_candidates(baskets, candidates, candidate_length):
#     for basket in baskets:
#         for candidate in candidates:
#             in_basket = True
#             for item in candidate:
#                 if item not in basket:
#                     in_basket = False
#                     break
#             if in_basket:
#                 candidates[candidate] += 1
#     return candidates


# FAST IMPLEMENTATION: Generate all possible basket items combinations and check if they exist in candidates
def count_candidates(baskets, candidates, candidate_length):
    for basket in baskets:
        basket_variations = generate_basket_item_combinations(basket, candidate_length)
        for combination in basket_variations:
            if combination in candidates:
                candidates[combination] += 1
    return candidates


def generate_basket_item_combinations(basket, length):
    if length == 1:
        return [(i,) for i in basket]
    combinations = []
    for i in range(len(basket)):
        for j in generate_basket_item_combinations(basket[i + 1:], length - 1):
            combinations.append((basket[i],) + j)
    return combinations



def main():
    support = 1000
    frequent_itemsets = []  # Results

    baskets = read_baskets()                                                # Read data file
    singletons_count = count_singletons(baskets)                            # Find and count singletons
    frequent_singletons = filter_frequent_items(singletons_count, support)  # Filter frequent singletons
    frequent_itemsets.append([(i,) for i in frequent_singletons])            # Wrap singletons in tuple to use the same data structure for pairs, triplets, etc..
    print("Frequent singletons:", frequent_singletons)

    k = 1
    while len(frequent_itemsets[k - 1]) > 0:    # While new frequent elements are found
        candidates = generate_candidates(frequent_itemsets[k - 1], frequent_itemsets[0])     # Generate candidates from previous frequent itemset and singletons
        candidates_count = count_candidates(baskets, candidates, k + 1) # Count candidates frequency
        frequent_itemset = filter_frequent_items(candidates_count, support)                  # Filter frequent items
        frequent_itemsets.append(frequent_itemset)
        print("Frequent " + str(k + 1) + "-tuples:", frequent_itemsets[k])
        k += 1


import time
start_time = time.time()
main()
print("--- %s seconds ---" % (time.time() - start_time))
