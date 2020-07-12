"""
This Python file is created for building Command Line Dictionary Tool.
"""
import sys
import os
import random
from random import shuffle
import re
import requests
from dotenv import load_dotenv
load_dotenv()

# Environment Variables
API_KEY = os.getenv('API_KEY')
API_HOST = os.getenv('API_HOST')

# Global Variables
definition_url = API_HOST+'/word/{}/definitions?api_key='+API_KEY
antonym_url = API_HOST+'/word/{}/relatedWords?api_key='+API_KEY
example_url = API_HOST+'/word/{}/examples?api_key='+API_KEY
randomwords_url = API_HOST+'/words/randomWord?api_key='+API_KEY
special = []
syn = []
ant = []
definitions = []
all_list = []
hint = []
examples = []
count = 0
s = requests.Session()

class DictionaryTool():
    """Class is created to perform different dictionary operations."""
    def __init__(self):
        pass

    def shuffle_word(self, word):
        """To display the word randomly jumbled (cat => atc, tac, tca)"""
        word = list(word)
        shuffle(word)
        print(word)
        return ''.join(word)

    def play(self, count):
        """The command should display a definition, a synonym or an antonym and ask the user to guess the word."""
        
        if count == 0:
            s.synonym, s.antonym, s.word = obj.random_words(1)
            all_list.extend(s.synonym)
            definition = requests.get(definition_url.format(s.word))
            definition_json = definition.json()
            for i in range(0, len(definition_json)):
                all_list.append(definition_json[i]['text'])
            if s.antonym != 'No antonyms found':
                all_list.extend(s.antonym)
            s.question = random.choice(all_list)
            print(s.question)
            s.result = ''
            result = input('Enter the correct word: ')
        result = ''
        print(s.result)
        if result == s.word or result in s.synonym or s.result == s.word or s.result in s.synonym:
            print('Successfully solved.')
            return
        else:
            print('Incorrect word.Choose from the following: \n 1. Try again 2. Hint 3. Quit')
            incorrect_result = input()
            if incorrect_result == 1 or incorrect_result == 'try again':
                s.result = input("Try again: ")
                count += 1
                obj.play(count)
            elif incorrect_result == 2 or incorrect_result == 'hint':
                hint.extend([obj.shuffle_word(s.word) for word in s.word.split(',')])
                hint.extend(all_list)
                hint.remove(s.question)
                if s.result != '':
                    hint.remove(s.result)
                random_hint = random.choice(hint)
                s.result = input(random_hint)
                count += 1
                obj.play(count)
            elif incorrect_result == 3 or incorrect_result == 'quit':
                if s.antonym == 'No antonyms found':
                    print('Correct Word: {} \nSynonyms: {} \nDefinitions:'.format(s.word, s.synonym))
                    print(*definitions, sep='\n')
                    exit()
                else:
                    print('Correct Word: {} \nSynonyms: {} \nAntonyms: {}\nDefinitions:'.format(s.word, s.synonym, s.antonym))
                    print(*definitions, sep='\n')
                    exit()
            else:
                print('Oops. You are inputting something wrong. Please try again.')
                exit()

    def definition(self, word):
        """Display definitions of a given word."""
        request_url = (definition_url.format(word))
        response = requests.get(request_url)
        data = response.json()
        del definitions[:]
        for i, val in enumerate(data):
            definitions.append('{}) {}'.format(i+1, val['text']))
        return definitions

    def synonym_antonym(self, syn_ant, word):
        """Display synonyms/antonyms of a given word."""
        request_url = (antonym_url.format(word))
        response = requests.get(request_url)
        data = response.json()
        if response.status_code == 200:
            for i, val in enumerate(data):
                if val['relationshipType'] == 'synonym' and syn_ant == 'syn':
                    syn.extend(val['words'])
                    return syn
                if val['relationshipType'] == 'antonym' and syn_ant == 'ant':
                    ant.extend(val['words'])
                    return ant
                elif val['relationshipType'] != 'antonym' and syn_ant == 'ant':
                    return 'No antonyms found'
        elif response.status_code == 400:
            return data['error']

    def example(self, word):
        """Display examples of usage of a given word in a sentence."""
        request_url = (example_url.format(word))
        response = requests.get(request_url)
        data = response.json()
        if response.status_code == 200:
            del special[:]
            for i, val in enumerate(data['examples']):
                clean_text = (re.sub('[^a-zA-Z0-9]+', ' ', val['text']))
                special.append('{}) {}'.format(i+1, clean_text))
                examples.append(clean_text)
            return special
        elif response.status_code == 400:
            return data['error']

    def display(self, word):
        """Display Word Definitions, Word Synonyms, Word Antonyms & Word Examples for a given word."""
        print('In display')
        ex = obj.example(word)
        if ex != 'word not found':
            print('Examples:')
            print(*ex, sep='\n')
            definition = obj.definition(word)
            print('\nDefinition:')
            print(*definition, sep='\n')
            synonym = obj.synonym_antonym('syn', word)
            print('\nSynonyms:')
            print(*synonym, sep=',')
            antonym = obj.synonym_antonym('ant', word)
            if antonym != 'No antonyms found':
                print('\nAntonyms:')
                print(*antonym, sep=', ')
        else:
            print(ex)

    def random_words(self, play):
        """Display Word Definitions, Word Synonyms, Word Antonyms & Word Examples for a random word."""
        response = requests.get(randomwords_url)
        if response.status_code == 200:
            data = response.json()
            ex = obj.example(data['word'])
            if ex != 'word not found':
                definition = obj.definition(data['word'])
                synonym = obj.synonym_antonym('syn', data['word'])
                antonym = obj.synonym_antonym('ant', data['word'])
                if play == 1:
                    word = data['word']
                    return synonym, antonym, word
                print('Examples:')
                print(*ex, sep='\n')
                print('\nDefinition:')
                print(*definition, sep='\n')
                print('\nSynonyms:')
                print(*synonym, sep=',')
                if antonym != 'No antonyms found':
                    print('\nAntonyms:')
                    print(*antonym, sep=', ')
                

obj = DictionaryTool()
# ./dict
if len(sys.argv) == 1:
    obj.random_words(0)

else:
    # ./dict play
    if sys.argv[1] == 'play':
        obj.play(count)

    # ./dict defn <word>
    if sys.argv[1] == 'defn':
        definition = obj.definition(sys.argv[2])
        if definition != 'word not found':
            print(*definition, sep='\n')
        else:
            print(definition)

    # ./dict syn <word> or ./dic ant <word>
    if sys.argv[1] == 'syn' or sys.argv[1] == 'ant':
        syn_ant = obj.synonym_antonym(sys.argv[1], sys.argv[2])
        print(syn_ant)

    # ./dict ex <word>
    if sys.argv[1] == 'ex':
        ex = obj.example(sys.argv[2])
        if ex != 'word not found':
            print(*ex, sep='\n')
        else:
            print(ex)

    # ./dict <word>
    else:
        obj.display(sys.argv[1])
