import random
import numpy as np
from collections import deque
import tensorflow as tf
from tensorflow.keras.layers import Conv2D, Concatenate, Flatten, Dense, Input, Dropout
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.optimizers import Adam

class DQNAgent:
    def __init__(self, state_size, action_size, gamma=0.99, epsilon=0.9, epsilon_min=0.01, epsilon_decay=0.995, learning_rate=0.00025, batch_size=64, memory_size=50000):
        self.state_size = state_size
        self.action_size = action_size
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.memory = deque(maxlen=memory_size)
        self.model = self._build_model()
        self.target_model = self._build_model()
        self.update_target_model()
        self.actions = ['w', 'a', 's', 'd']
        self.rewards_history = []

    def _build_model(self):
        inputs = Input(shape=(4, 4, 1))
        x = Conv2D(256, (2, 2), activation='relu')(inputs)
        x = Conv2D(512, (2, 2), activation='relu')(x)
        x = Flatten()(x)
        x = Dense(1024, activation='relu')(x)
        x = Dropout(0.5)(x)
        outputs = Dense(self.action_size, activation='linear')(x)
        model = Model(inputs, outputs)
        model.compile(loss='mse', optimizer=Adam(learning_rate=self.learning_rate))
        return model

    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            action = random.randrange(self.action_size)
            print(f"Random action: {action}")
            return action
        act_values = self.model.predict(state)
        action = np.argmax(act_values[0])
        print(f"Predicted action: {action}")
        return action

    def replay(self):
        if len(self.memory) < self.batch_size:
            return

        minibatch = random.sample(self.memory, self.batch_size)
        states = np.array([experience[0] for experience in minibatch]).reshape(self.batch_size, 4, 4, 1)
        actions = np.array([experience[1] for experience in minibatch])
        rewards = np.array([experience[2] for experience in minibatch])
        next_states = np.array([experience[3] for experience in minibatch]).reshape(self.batch_size, 4, 4, 1)
        dones = np.array([experience[4] for experience in minibatch])
        
        print("Predicting target values")
        target = self.model.predict(states)
        print("Predicting next state values")
        target_next = self.model.predict(next_states)
        print("Predicting target model values")
        target_val = self.target_model.predict(next_states)

        for i in range(self.batch_size):
             # Log the initial Q-values
            print(f"Initial Q-Values for State {i}: {target[i]}")
            if dones[i]:
                target[i][actions[i]] = rewards[i]
            else:
                a = np.argmax(target_next[i])
                target[i][actions[i]] = rewards[i] + self.gamma * target_val[i][a]
              # Log the updated Q-values
            print(f"Updated Q-Values for State {i}: {target[i]}")

        self.model.fit(states, target, epochs=1, verbose=0)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)

    def get_state(self, board):
        return np.array(board).reshape((1, 4, 4, 1))  # Adjust based on your board representation
