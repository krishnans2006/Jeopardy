import pygame

from textwrap import wrap


class Contestant:
    def __init__(self, name, pos, total, font, no_answer=False, start_points=0):
        self.name = name
        self.no_answer = no_answer
        self.font = font
        self.name_text = self.font.render(self.name, 1, (200, 200, 0))
        self.width = 1200 // total + 1
        self.x = self.width * pos
        self.y = 690
        self.height = 100
        self.start_points = start_points
        self.current_points = self.start_points
        self.points_text = self.font.render(str(self.current_points), 1, (220, 220, 220))
        self.done = False
        if self.no_answer:
            self.name_text = self.font.render("No", 1, (200, 200, 0))
            self.points_text = self.font.render("Answer", 1, (200, 200, 0))
            self.rect = pygame.Rect(self.x + 10, self.y - 5, self.width - 20, self.height + 10)
        else:
            self.rect = pygame.Rect(self.x + 10, self.y, self.width - 20, self.height)
            self.green_rect = pygame.Rect(self.x + 10, self.y - 5, self.width - 20, self.height // 2 + 5)
            self.red_rect = pygame.Rect(self.x + 10, self.y + 50, self.width - 20, self.height // 2 + 5)

    def add_points(self, points):
        self.current_points += points
        self.points_text = self.font.render(str(self.current_points), 1, (220, 220, 220))

    def remove_points(self, points):
        self.current_points -= points
        self.points_text = self.font.render(str(self.current_points), 1, (220, 220, 220))

    def draw(self, win):
        if not self.no_answer:
            pygame.draw.rect(win, (24, 165, 24), self.green_rect)
            pygame.draw.rect(win, (165, 24, 24), self.red_rect)
        pygame.draw.rect(win, (24, 24, 165), self.rect)
        win.blit(self.name_text, (self.x + self.rect.width // 2 - self.name_text.get_width() // 2 + 10, self.y - 5))
        win.blit(self.points_text, (self.x + self.rect.width // 2 - self.points_text.get_width() // 2 + 10, self.y - 5 + self.name_text.get_height() - 10))

    def __repr__(self):
        return f"Player {self.name} with {self.current_points} points."


class Box:
    def __init__(self, x, y, width, height, name, qnFont, priceFont):
        self.x = x * 200 + 10
        self.y = y * 98 + 210
        if y == 0:
            self.y -= 10
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.is_header = y == 0
        self.font = qnFont if self.is_header else priceFont
        self.over = False
        if self.is_header:
            self.category = wrap(name, 12)
            self.points = self.qn = self.ans = None
        else:
            self.category = None
            self.points = int(name.split(": ")[0])
            qn_split = name.split(": ")[1].split(" - ")[0]
            self.qn = wrap(qn_split, len(qn_split) // 3)
            ans_split = name.split(": ")[1].split(" - ")[1]
            self.ans = wrap(ans_split, 30)

    def click(self):
        if not self.is_header:
            self.over = True
            cover_texts = [self.font.render(line, 1, (230, 230, 230)) for line in self.qn]
            max_width = 0
            for cover_text in cover_texts:
                if cover_text.get_width() > max_width:
                    max_width = cover_text.get_width()
            self.all_qn = pygame.Surface((max_width, len(cover_texts) * 46 + 10), pygame.SRCALPHA)
            for x, cover_text in enumerate(cover_texts):
                self.all_qn.blit(cover_text,
                               (self.all_qn.get_width() // 2 - cover_text.get_width() // 2, x * 46))
            cover_texts = [self.font.render(line, 1, (230, 230, 230)) for line in self.ans]
            max_width = 0
            for cover_text in cover_texts:
                if cover_text.get_width() > max_width:
                    max_width = cover_text.get_width()
            self.all_ans = pygame.Surface((max_width, len(cover_texts) * 46 + 10), pygame.SRCALPHA)
            for x, cover_text in enumerate(cover_texts):
                self.all_ans.blit(cover_text,
                               (self.all_ans.get_width() // 2 - cover_text.get_width() // 2, x * 46))
            return self.points, self.all_qn, self.all_ans, self.ans
        else:
            return None

    def draw(self, win):
        pygame.draw.rect(win, (24, 24, 165), self.rect)
        if not self.over:
            if self.is_header:
                cover_texts = [self.font.render(line, 1, (230, 230, 230)) for line in self.category]
                max_width = 0
                for cover_text in cover_texts:
                    if cover_text.get_width() > max_width:
                        max_width = cover_text.get_width()
                all_words = pygame.Surface((max_width, len(cover_texts) * 25), pygame.SRCALPHA)
                for x, cover_text in enumerate(cover_texts):
                    all_words.blit(cover_text,
                                   (all_words.get_width() // 2 - cover_text.get_width() // 2, x * 25))
            else:
                all_words = self.font.render(str(self.points), 1, (200, 200, 0))
            win.blit(all_words, (self.x + self.width // 2 - all_words.get_width() // 2, self.y + self.height // 2 - all_words.get_height() // 2))
