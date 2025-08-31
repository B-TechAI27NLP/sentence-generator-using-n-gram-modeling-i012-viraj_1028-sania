import re
import random
import math
from collections import defaultdict, Counter

def preprocess_text(text):
    """Preprocesses the input text."""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s.,!?]', '', text)
    return text.split()

def build_ngram_model(tokens, n):
    """Builds an n-gram model from a list of tokens."""
    model = defaultdict(Counter)
    for i in range(len(tokens) - n):
        context = tuple(tokens[i:i + n - 1])
        next_word = tokens[i + n - 1]
        model[context][next_word] += 1
    return model

def generate_sentence(model, n, start_words, length, vocab):
    """Generates a sentence using the n-gram model."""
    sentence = list(start_words)
    vocab_list = list(vocab) # Convert set to list for random.choices

    for _ in range(length - len(start_words)):
        context = tuple(sentence[-(n - 1):])
        
        if context in model:
            counts = model[context]
            total_count = sum(counts.values()) + len(vocab)
            words = list(counts.keys())
            weights = [(count + 1) / total_count for count in counts.values()]
            
            unseen_words = [w for w in vocab_list if w not in counts]
            weights.extend([(1 / total_count) for _ in unseen_words])
            words.extend(unseen_words)

            next_word = random.choices(words, weights=weights, k=1)[0]
        else:
            # Backoff: pick a random word if context is not found
            next_word = random.choice(vocab_list)
            
        sentence.append(next_word)
        if sentence[-1] in [".", "!", "?"]:
            break
            
    return " ".join(sentence)

def calculate_perplexity(model, n, tokens, vocab):
    """Calculates the perplexity of a model on a given text."""
    log_prob = 0
    N = 0
    vocab_size = len(vocab)

    for i in range(n - 1, len(tokens)):
        context = tuple(tokens[i - n + 1:i])
        word = tokens[i]
        
        counts = model.get(context, Counter())
        total_count = sum(counts.values()) + vocab_size
        prob = (counts.get(word, 0) + 1) / total_count
        
        if prob > 0:
            log_prob += -math.log(prob)
            N += 1
            
    if N == 0:
        return float('inf')
        
    return math.exp(log_prob / N)