# Planning & Research

## Game playing agents

### Monte Carlo Tree Search

- No heuristic function required
- Good for games with large branching factor as is the case in Infexion
- Need to perform many playouts, will take a long time to compute average utility of all the possible states - could use a modified version with an evaluation function to speed things up?
- According to studies there seems to be an issue of MCTS not detecting “shallow traps” - outcomes of the game in which the opponent can win within only a few moves
- Current implementation: simulates x amount of playouts distrubuted across the children of the current state. Picks the best move based on the given formula.
- As red, this MCTS always loses against Agent_Utility. As blue, this MCTS always draws against Agent_Utility.

### Minimax with Alpha-Beta pruning

- Slow, since branching factor of Infexion is fairly large (between 6 and 53) - though speed could hopefully be improved with a good evaluation function & further pruning in addition to alpha-beta
- Able to detect shallow traps

### Utility Function
- Utility value based on total power only almost always beats Utility value based on number of cells only
- Probably something like this would be best: A*(powerEnemies/powerAllies) + B*(numEnemies/numAllies), A>B
- Need to do lots of tests to decide A and B
- Maybe also consider "occupied lines" like the heuristic in Part A

## Links that may be useful for further research

- Comparison of MCTS and Minimax: <https://www.diva-portal.org/smash/get/diva2:1597267/FULLTEXT01.pdf>
- Another MCTS & Minimax comparison: <https://inria.hal.science/hal-01466213/document>
- MCTS & Minimax hybrids: <https://dke.maastrichtuniversity.nl/m.winands/documents/mctshybrids.pdf>
- Improving Minimax: <https://levelup.gitconnected.com/improving-minimax-performance-fc82bc337dfd>
- Compilation of many different implementations of MCTS, may have useful ideas regarding enhancements to MCTS: <https://arxiv.org/abs/2103.04931>
- Analysis of Minimax and a reinforcement learning agent: <https://www.tandfonline.com/doi/full/10.1080/08839514.2021.1934265>

## Resources used

- <https://ai-boson.github.io/mcts/>
