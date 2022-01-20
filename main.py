import pygame

from classes import Box, Contestant


def setup(W, H):
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()

    win = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Jeopardy Control")

    clock = pygame.time.Clock()

    qnFont = pygame.font.Font("QuestionFont.ttf", 30)
    priceFont = pygame.font.Font("PriceFont.ttf", 50)
    music = pygame.mixer.music.load("jeopardy_music.mp3")

    return win, clock, qnFont, priceFont, music


win, clock, qnFont, priceFont, music = setup(1200, 800)
pygame.mixer.music.play(-1)
jeopardy_board = [
    ["Talented People", "Sports", "DC Superheroes", "Greek Mythology", "Units",
     "Fun Facts"],
    ["100: How many kids did the moonhack coding club set to code each day? - 28000!",
     "100: Who is the ONLY basketball player that has NEVER scored under 20 points in a game? - Michael Jordan",
     "100: When did Batman vs Superman come out? - 2015",
     "100: What is Ares the god of? - War",
     "100: What is the unit of weight in the metric system? - Kilogram",
     "100: Does the moon have moonquakes? - Yes!"],
    ["200: What was the time for the LONGEST math problem that was unsolved? - 365 years!",
     "200: This retired Basketball player goes by the title 'Magic' - Magic Johnson",
     "200: How many robins are there? - 5",
     "200: What is Herra the goddess of? - Marriage",
     "200: How many cups in a gallon? - 16", "200: What other animals besides humans blush? - None!"],
    ["300: Who is the third father of Quantum Physics? - Albert Einstein",
     "300: Who won 2019 MVP of NBA? - Giannis",
     "300: What is the first batgirl's identity? - Barbara Gordon",
     "300: What is Athena the goddess of? - Wisdom",
     "300: What is the unit for force? - A Newton",
     "300: What is the ONLY fruit that cannot be made into cider? - Pears"],
    [
        "400: Who invented Braille? - Louis Braile",
        "400: Who is the number 1 point guard for the 76ers? - Ben Simmons",
        "400: Is there a thing called a blue lantern? - Yes!",
        "400: What is Hecate the goddess of? - Magic",
        "400: What is the unit for work? - Joule",
        "400: What are goosebumps believed to do? - Ward off enemies"],
    [
        "500: Who invented Morse code? - Samuel",
        "500: Who's son is better than HIM in basketball currently? - Lebron James",
        "500: What is the ONLY way superman can be hurt? - Kryptonite",
        "500: What is Prometheus the god of? - Prometheus is a titan, not a god!",
        "500: what is the unit for pressure? - Pascal",
        "500: What fruit softens meat? - Pineapples!"],
]
double_jeopardy_board = jeopardy_board  # Create a new board - make sure to update the money for the questions!

final_jeopardy = [["Coding"], ["0: What are the two things in coding you should NEVER do? - Copy code and memorize it without understanding"]]  # To be implemented

jeopardy = [
    [Box(i, j, 180, 90, jeopardy_board[j][i], qnFont, priceFont) for i in range(6)] for j in range(6)
]

logo = pygame.transform.scale(pygame.image.load("jeopardy_logo.jpg"), (1200, 200))

current_state = "board"
time_to_board = 0
qn = None
pts = None
current_board = "single"
players = input("Enter Player's Names Split By Commas: ").split(",")
contestants = [Contestant(name, x, len(players) + 1, priceFont) for x, name in enumerate(players)]
no_answer = Contestant("No Answer", len(players), len(players) + 1, priceFont, True)


def switch_to_qn(points, question, answer):
    global current_state, qn, pts
    current_state = "qn"
    qn = question
    pts = points
    print(f"Answer: {' '.join(answer)}")


def handle_click(jeopardy, contestants):
    global current_state
    mousepos = pygame.mouse.get_pos()
    if current_state == "qn" and no_answer.rect.collidepoint(mousepos):
        current_state = "board"
        for my_contestant in contestants:
            my_contestant.done = False
        return None
    if current_state == "qn":
        for contestant in contestants:
            if not contestant.done and contestant.red_rect.collidepoint(mousepos):
                contestant.remove_points(pts)
                contestant.done = True
            if not contestant.done and contestant.green_rect.collidepoint(mousepos):
                contestant.add_points(pts)
                current_state = "board"
                for my_contestant in contestants:
                    my_contestant.done = False
        return None
    for box_list in jeopardy:
        for box in box_list:
            if not box.over and box.rect.collidepoint(mousepos):
                return box.click()
    return None


def check_completeness(jeopardy):
    for box_list in jeopardy:
        for box in box_list:
            if not box.is_header and not box.over:
                return False
    return True


def check_rowness(jeopardy):
    for i in range(6):
        all_over = True
        for j in range(1, 6):
            if not jeopardy[j][i].over:
                all_over = False
        if all_over:
            jeopardy[0][i].over = True


def check_overness(jeopardy_param):
    global jeopardy, current_board
    if check_completeness(jeopardy_param):
        if current_board == "single":
            jeopardy = [
                [Box(i, j, 180, 90, double_jeopardy_board[j][i], qnFont, priceFont) for i in range(6)] for j in range(6)
            ]
        else:
            current_board = "final"
    check_rowness(jeopardy)


def redraw_board(win, **kwargs):
    win.fill((20, 20, 20))
    win.blit(logo, (0, 0))
    for name, object in kwargs.items():
        if name == "jeopardy":
            for box_list in object:
                for box in box_list:
                    box.draw(win)
        elif name == "qn":
            continue
        else:
            object.draw()
    pygame.display.flip()


def redraw_qn(win, qn):
    win.fill((20, 20, 20))
    win.blit(logo, (0, 0))
    boundary_box = pygame.Rect(10, 210, 1180, 470)
    pygame.draw.rect(win, (24, 24, 165), boundary_box)
    for contestant in contestants:
        contestant.draw(win)
    no_answer.draw(win)
    win.blit(qn, (win.get_width() // 2 - qn.get_width() // 2, 210 + boundary_box.height // 2 - qn.get_height() // 2))
    pygame.display.flip()


def redraw(win, **kwargs):
    if current_state == "board":
        redraw_board(win, **kwargs)
    else:
        redraw_qn(win, kwargs["qn"])


def main():
    global current_state
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                result = handle_click(jeopardy, contestants)
                if result:
                    switch_to_qn(result[0], result[1], result[3])
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                current_state = "board"
        check_overness(jeopardy)
        redraw(win, jeopardy=jeopardy, qn=qn)
        clock.tick(30)


if __name__ == '__main__':
    main()
