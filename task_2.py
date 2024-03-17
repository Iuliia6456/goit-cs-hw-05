import string

from concurrent.futures import ThreadPoolExecutor
from collections import Counter, defaultdict
import matplotlib.pyplot as plt

import requests

def get_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  
        return response.text
    except requests.RequestException as e:
        return None

def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))

def map_function(word):
    return word, 1

def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()

def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)

def map_reduce(text, search_words=None):
    
    text = remove_punctuation(text)
    words = text.split()

    if search_words:
        words = [word for word in words if word in search_words]

    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))

    shuffled_values = shuffle_function(mapped_values)

    with ThreadPoolExecutor() as executor:
        reduced_values = list(executor.map(reduce_function, shuffled_values))

    return dict(reduced_values)

def visualize_top_words(result, top_n=10):
    top_words = Counter(result).most_common(top_n)
    words, counts = zip(*top_words)
    plt.bar(words, counts, color='green')
    plt.xlabel('Word')
    plt.ylabel('Count')
    plt.title('Top Words')
    plt.show()

if __name__ == '__main__':
    url = "https://gutenberg.net.au/ebooks01/0100021.txt"
    text = get_text(url)
    
    if text:
        search_words = ['war', 'peace', 'love']
        result = map_reduce(text)
        print("Word count result:", result)
    else:
        print("Error: Failed to get input text.")

    visualize_top_words(result)
