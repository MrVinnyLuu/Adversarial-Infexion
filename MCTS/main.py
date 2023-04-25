
from MCTS.MCTS import *

def main():

    root = MCTSNode(state = GameState())

    selectedNode = root.bestAction()
    print(selectedNode.state.reds)
    print(selectedNode.state.blues)

    print("*******************")
    selectedNode = selectedNode.bestAction()
    print(selectedNode.state.reds)
    print(selectedNode.state.blues)

    print("*******************")
    selectedNode = selectedNode.bestAction()
    print(selectedNode.state.reds)
    print(selectedNode.state.blues)

    print("*******************")
    selectedNode = selectedNode.bestAction()
    print(selectedNode.state.reds)
    print(selectedNode.state.blues)

    print("*******************")
    selectedNode = selectedNode.bestAction()
    print(selectedNode.state.reds)
    print(selectedNode.state.blues)

    print("*******************")
    selectedNode = selectedNode.bestAction()
    print(selectedNode.state.reds)
    print(selectedNode.state.blues)
    
    return