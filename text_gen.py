#!/usr/bin/env python

import sys
import random


def main():

    if len(sys.argv) != 3:
        print("\nUsage:\n\t./text_gen.py INPUT_FILE INITIAL_PHRASE")
        print("\tex: ./text_gen.py hamlet.txt \"To be\"\n")
        sys.exit()

    input_file = sys.argv[1]
    initial_phrase = sys.argv[2]

    try:
        words = ingest_training_data(input_file)
    except Exception as e:
        print(e)
        sys.exit()

    training_data = train(words)

    # print_training_data(training_data)

    print(generate_content(training_data, initial_phrase))


def ingest_training_data(input_file):
    words = []
    with open(input_file, 'r') as input_data:
        for line in input_data:
            for word in line.split():
                words.append(word)
    return words


def train(words):
    # TODO: Implement custom chain length
    training_data = {}

    for i, word in enumerate(words):
        prev_word = words[i-1] if i > 0 else None
        next_word = words[i+1] if i < len(words)-1 else None

        key = prev_word + " " + word if prev_word else word
        value = next_word if next_word else ""

        if not key in training_data:
            training_data[key] = {value: 1}
        elif not value in training_data[key]:
            training_data[key][value] = 1
        else:
            training_data[key][value] += 1

    return training_data


def generate_content(training_data, initial_phrase):
    generated = initial_phrase.split()

    for i in range(0, 100):
        phrase = " ".join(generated[-2:])
        try:
            next_word = choose_next_word(training_data, phrase)
            generated.append(next_word)
            if i > 50 and next_word[-1] in ['.', '!', '?']:
                break
        except KeyError as e:
            break

    return " ".join(generated)


def choose_next_word(training_data, phrase):
    possible_words = training_data[phrase]
    chosen_index = random.randint(0, sum(possible_words.values())-1)

    counter = 0
    for word, count in possible_words.items():
        for i in range(0, count):
            if counter == chosen_index:
                return word
            counter += 1

    raise Exception("Choosing next word failed")


def print_training_data(training_data):
    for phrase in training_data:
        print(phrase)
        for value in training_data[phrase]:
            print('\t{0}: {1}'.format(value, training_data[phrase][value]))


if __name__ == "__main__":
    main()
