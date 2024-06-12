import random
import numpy as np
from collections import deque
import tensorflow as tf
from tensorflow.keras.layers import Conv2D, Concatenate, Flatten, Dense, Input, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam

class DQNAgent:
    def __init__(self, state_size, action_size, gamma=0.99, epsilon=0.9, epsilon_min=0.01, epsilon_decay=0.99, learning_rate=5e-5, batch_size=64, memory_size=50000):
        self.state_size = state_size
        self.action_size = action_size
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.memory = deque(maxlen=memory_size)
        self.model = self.build_model(state_size, action_size)
        self.target_model = self.build_model(state_size, action_size)
        self.update_target_model()
        self.actions = ['w', 'a', 's', 'd']
        self.rewards_history = []

    def build_model(self, input_shape, action_size):
        inputs = Input(shape=input_shape)

        # Convolutional layers with varied kernel sizes
        conv1a = Conv2D(64, (1, 1), activation='relu', padding='same')(inputs)
        conv1b = Conv2D(64, (2, 2), activation='relu', padding='same')(inputs)
        conv1c = Conv2D(64, (3, 3), activation='relu', padding='same')(inputs)
        conv1d = Conv2D(64, (4, 4), activation='relu', padding='same')(inputs)
        merged = Concatenate()([conv1a, conv1b, conv1c, conv1d])

        # Further processing
        conv2 = Conv2D(256, (2, 2), activation='relu')(merged)
        flat = Flatten()(conv2)
        dense1 = Dense(1024, activation='relu')(flat)
        dropout = Dropout(0.5)(dense1)
        outputs = Dense(action_size, activation='linear')(dropout)

        model = Model(inputs=inputs, outputs=outputs)
        model.compile(optimizer=Adam(learning_rate=self.learning_rate), loss='mse')
        return model

    def choose_action(self, state):
        if np.random.rand() <= self.epsilon:
            return random.choice([0, 1, 2, 3])  # Assuming 0, 1, 2, 3 correspond to ['w', 'a', 's', 'd']
        state = np.array(state).reshape((1, 4, 4, 1))
        q_values = self.model.predict(state)
        return np.argmax(q_values[0])

    def update(self, state, action, reward, next_state, done):
        # Ensure state and next_state are numpy arrays with the correct shape
        state = np.array(state).reshape((1, 4, 4, 1))
        next_state = np.array(next_state).reshape((1, 4, 4, 1))

        # Predict the current Q-values and the future Q-values from the models
        current_q = self.model.predict(state)[0]
        future_q = np.max(self.target_model.predict(next_state)[0])

        # Debugging output to understand what is happening
        print(f"Current Q-values: {current_q}, Action chosen: {action}, Reward: {reward}")

        # Check action type and range to prevent IndexError
        if isinstance(action, int) and 0 <= action < len(current_q):
            # Update the Q-value for the action taken
            if done:
                current_q[action] = reward
            else:
                current_q[action] = reward + self.gamma * future_q
            # Fit model with the updated Q-values
            self.model.fit(state, current_q.reshape((1, self.action_size)), epochs=1, verbose=0)
        else:
            print(f"Error: Invalid action index '{action}'")


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
        target = self.model.predict(states)
        target_val = self.target_model.predict(next_states)
        for i in range(self.batch_size):
            if dones[i]:
                target[i][actions[i]] = rewards[i]
            else:
                target[i][actions[i]] = rewards[i] + self.gamma * np.amax(target_val[i])
        self.model.fit(states, target, epochs=1, verbose=0)

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)

    def get_state(self, board):
        return np.array(board).reshape((1, 4, 4, 1))

