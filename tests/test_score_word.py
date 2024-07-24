from game_files.game_board import LetterGrid

def test_score_word1():
    grid = LetterGrid(3)
    assert grid.score_word('tester') == 3

def test_score_word2():
    grid = LetterGrid(3)
    assert grid.score_word('it') == 0

def test_score_word3():
    grid = LetterGrid(3)
    assert grid.score_word('operates') == 11

def test_score_word4():
    grid = LetterGrid(3)
    assert grid.score_word('interstellar') == 20


    




