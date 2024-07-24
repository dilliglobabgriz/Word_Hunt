from game_files.game_board import LetterGrid

def test_is_english1():
    board = LetterGrid(4)
    word = 'pot'
    assert board.is_english_word(word) == True

def test_is_english2():
    board = LetterGrid(4)
    word = 'RAT'
    assert board.is_english_word(word) == True

def test_is_english_nonletter():
    board = LetterGrid(4)
    word = '$star!'
    assert board.is_english_word(word) == False

def test_is_english_plural():
    # some plural and conjugated words are not in my english dict
    board = LetterGrid(4)
    word = 'semesters'
    assert board.is_english_word(word) == False