# pylint: disable=undefined-variable
# pylint: disable=unused-wildcard-import
# ruff: noqa: F405
# mypy: disable-error-code="name-defined"

"""Main script/entry point for wordlemini."""

import random
import sys
from itertools import chain
from typing import Iterable, List, Union

from textual.app import App
from textual.binding import Binding
from textual.containers import Grid, Horizontal, Vertical
from textual.widget import Widget
from textual.widgets import Button, Input, Label, Rule

from . import ASSETS, CORPUS
from ._config import Config
from ._keyboards import *  # noqa
from ._util import translate

translate(Config.get("settings", "lang"))

GRID_WIDTH = 5
GRID_HEIGHT = 6


class Wordle(App):
    """Textual app to play a wordle game."""

    CSS_PATH = ASSETS / "styles.tcss"
    BINDINGS = [
        Binding("ctrl+n", "new_game_keybind", "Start new game"),
    ]
    LANG = Config.get("settings", "lang")

    words: List[str] = []

    @classmethod
    def apply_words(cls) -> None:
        """Gather all the words in a particular `<lang-code>.txt` file and append
        them to `Wordle.words`.
        """
        with open(CORPUS / f"{Wordle.LANG}.txt", encoding="utf-8") as f:
            for word in f:
                formatted_word = word[:-1]
                if len(formatted_word) == GRID_WIDTH:
                    cls.words.append(formatted_word)

    @property
    def main_widgets(self) -> List[Widget]:
        """Return a list of all the main widgets."""
        return [
            *list(chain(*self.grid)),
            *list(chain(*self.keyboard)),
            self.input,
            self.submit,
            self.delete,
            self.new,
        ]

    def __init__(self) -> None:
        """Initialise widgets and pick a random word to begin the first game."""
        super().__init__()
        self.dark = Config.get("settings", "dark")
        self.grid = [
            [Label("") for i in range(GRID_WIDTH)] for j in range(GRID_HEIGHT)
        ]
        if not self.dark:
            for label in list(chain(*self.grid)):
                label.styles.border = ("round", "black")
        self.keyboard = [
            [Button(key, name="key") for key in row]
            for row in globals().get(f"KEYBOARD_{Wordle.LANG.upper()}")
            or KEYBOARD_EN
        ]
        self.input = Input(
            placeholder=_("Enter your guess"),
            type="text",
            restrict=r"[a-zA-Z]{0,5}",
        )
        self.submit = Button(f"{_("Guess")} [↵]", name="submit")
        self.delete = Button(f"{_("Delete")} [⌫]", name="delete")
        self.new = Button(f"{_("New")} [^n]", name="new")
        self.quit = Button(f"{_("Quit")} [^c]", name="quit", variant="error")

        Wordle.apply_words()
        self.word = random.choice(Wordle.words).casefold()
        self.guess = ""
        self.row = 0

        self.nonexisting_chars: set[str] = set()
        self.wrong_pos_chars: set[str] = set()
        self.correct_pos_chars: set[str] = set()

    def compose(self) -> Iterable[Horizontal]:
        """Provide Textual with all the widgets for the DOM."""
        yield Horizontal(
            Grid(*list(chain(*self.grid)), classes="word-grid"),
            Rule(orientation="vertical"),
            Grid(
                Vertical(
                    *[
                        Horizontal(Grid(*row, classes="keyboard-row"))
                        for row in self.keyboard
                    ],
                    id="keyboard",
                ),
                Vertical(
                    self.input,
                    Horizontal(
                        self.submit,
                        Rule(),
                        self.delete,
                        Rule(),
                        self.new,
                        Rule(),
                        self.quit,
                        id="button-row",
                    ),
                ),
                id="right-side",
            ),
        )
        self.input.focus()

    def set_disabled_state_of_all_widgets(self, state: bool) -> None:
        """Enable or disable all main widgets."""
        for widget in self.main_widgets:
            widget.disabled = state

    def action_new_game_keybind(self):
        self.new.action_press()

    def new_game(self) -> None:
        """Begin a new game - which involves picking a new word and resetting
        all colour-related hints in the keyboard as well as user input in the
        grid.
        """
        txt = _("Started new game!")
        if self.guess != self.word:
            txt += f" ({_("The word was")} {self.word.upper()})"
        self.notify(txt, timeout=2.0)
        for label in [*list(chain(*self.grid))]:
            label.update("")
        for row in self.keyboard:
            for button in row:
                if button.name == "key":
                    button.label = str(button.label)
                    button.styles.opacity = "100%"

        self.input.value = ""
        self.nonexisting_chars = set()
        self.wrong_pos_chars = set()
        self.correct_pos_chars = set()
        self.word = random.choice(Wordle.words)
        self.row = 0
        self.set_disabled_state_of_all_widgets(False)
        self.input.focus()

    def update_grid(self, guess: str) -> None:
        """Update the current row of the grid. This is a more advanced algorithm
        compared to `update_char_statuses` and ensures the proper detection of
        misplaced letters"""
        word_letter_count = {
            char: self.word.count(char) for char in set(self.word)
        }

        # first pass - check for correct positions and reduce counts
        for i, char in enumerate(guess):
            label = self.grid[self.row][i]
            if char == self.word[i]:
                label.update(f"[green]{char.upper()}[/green]")
                self.correct_pos_chars.add(char.casefold())
                word_letter_count[char] -= 1
            else:
                label.update(
                    f"{char.upper()}"
                )  # change if needed in next pass

        # second pass - check for wrong positions using remaining counts
        for i, char in enumerate(guess):
            label = self.grid[self.row][i]
            if (
                char != self.word[i]
                and char in self.word
                and word_letter_count[char] > 0
            ):
                label.update(f"[yellow]{char.upper()}[/yellow]")
                self.wrong_pos_chars.add(char.casefold())
                word_letter_count[char] -= 1
            elif char != self.word[i] and char not in self.word:
                self.nonexisting_chars.add(char.casefold())

        self.row += 1

    def update_keyboard(self) -> None:
        """Update the virtual keyboard."""
        for row in self.keyboard:
            for button in row:
                label = str(button.label).casefold()
                if label in self.correct_pos_chars:
                    button.label = f"[green]{label.upper()}[/green]"
                elif label in self.wrong_pos_chars:
                    button.label = f"[yellow]{label.upper()}[/yellow]"
                elif label in self.nonexisting_chars:
                    button.styles.opacity = "20%"

    def update_char_statuses(self, guess: str) -> None:
        """Update the status of the characters in `guess`."""
        for i, char in enumerate(guess):
            if char == self.word[i]:
                self.correct_pos_chars.add(char)
            elif char in self.word:
                self.wrong_pos_chars.add(char)
            else:
                self.nonexisting_chars.add(char)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle a button being pressed."""
        name = event.button.name
        if name == "key":
            return self.action_submit_char(event)
        if name == "delete":
            return self.action_delete_char(event)
        if name == "submit":
            return self.on_input_submitted()
        if name == "new":
            return self.new_game()
        if name == "quit":
            sys.exit()
        return None

    def on_input_submitted(
        self, event: Union[Input.Submitted, None] = None
    ) -> None:
        """Handle a user submitting their word."""
        guess = str(self.input.value).casefold()
        if len(guess) != GRID_WIDTH:
            return self.notify(
                _("Guess must be 5 characters long."),
                severity="error",
                timeout=2.0,
            )
        if guess not in Wordle.words:
            return self.notify(
                _("Guess is not in word list."), severity="error", timeout=2.0
            )
        self.guess = guess
        self.update_char_statuses(guess)
        self.update_grid(guess)
        self.update_keyboard()
        self.input.value = ""
        self.input.focus()

        done = False
        if guess == self.word:
            self.notify(
                f"{_("You guessed the word in")} {self.row} {_("attempts")}!",
                timeout=3.5,
            )
            done = True
        elif self.row > GRID_WIDTH:
            self.notify(
                f"{_("The word was")} {self.word.upper()}. {_("Better luck next time")}!",
                timeout=3.5,
            )
            done = True
        if done:
            self.guess = self.word
            self.set_disabled_state_of_all_widgets(True)
            self.new.disabled = False

        return None

    def action_submit_char(self, event: Button.Pressed) -> None:
        """Enter a character from the virtual keyboard into `self.input`."""
        self.input.focus()
        if len(self.input.value) >= GRID_WIDTH:
            return
        self.input.value = (
            self.input.value + str(event.button.label).casefold()
        )
        self.input.action_cursor_right_word()

    def action_delete_char(self, event: Button.Pressed) -> None:
        """Delete a character from `self.input`."""
        self.input.focus()
        if len(self.input.value) <= 0:
            return
        self.input.value = self.input.value[:-1]
        self.input.action_cursor_left()


def initialise() -> None:
    """Initialise the Wordle game."""
    Wordle().run()


if __name__ == "__main__":
    initialise()
