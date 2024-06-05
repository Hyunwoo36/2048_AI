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

    def conv_block(self, input_dim, output_dim):
        d = output_dim // 4
        inputs = Input(shape=(4, 4, input_dim))
        conv1 = Conv2D(d, (1, 1), padding='same', activation='relu')(inputs)
        conv2 = Conv2D(d, (2, 2), padding='same', activation='relu')(inputs)
        conv3 = Conv2D(d, (3, 3), padding='same', activation='relu')(inputs)
        conv4 = Conv2D(d, (4, 4), padding='same', activation='relu')(inputs)
        outputs = Concatenate()([conv1, conv2, conv3, conv4])
        return Model(inputs, outputs)

    def _build_model(self):
        inputs = Input(shape=(4, 4, 1))
        x = self.conv_block(1, 256)(inputs)
        x = self.conv_block(256, 512)(x)
        x = self.conv_block(512, 1024)(x)
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
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

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
        target_next = self.model.predict(next_states)
        target_val = self.target_model.predict(next_states)

        for i in range(self.batch_size):
            if dones[i]:
                target[i][actions[i]] = rewards[i]
            else:
                a = np.argmax(target_next[i])
                target[i][actions[i]] = rewards[i] + self.gamma * target_val[i][a]

        self.model.fit(states, target, epochs=1, verbose=0)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)

    def get_state(self, board):
        return np.array(board).reshape((1, 4, 4, 1))  # Adjust based on your board representation
