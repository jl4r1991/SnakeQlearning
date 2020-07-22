import random
import json

import dataclasses

@dataclasses.dataclass
class GameState:
    distance: tuple
    position: tuple
    surroundings: str
    food: tuple


class Learner(object):
    def __init__(self, display_width, display_height, block_size):
        # Game parameters
        self.display_width = display_width
        self.display_height = display_height
        self.block_size = block_size

        # Learning parameters
        self.epsilon = 0.1
        self.lr = 0.7
        self.discount = .5

        # State/Action history
        self.qvalues = self.LoadQvalues()
        self.history = []

        # Action space
        self.actions = {
            0:'left',
            1:'right',
            2:'up',
            3:'down'
        }

    def Reset(self):
        self.history = []

    def LoadQvalues(self, path="qvalues.json"):
        with open(path, "r") as f:
            qvalues = json.load(f)
        return qvalues

    def SaveQvalues(self, path="qvalues.json"):
        with open(path, "w") as f:
            json.dump(self.qvalues, f)
            
    def act(self, snake, food):
        state = self._GetState(snake, food)

        # Epsilon greedy
        rand = random.uniform(0,1)
        if rand < self.epsilon:
            action_key = random.choices(list(self.actions.keys()))[0]
        else:
            state_scores = self.qvalues[self._GetStateStr(state)]
            action_key = state_scores.index(max(state_scores))
        action_val = self.actions[action_key]
        
        # Remember the actions it took at each state
        self.history.append({
            'state': state,
            'action': action_key
            })
        return action_val
    
    def UpdateQValues(self, reason):
        history = self.history[::-1]
        for i, h in enumerate(history[:-1]):
            if reason: # Snake Died -> Negative reward
                sN = history[0]['state']
                aN = history[0]['action']
                state_str = self._GetStateStr(sN)
                reward = -1
                self.qvalues[state_str][aN] = (1-self.lr) * self.qvalues[state_str][aN] + self.lr * reward # Bellman equation - there is no future state since game is over
                reason = None
            else:
                s1 = h['state'] # current state
                s0 = history[i+1]['state'] # previous state
                a0 = history[i+1]['action'] # action taken at previous state
                
                x1 = s0.distance[0] # x distance at current state
                y1 = s0.distance[1] # y distance at current state
    
                x2 = s1.distance[0] # x distance at previous state
                y2 = s1.distance[1] # y distance at previous state
                
                if s0.food != s1.food: # Snake ate a food, positive reward
                    reward = 1
                elif (abs(x1) > abs(x2) or abs(y1) > abs(y2)): # Snake is closer to the food, positive reward
                    reward = 1
                else:
                    reward = -1 # Snake is further from the food, negative reward
                    
                state_str = self._GetStateStr(s0)
                new_state_str = self._GetStateStr(s1)
                self.qvalues[state_str][a0] = (1-self.lr) * (self.qvalues[state_str][a0]) + self.lr * (reward + self.discount*max(self.qvalues[new_state_str])) # Bellman equation


    def _GetState(self, snake, food):
        snake_head = snake[-1]
        dist_x = food[0] - snake_head[0]
        dist_y = food[1] - snake_head[1]

        if dist_x > 0:
            pos_x = '1' # Food is to the right of the snake
        elif dist_x < 0:
            pos_x = '0' # Food is to the left of the snake
        else:
            pos_x = 'NA' # Food and snake are on the same X file

        if dist_y > 0:
            pos_y = '3' # Food is below snake
        elif dist_y < 0:
            pos_y = '2' # Food is above snake
        else:
            pos_y = 'NA' # Food and snake are on the same Y file

        sqs = [
            (snake_head[0]-self.block_size, snake_head[1]),   
            (snake_head[0]+self.block_size, snake_head[1]),         
            (snake_head[0],                  snake_head[1]-self.block_size),
            (snake_head[0],                  snake_head[1]+self.block_size),
        ]
        
        surrounding_list = []
        for sq in sqs:
            if sq[0] < 0 or sq[1] < 0: # off screen left or top
                surrounding_list.append('1')
            elif sq[0] >= self.display_width or sq[1] >= self.display_height: # off screen right or bottom
                surrounding_list.append('1')
            elif sq in snake[:-1]: # part of tail
                surrounding_list.append('1')
            else:
                surrounding_list.append('0')
        surroundings = ''.join(surrounding_list)

        return GameState((dist_x, dist_y), (pos_x, pos_y), surroundings, food)

    def _GetStateStr(self, state):
        return str((state.position[0],state.position[1],state.surroundings))
