import numpy as np, random, time, gym

class GridWorld:
    def __init__(self, width, height, start_pos, goal_pos, obstacles=None, move_reward=-1, goal_reward=10, obstacle_reward=-10):
        self.width = width
        self.height = height
        self.start_pos = start_pos
        self.goal_pos = goal_pos
        self.obstacles = obstacles if obstacles else []
        self.state = start_pos
        self.move_reward = move_reward
        self.goal_reward = goal_reward
        self.obstacle_reward = obstacle_reward

    def reset(self):
        self.state = self.start_pos
        return self.state

    def step(self, action):
        # Define actions as tuples of (delta_x, delta_y)
        actions = {
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0),
        }
        delta = actions[action]
        next_state = (self.state[0] + delta[0], self.state[1] + delta[1])

        # Check for boundaries and obstacles
        if (0 <= next_state[0] < self.width) and (0 <= next_state[1] < self.height):
            if next_state in self.obstacles:
                reward = self.obstacle_reward
            elif next_state == self.goal_pos:
                self.state = next_state
                return self.state, self.goal_reward, True
            else:
                self.state = next_state
                reward = self.move_reward
        else:
            reward = self.move_reward

        return self.state, reward, self.state == self.goal_pos

    def render(self):
        grid = np.zeros((self.height, self.width))
        for obstacle in self.obstacles:
            grid[obstacle[1], obstacle[0]] = -1  # Represent obstacles
        grid[self.goal_pos[1], self.goal_pos[0]] = 2  # Represent goal
        grid[self.state[1], self.state[0]] = 1  # Represent agent
        print(grid)

def q_learning(env, episodes, alpha = 0.1, gamma = 0.99, epsilon = 0.1):
    q_values = np.zeros((env.height, env.width, 4))  # Assuming 4 actions: up, down, left, right
    actions = ['up', 'down', 'left', 'right']

    for episode in range(episodes):
        state = env.reset()
        done = False

        while not done:
            if random.uniform(0, 1) < epsilon:  # Explore
                action = random.choice(actions)
            else:  # Exploit
                action_index = np.argmax(q_values[state[1], state[0]])
                action = actions[action_index]

            next_state, reward, done = env.step(action)
            next_max = np.max(q_values[next_state[1], next_state[0]])

            # Q-learning update rule
            current_q = q_values[state[1], state[0], actions.index(action)]
            q_values[state[1], state[0], actions.index(action)] = current_q + alpha * (reward + gamma * next_max - current_q)

            state = next_state

    return q_values

def evaluate_policy(env, q_values, max_steps=100):
    state = env.reset()
    env.render()
    for step in range(max_steps):
        action_index = np.argmax(q_values[state[1], state[0]])
        actions = ['up', 'down', 'left', 'right']
        action = actions[action_index]
        state, reward, done = env.step(action)
        env.render()
        if done:
            if reward == env.goal_reward:
                print("Reached the goal!")
            else:
                print("Hit an obstacle or penalty.")
            break

def main():
    env = GridWorld(5, 5, (0, 0), (4, 4), [(4, 0), (3, 1), (2, 3), (1, 2), (1, 1)])
    q_values = q_learning(env, 1000)
    evaluate_policy(env, q_values)
    

if __name__ == '__main__':
    main()