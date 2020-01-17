#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_remove,
                        hash_table_retrieve,
                        hash_table_resize)


def get_indices_of_item_weights(weights, length, limit):
    ht = HashTable(16)

    """
    YOUR CODE HERE
    """
    # Create a list that can contain enumerated weights with idxs
    indexed_weights = []
    idx = 0
    # For each item in weights, create a small tuple with an idx for each value
    # and append it to our list above
    for value in weights:
        indexed_weights.append((idx, value))
        idx += 1
    # For each key and value in the new list, insert it into the hash table with
    # the weights as keys
    for key, value in indexed_weights:
        hash_table_insert(ht, value, key)
    # For each pair inserted...
    for key, value in indexed_weights:
        # If the table has an entry for limit - value...
        if hash_table_retrieve(ht, limit - value) is not None:
            # Retrieve the index for that weight, compare it against our key to order them and return
            item_idx = hash_table_retrieve(ht, limit - value)
            if item_idx >= key:
                return [item_idx, key]
            else:
                return [key, item_idx]
    return None


def print_answer(answer):
    if answer is not None:
        print(str(answer[0] + " " + answer[1]))
    else:
        print("None")
