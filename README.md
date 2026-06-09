# oTree @ Melbourne 2026

Example apps developed in my course on oTree held at The University of Melbourne in 2026. *Note*: This class deals exclusively with oTree 5.11.5.

The class will be held via Zoom on June 1–4 (3 PM AET), and June 10 (10 AM AET).

This repository is directly runnable as an oTree project. The app `slides` contains slides with important class information; the remaining apps were developed in the following order: `survey`, `donation`, `dictator_game`, `ultimatum_game`, `pd`, `pd_1round`, `dropout`.

## Useful links

- [VS Code](https://code.visualstudio.com/download)
- [oTree project template](https://github.com/mrpg/otree-uv)
- [Installing `uv`](https://docs.astral.sh/uv/getting-started/installation/)

- Chapters 2, 3, 4, 5 of the [official Python tutorial](https://docs.python.org/3/tutorial/)
- [HTML](https://www.youtube.com/watch?v=bWPMSSsVdPk)
- [JavaScript](https://www.youtube.com/watch?v=xwKbtUP87Dk)
- [CSS](https://www.youtube.com/watch?v=yfoY53QXEnI)

### Further resources for learning Python

- [Python](https://www.youtube.com/watch?v=BVfCWuca9nw)
- [Python](https://www.youtube.com/watch?v=ZDa-Z5JzLYM)

### Miscellaneous

- [fish](https://fishshell.com)
- [oTree documentation](https://otree.readthedocs.io/en/latest/index.html)
- [What is the meaning of @staticmethod?](https://www.youtube.com/watch?v=rq8cL2XMM5M)
- [Computerphile on floating point numbers](https://www.youtube.com/watch?v=PZRI1IfStY0)

## Schedule

### Monday (June 1)

1. Getting started with oTree and uv
1. Creating a modern oTree project
1. Using oTree’s command line interface
1. Setting up an editor
1. Developing and running a simple app
1. Basic fields
1. **BREAKOUT**: Build a "Fun Facts Quiz" — a single-page app with 3 creative trivia questions using different field types
1. **PROJECT**: Survey
1. Using [black](https://github.com/psf/black)
1. Static files

### Tuesday (June 2)

1. Models
1. Subsessions, players and participants
1. Treatments, `creating_session`
1. More on fields
1. `choices`
1. **PROJECT**: Framed donation experiment
1. Currency, points, currency amounts
1. Constants
1. `vars_for_template` is banned, use `@property`
1. App sequences
1. **BREAKOUT**: Build a "Product Rating" app — a treatment (set in `creating_session`) changes the product shown, and players rate it 1–5

### Wednesday (June 3)

1. Basic grouping
1. Roles
1. WaitPages
1. **PROJECT**: Dictator game
1. **PROJECT**: Ultimatum game
1. Rounds
1. **PROJECT**: Repeated prisoner’s dilemma
1. ~~**BREAKOUT**: Build a "Rock-Paper-Scissors" game — simultaneous choices, a WaitPage, and a results page~~

### Thursday (June 4)

1. Paying for one or all rounds
1. `participant.vars`, shortcuts
1. Basic timeouts, `devserver` vs `prodserver`
1. Chats
1. Templating with `if` and `for`
1. **PROJECT**: Public goods game with chat and history table
1. Rooms, labels
1. Dropout handling

### Wednesday (June 10)

1. Raw widgets
1. Live Pages
1. `js_vars`
1. **PROJECT**: Surveillance game
1. `ExtraModel`, Custom exports
1. Sentinel fields
1. Session configs
1. Using coding agents (Claude Code and Codex) with oTree projects ([example prompt](#example-prompt))
1. [uproot](https://uproot.science/)

## Running this project

Install `uv` (if you haven't already):

- **macOS / Linux:**
  ```sh
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- **Windows:**
  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

## Getting started

1. **Get the template** — either clone the repository:
   ```sh
   git clone https://github.com/mrpg/otree-class
   cd otree-class
   ```
   or download and unzip it ([releases](https://github.com/mrpg/otree-uv/releases)), then open a terminal in the resulting folder.

2. **Install dependencies:**
   ```sh
   uv sync
   ```
   This creates a virtual environment and installs oTree and all dev tools automatically. No manual `pip install` or `venv` setup needed.

3. **Run the development server:**
   ```sh
   uv run otree devserver
   ```
   Then open [http://localhost:8000](http://localhost:8000) in your browser.

## Example prompt

```
Read through README.md, and */*.py, and */*.html.

Deeply inhale all best practices from these documents.

Then build a first-rate repeated public goods game with a history table.

Crucially, after each round, wait for all participants in the session, and randomly reshuffle groups.
```
