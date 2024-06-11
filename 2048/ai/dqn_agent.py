import random
import numpy as np
from collections import deque
import tensorflow as tf
from tensorflow.keras.layers import Conv2D, Concatenate, Flatten, Dense, Input, Dropout
from tensorflow.keras.models import Model, Sequential
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
    
    def choose_action(self, state):
        if np.random.rand() <= self.epsilon:
            return random.choice([0, 1, 2, 3])  # Assuming 0, 1, 2, 3 correspond to ['w', 'a', 's', 'd']

        state = state.reshape((1, 4, 4, 1))  # Reshape state to fit the network input
        q_values = self.model.predict(state)
        return np.argmax(q_values[0])
    
    def update(self, state, action, reward, next_state, done):
        # Ensure state and next_state are numpy arrays with the correct shape
        state = np.array(state).reshape((1, 4, 4, 1))
        next_state = np.array(next_state).reshape((1, 4, 4, 1))

        # Predict the current and future Q-values
        current_target = self.model.predict(state)[0]
        future_q_value = np.amax(self.target_model.predict(next_state)[0])

        # Debugging output
        print(f"Current Q-values: {current_target}, Action chosen: {action}, Reward: {reward}")

        # Check action type and range
        if not isinstance(action, int) or action < 0 or action >= len(current_target):
            print(f"Error: Invalid action index '{action}'")
            return  # You might want to handle this case more gracefully

        # Update the Q-value for the action taken
        if done:
            current_target[action] = reward
        else:
            current_target[action] = reward + self.gamma * future_q_value

        # Fit the model with the updated Q-values
        self.model.fit(state, current_target.reshape((1, self.action_size)), epochs=1, verbose=0)



    
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
        print("Predicting target model values")
        target_val = self.target_model.predict(next_states)

        for i in range(self.batch_size):
            if dones[i]:
                target[i][actions[i]] = rewards[i]
            else:
                target[i][actions[i]] = rewards[i] + self.gamma * np.amax(target_val[i])

        self.model.fit(states, target, epochs=1, verbose=0)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)

    def get_state(self, board):
        return np.array(board).reshape((1, 4, 4, 1))  # Adjust based on your board representation
