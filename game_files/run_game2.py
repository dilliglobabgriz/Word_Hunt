import pygame
from game_files.game_board import LetterGrid
import nltk
from nltk.corpus import words

nltk.download('words')

class Game:
    def __init__(self, time_secs: int):
        self.time_secs = time_secs

    def play(self):



        pygame.init()

        # Constants
        SCREEN_WIDTH = 800
        SCREEN_HEIGHT = 600
        FONT_SIZE = 30
        TITLE_FONT_SIZE = 50
        TIMER_FONT_SIZE = 40
        GAME_OVER_FONT_SIZE = 100
        GAME_TIME_SEC = self.time_secs

        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Letter Grid")

        # Set up the board area and fonts
        board = pygame.Rect((273, 173, 275, 275))
        font = pygame.font.Font(None, FONT_SIZE)
        title_font = pygame.font.Font(None, TITLE_FONT_SIZE)
        timer_font = pygame.font.Font(None, TIMER_FONT_SIZE)
        game_over_font = pygame.font.Font(None, GAME_OVER_FONT_SIZE)

        # Create and fill the letter grid
        b1 = LetterGrid(6)
        b1.fill_grid_weighted()
        board_array = b1.grid

        # Create game state variables
        guesses = set()
        score = 0

        # Clock and timer setup
        clock = pygame.time.Clock()
        start_ticks = pygame.time.get_ticks()

        # Text input variables
        input_box = pygame.Rect(100, 50, 140, 32)
        color_inactive = (150, 150, 150)
        color_active = pygame.Color(80, 80, 80)
        color = color_inactive
        active = False
        text = ''

        # Game state
        done = False
        timeout = False

        # Title display
        title_box = pygame.Rect(297, 120, 350, 50)
        title_text = 'WORD HUNT'

        # Message after word inputted
        message_box = pygame.Rect(230, 500, 400, 35)
        message_text = 'Use adjacent letters to input words'

        # Score
        score_box = pygame.Rect(700, 250, 50, 35)
        score_text = str(score)

        # Function to display the timer
        def display_timer(seconds_left):
            minutes = seconds_left // 60
            seconds = seconds_left % 60
            timer_text = f"{minutes:02}:{seconds:02}"
            text = timer_font.render(timer_text, True, (255, 255, 255))
            screen.blit(text, (700, 560))
            pygame.display.flip()

        def draw_grid(xcoord, ycoord, rows, side_length, gap_length):
            x_offset = 0
            y_offset = 0
            for i in range(rows):
                for j in range(rows):
                    x_offset = (j * side_length) + ((j + 1) * gap_length)
                    y_offset = (i * side_length) + ((i + 1) * gap_length)

                    grid_square = pygame.Rect((xcoord + x_offset, ycoord + y_offset, side_length, side_length))
                    pygame.draw.rect(screen, (255, 165, 0), grid_square)

                    # Render the letter in the center of the square
                    letter = board_array[i][j]
                    text_surface = font.render(letter, True, (0, 0, 0))
                    text_rect = text_surface.get_rect(center=grid_square.center)
                    screen.blit(text_surface, text_rect)

        # Function to handle logic after a word has been entered
        # Return a message to give to the player based on what action is taken
        # Return a list with the string as the 0th arg and the score of the word as arg 1
        def check_word(word: str):
            cur_word = word.upper()
            if cur_word in guesses:
                return [f'{cur_word} has already been guessed, please try again', 0]
            guesses.add(cur_word)
            if len(cur_word) < 3:
                return ['Words must be at least 3 letters', 0]
            if not b1.valid_word(cur_word):
                return [f'{cur_word} cannot be made, please try again', 0]
            if not b1.is_english_word(cur_word):
                return [f'{cur_word} is not in the english language', 0]

            # If not of the bad cases are hit word must be valid
            cur_score = b1.score_word(cur_word)
            return [f'{cur_word} scored {cur_score} pt(s)', cur_score]


        while not done and not timeout:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # If the user clicked on the input_box rect.
                    if input_box.collidepoint(event.pos):
                        # Toggle the active variable.
                        active = not active
                    else:
                        active = False
                    # Change the current color of the input box.
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            message_text, cur_score = check_word(text)
                            score += cur_score
                            score_text = str(score)
                            text = ''
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

            screen.fill((100, 100, 100))  # Fill the screen with grey

            pygame.draw.rect(screen, (255, 255, 255), board)
            draw_grid(273, 173, 6, 40, 5)

            # Title text
            title_surface = title_font.render(title_text, True, pygame.Color('navy'))
            screen.blit(title_surface, (title_box.x + 5, title_box.y + 5))

            # Score text
            score_surface = font.render(f"Score: {score_text}", True, (255, 255, 255))
            screen.blit(score_surface, (score_box.x, score_box.y))

            # Add the message text box below the game board
            message_text_surface = font.render(message_text, True, (255, 255, 255))
            # Adjust size of text box
            message_width = max(200, message_text_surface.get_width() + 10)
            message_box.w = message_width
            # Blit the message box background
            pygame.draw.rect(screen, pygame.Color('navy'), message_box)
            # Blit message text
            screen.blit(message_text_surface, (message_box.x + 5, message_box.y + 5))
            #pygame.draw.rect(screen, pygame.Color('white'), message_box, 1)

            # Render the current text.
            txt_surface = font.render(text, True, (0, 0, 0))  # Render text in black
            # Resize the box if the text is too long.
            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width
            # Blit the text box background.
            pygame.draw.rect(screen, pygame.Color('lightgrey'), input_box)
            # Blit the text.
            screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            # Blit the input_box rect.
            pygame.draw.rect(screen, color, input_box, 2)

            # Update the timer
            seconds_left = GAME_TIME_SEC - (pygame.time.get_ticks() - start_ticks) // 1000

            # Check if timer has hit zero
            if seconds_left <= 0:
                seconds_left = 0
                timeout = True

            display_timer(seconds_left)

            clock.tick(30)  # Maxing tick rate

            pygame.display.flip()

        # If the user times out but doesnt exit out, display their score
        while not done and timeout:
            # Check for users clicking out
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

            screen.fill(pygame.Color('fuchsia'))
            game_over_text = f'SCORE: {score}'
            display_game_over_text = game_over_font.render(game_over_text, True, (255, 255, 255))
            screen.blit(display_game_over_text, (200, 275))
            pygame.display.flip()


        pygame.quit()
