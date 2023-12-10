# weirdle
a weird version of wordle

## how to play
In the command line like `python weirdle.py`. It plays like the regular wordle game where the result of your guess is shown per character, and is either:
 - black: character not present in the word
 - orange: character is present in the word, but not at this location
 - green: character is in the word in this position

### example
```
> python3 weirdle.py
New game started. Guess the 5 letter word...
Enter guess:shade
('shade', ['Black', 'Black', 'Orange', 'Black', 'Black'])
```
