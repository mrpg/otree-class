# oTree @ Cologne 2026

Example apps developed in my course on oTree held at the University of Cologne in 2026. *Note*: This class deals exclusively with oTree 5.11.4.

The class will be held via Zoom on February 23, 24, 25, and March 2, 3, 4 (8:30 AM CET).

This repository is directly runnable as an oTree project. The app `slides` contains slides with important class information; the remaining apps were developed in the following order: `survey`, `donation`, `dictator\_game`.

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

### Monday (Feb 23)

1. Getting started with oTree and uv
1. Creating a modern oTree project
1. Using oTree's command line interface
1. Setting up an editor
1. Developing and running a simple app
1. Basic fields
1. **PROJECT**: Survey
1. Using [black](https://github.com/psf/black)
1. Static files

### Tuesday (Feb 24)

1. Models
1. Treatments, `creating_session`
1. **PROJECT**: Framed donation experiment
1. Subsessions, players and participants
1. Currency, points, currency amounts
1. Constants
1. `vars_for_template` is banned, use `@property`
1. App sequences

### Wednesday (Feb 25)

1. More on fields
1. `choices`
1. Basic grouping
1. Roles
1. WaitPages
1. **PROJECT**: Dictator game
1. Rounds
1. **PROJECT**: Repeated prisoner’s dilemma

### Monday (Mar 2)

1. Paying for one or all rounds
1. Basic timeouts
1. **PROJECT**: Public goods game with feedback
1. Session settings
1. Widgets
1. Templating with `if` and `for`
1. `participant.vars`, shortcuts
1. Dropout handling, `devserver` vs `prodserver`, `app_after_this_page`
1. Chats

### Tuesday (Mar 3)

1. `js_vars`
1. Live Pages
1. **PROJECT**: Surveillance game
1. **PROJECT**: Sentinel fields
1. `ExtraModel`, Custom exports

### Wednesday (Mar 4)

1. Using coding agents with oTree projects
1. Alternatives to oTree, [uproot](https://uproot.science/)

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
