import random


class Weirdle:
    words: list[str] = []
    initial_words: list[str] = []
    answers: list[tuple[str, list[str], str]] = []
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

    def score(self, input, word):
        score = 0
        answer = []
        for i in range(0, 5):
            if input[i] == word[i]:
                score += 100
                answer.append("Green")
                # don't allow any further matches on this character
                word = word[:i] + "-" + word[i + 1 :]
            elif input[i] in word:
                score += 50
                answer.append("Orange")
                # don't allow any further matches on this character
                pos = word.find(input[i])
                word = word[:pos] + "-" + word[pos + 1 :]
            else:
                score += random.randint(1, 100) / 10
                answer.append("Black")
        return score, answer

    def guess(self, input: str):

        # first check that the guessed word exists
        if input not in self.initial_words:
            print("Word does not exist, try again.")
            return
        else:
            self.attempts_remaining -= 1

        # give each word left in words a score, based on how it matches with input
        scored = [(word, self.score(input, word)) for word in self.words]

        def get_score(elem):
            return elem[1][0]

        # use a low ranked one of these to produce the answer we'll give the player
        answer = sorted(scored, key=get_score)[int(len(scored) / 10)]
        print((input, answer[1][1]))

        if set(answer[1][1]) == {"Green"}:
            print("Hooray!")
            exit()

        self.answers.append((input, answer[1][1], answer[0]))

        # now filter the available candidates
        new_words = []
        last_answer = self.answers[-1]

        for word in self.words:
            could_be = True

            # ensure we keep at least the word behind the last score
            if word == last_answer[2]:
                new_words.append(word)
                continue

            reason = ""
            for i in range(0, 5):
                if last_answer[1][i] == "Black" and last_answer[0][i] in word:
                    could_be = False
                    reason = "B"
                    break
                elif last_answer[1][i] == "Orange" and (
                    last_answer[0][i] not in word or last_answer[0][i] == word[i]
                ):
                    could_be = False
                    reason = "O"
                    break
                elif last_answer[1][i] == "Green" and last_answer[0][i] != word[i]:
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

    print("Sorry, you're too rubbish. The word was %s.\n" % weirdle.answers[-1][2])
