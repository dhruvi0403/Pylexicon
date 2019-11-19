# Pylexicon
Pylexicon is a command-line dictionary tool. The simple use case of this tool is users can get antonyms, synonyms, definitions, examples just by passing a word in the command line and another major feature is one can play the game, you have to guess a word from the given definition, synonym or an antonym.

## Pre-requisites
- Python3.6+ version is required
- First of all, create .env file and declare two variables:<br/>
	API_KEY = your_api_key<br/>
	API_HOST = https://fourtytwowords.herokuapp.com


## The command-line tool has the following functions - 

1. Word Definitions

            ```python3 dictionarytool.py defn <word>```

Will display definitions of a given word.

2. Word Synonyms

            ```python3 dictionarytool.py syn <word>```

Will display synonyms of a given word. 

3. Word Antonyms

            ```python3 dictionarytool.py ant <word>```

Will display antonyms of a given word.

4. Word Examples

            ```python3 dictionarytool.py ex <word>```

Will display examples of usage of a given word in a sentence. 

5. Word Full Dict

            ```python3 dictionarytool.py <word>```

Will display Word Definitions, Word Synonyms, Word Antonyms & Word Examples for a given word.

6. Word of the Day Full Dict

            ```python3 dictionarytool.py```

Will display Word Definitions, Word Synonyms, Word Antonyms & Word Examples for a random word.

7. Word Game

            ```python3 dictionarytool.py play```

The command will display a definition, a synonym or an antonym and ask the user to guess the word. 
