# Adversarial Infexion

Project Part B for COMP30024_2023_SM1 Artifical Intelligence. \
Play Infexion here: <https://comp30024.pages.gitlab.unimelb.edu.au/2023s1/infexion-playground/> \
Contributors: Natasha Chiorsac, Vincent Luu

"You will design and implement an agent program to play the game of Infexion. That is, given information about the evolving state of the game, your program will decide on an action to take on each of its turns."

## Running the Project

- Download the repository
- Run `python -m referee x y`, where `x` and `y` are game playing agents.
- Game playing agent choices:
  - `agent`: Minimax agent with improvements described in report
  - `Experimentation/Agent_Greedy`: A greedy agent based on a utility function
  - `Experimentation/Agent_MCTS`: Agent trained with Monte Carlo Tree Search
  - `Experimentation/Agent_Random`: A random agent

