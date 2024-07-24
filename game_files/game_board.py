import random
import nltk
from nltk.corpus import words

nltk.download('words')
# Word search
# Return true if the word can be made by using adjacent letters without repeats and false otherwise

# Returns a 2d array of letters with dimensions rows X rows
class LetterGrid:
    def __init__(self, rows):
        self.grid = []
        self.rows = rows

    def fill_grid(self):
        letters = 'ABCDEFGHIJKLMNOPRSTUVWXYZ'
        for i in range(self.rows):
            cur = []
            for j in range(self.rows):
                cur.append(random.choice(letters))
            self.grid.append(cur) 

    def fill_grid_weighted(self):
        letters = 'AAABCDEEEFGHIIJKLMNOOPSTUVWY'
        for i in range(self.rows):
            cur = []
            for j in range(self.rows):
                cur.append(random.choice(letters))
            self.grid.append(cur) 

    def fill_grid_common(self):
        letters = 'ABDEILMNOPRST'
        for i in range(self.rows):
            cur = []
            for j in range(self.rows):
                cur.append(random.choice(letters))
            self.grid.append(cur) 

    def fill_grid_explicit(self, letter_string):
        if len(letter_string) != self.rows ** 2:
            print('Letter string is invalid')
            return
        else:
            for i in range(self.rows):
                cur = letter_string[self.rows * i:self.rows * (i+1)]
                self.grid.append(cur)
    
    def display_grid(self) -> None:
        for row in self.grid:
            cur = ''
            for letter in row:
                if cur == '':
                    cur = cur + letter
                else:
                    cur = cur + ' ' + letter
            print(cur)

    def valid_word(self, word: str) -> bool:
        visited = set()
        for i in range(self.rows):
            for j in range(self.rows):
                if self.valid_word_diagonals(word, i, j, visited):
                    return True
        return False
    
    # This function checks for vertical and adjacent neighbors
    def valid_word_step(self, word: str, x_coord, y_coord) -> bool:
        if word == self.grid[x_coord][y_coord]:
            return True
        elif word[0] == self.grid[x_coord][y_coord]:
            # Run valid word on all valid neighbors and x[1:]
            # Check for above neighbor
            if x_coord - 1 >= 0:
                if self.valid_word_step(word[1:], x_coord - 1, y_coord):
                    return True
            # Check for below neighbor
            if x_coord + 1 < self.rows:
                if self.valid_word_step(word[1:], x_coord + 1, y_coord):
                    return True
            # Check for right neighbor
            if y_coord - 1 >= 0:
                if self.valid_word_step(word[1:], x_coord, y_coord - 1):
                    return True
            # Check for left neighbor
            if y_coord + 1 < self.rows:
                if self.valid_word_step(word[1:], x_coord, y_coord + 1):
                    return True
        return False
    
    # Improved step function that checks for diagonals and ensures that letters are not reused
    def valid_word_diagonals(self, word: str, x_coord, y_coord, visited) -> bool:
        if word == self.grid[x_coord][y_coord]:
            return True
        elif word[0] == self.grid[x_coord][y_coord]:
            visited.add((x_coord, y_coord))
            # Run valid word on all valid neighbors and x[1:]
            # Check for above neighbor
            if x_coord - 1 >= 0 and (x_coord-1, y_coord) not in visited:
                if self.valid_word_diagonals(word[1:], x_coord - 1, y_coord, visited):
                    return True
            # Check for below neighbor
            if x_coord + 1 < self.rows and (x_coord+1, y_coord) not in visited:
                if self.valid_word_diagonals(word[1:], x_coord + 1, y_coord, visited):
                    return True
            # Check for right neighbor
            if y_coord - 1 >= 0 and (x_coord, y_coord-1) not in visited:
                if self.valid_word_diagonals(word[1:], x_coord, y_coord - 1, visited):
                    return True
            # Check for left neighbor
            if y_coord + 1 < self.rows and (x_coord, y_coord+1) not in visited:
                if self.valid_word_diagonals(word[1:], x_coord, y_coord + 1, visited):
                    return True
            # Check for all diagonals too
            if x_coord - 1 >= 0 and y_coord - 1 >= 0 and (x_coord-1, y_coord-1) not in visited:
                if self.valid_word_diagonals(word[1:], x_coord - 1, y_coord - 1, visited):
                    return True
            if x_coord + 1 < self.rows and y_coord - 1 >= 0 and (x_coord+1, y_coord-1) not in visited:
                if self.valid_word_diagonals(word[1:], x_coord + 1, y_coord - 1, visited):
                    return True
            if y_coord + 1 < self.rows and x_coord - 1 >= 0 and (x_coord-1, y_coord+1) not in visited:
                if self.valid_word_diagonals(word[1:], x_coord - 1, y_coord + 1, visited):
                    return True
            if y_coord + 1 < self.rows and x_coord + 1 < self.rows and (x_coord+1, y_coord+1) not in visited:
                if self.valid_word_diagonals(word[1:], x_coord + 1, y_coord + 1, visited):
                    return True
        return False
    
    def score_word(self, word: str) -> int:
        # ensure word is only letters 
        score_dict = {3:1, 4:1, 5:2, 6:3, 7:5, 8:11, 9:20}
        if len(word) < 3:
            return 0
        if len(word) > 9:
            return 20
        return score_dict[len(word)]
        
    def is_english_word(self, word: str) -> bool:
        english_words = set(words.words())
        return word.lower() in english_words

    def run_game(self) -> None:
        guesses = set()
        score_dict = {0:0, 1:0, 2:0, 3:1, 4:1, 5:2, 6:3, 7:5, 8:8}
        score = 0
        print(f'\nInput valid words using adjacent letters:\n(type "done" to end)')
        user_input = input().upper()
        while user_input != 'DONE' and len(guesses) <= 5:
            if user_input in guesses:
                print(f'You already tried {user_input} try a new word')
            elif not self.valid_word(user_input):
                print(f'{user_input} is not in the grid, please try again')
            else:
                cur_score = 8 if len(user_input) > 8 else score_dict[len(user_input)]
                score += cur_score
                print(f'{user_input} scored you {cur_score} points! Total = {score}')
            guesses.add(user_input)
            self.display_grid()
            user_input = input().upper()
        print(f'Your final score is {score}')
        
    # Returns a list of the valid neighboring letters
    def get_neighbors(self, x_coord: int, y_coord: int):
        return

def main() -> None:
    board = LetterGrid(5)
    board.fill_grid()
    board.display_grid()
    board.run_game()

if __name__ == '__main__':
    main()

    