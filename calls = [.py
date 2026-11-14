calls = [
    "seeds not received seeds delayed",
    "fertiliser price high",
    "seeds price high subsidy not received",
]
STOP = {"not", "high"}

def frequencies(texts, stop):
    # TODO 1: Return word -> count dictionary using dict.get()
    freq_dict = {}
    for text in texts:
        for word in text.split():
            if word not in stop:
                freq_dict[word] = freq_dict.get(word, 0) + 1
    return freq_dict

def top(counts, k):
    # TODO 2: Return k most frequent (word, count) pairs; highest count first, alphabetical for ties
    sorted_items = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return sorted_items[:k]

print(top(frequencies(calls, STOP), 3))