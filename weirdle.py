import random
from collections import namedtuple
Answer = namedtuple('Answer', ['guess', 'gbo', 'word'])
Result = namedtuple('Result', ['score', 'gbo'])
WordToResult = namedtuple('WordToResult', ['word', 'result'])

class Weirdle:
    words: list[str] = []
    initial_words: list[str] = []
    answers: list = []
    attempts_remaining: int

    def __init__(self):
        f = open("words.txt", "r")
        wordlist = f.read().splitlines()
        self.words = list(
            filter(
                lambda word: set("0123456789-'.").intersection(set(word)) == set(),
                wordlist,
            )
        )
        self.initial_words = self.words.copy()
        self.attempts_remaining = 6

    def result(self, input, word):
        score = 0
        gbo = []
        for i in range(0, 5):
            if input[i] == word[i]:
                score += 100
                gbo.append("Green")
                # don't allow any further matches on this character
                word = word[:i] + "-" + word[i + 1 :]
            elif input[i] in word:
                score += 50
                gbo.append("Orange")
                # don't allow any further matches on this character
                pos = word.find(input[i])
                word = word[:pos] + "-" + word[pos + 1 :]
            else:
                score += random.randint(1, 100) / 10
                gbo.append("Black")
        return Result(score, gbo)

    def guess(self, input: str):

        # first check that the guessed word exists
        if input not in self.initial_words:
            print("Word does not exist, try again.")
            return
        else:
            self.attempts_remaining -= 1

        # give each word left in words a score, based on how it matches with input
        scored = [WordToResult(word=word, result=self.result(input, word)) for word in self.words]

        def get_score(elem: WordToResult):
            return elem.result.score

        # use a low ranked one of these to produce the answer we'll give the player
        candidate = sorted(scored, key=get_score)[int(len(scored) / 10)]
        print((input, candidate.result.gbo))

        if set(candidate.result.gbo) == {"Green"}:
            print("Hooray!")
            exit()

        self.answers.append(Answer(input, candidate.result.gbo, candidate.word))

        # now filter the available candidates
        new_words = []
        last_answer = self.answers[-1]

        for word in self.words:
            could_be = True

            # ensure we keep at least the word behind the last score
            if word == last_answer.word:
                new_words.append(word)
                continue

            reason = ""
            for i in range(0, 5):
                if last_answer.gbo[i] == "Black" and last_answer.guess[i] in word:
                    could_be = False
                    reason = "B"
                    break
                elif last_answer.gbo[i] == "Orange" and (
                    last_answer.guess[i] not in word or last_answer.guess[i] == word[i]
                ):
                    could_be = False
                    reason = "O"
                    break
                elif last_answer.gbo[i] == "Green" and last_answer.guess[i] != word[i]:
                    could_be = False
                    reason = "G"
                    break
            if could_be == True:
                new_words.append(word)

        self.words = new_words.copy()


while True:
    weirdle = Weirdle()

    print("New game started. Guess the 5 letter word...")

    while weirdle.attempts_remaining > 0:
        guess = input("Enter guess:")
        weirdle.guess(guess)

    print("Sorry, you're too rubbish. The word was %s.\n" % weirdle.answers[-1].word)
