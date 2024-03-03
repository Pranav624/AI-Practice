import numpy as np, random, string

class Organism:
    def __init__(self, x, y, map_width, map_height, size, learn_rate=0.01):
        self.__intial_x = x
        self.__initial_y = y
        self.__x = x
        self.__y = y
        self.__map_width = map_width
        self.__map_height = map_height
        self.__size = size
        self.__color = (255, 255, 255)
        self.__genome = self.create_genome()
        self.__wih = np.random.uniform(-0.5, 0.5, (8, 16))
        self.__who = np.random.uniform(-0.5, 0.5, (4, 8))
        self.__bih = np.array([0.0 for _ in range(8)])
        self.__bho = np.array([0.0 for _ in range(4)])
        self.__ord_list = np.array([ord(char) for char in self.__genome])
        self.__h = []
        self.__nr_correct = 0
        self.__outputs = []
        self.f_prop()
        self.__labels = np.array([0, 0, 0, 0])
        self.__learn_rate = learn_rate

    def get_initial_position(self):
        return (self.__intial_x, self.__initial_y)

    def get_position(self):
        return (self.__x, self.__y)
    
    def set_position(self, x, y):
        self.__x = x
        self.__y = y

    def get_outputs(self):
        return self.__outputs
    
    def set_labels(self, l):
        self.__labels = l

    def get_labels(self):
        return self.__labels
    
    def get_color(self):
        return self.__color

    def create_genome(self):
        # Return 16 character list
        genome = random.choices(string.ascii_letters, k=16)
        ord_list = np.array([ord(char) for char in genome])
        sum_genome = sum(ord_list)
        if sum_genome % 4 == 0:
            self.__color = (255, 0, 0)
        elif sum_genome % 4 == 1:
            self.__color = (0, 255, 0)
        elif sum_genome % 4 == 2:
            self.__color = (0, 0, 255)
        else:
            self.__color = (0, 0, 0)
        return genome
        

    def f_prop(self):
        # Forward propogation, input -> hidden
        h_pre = self.__bih + self.__wih @ self.__ord_list
        h = 1 / (1 + np.exp(-h_pre))
        self.__h = np.array(h)
        # Forward propogation, hidden -> output
        o_pre = self.__bho + self.__who @ h
        o = 1 / (1 + np.exp(-o_pre))
        self.__outputs = o

    def b_prop(self):
        # Error calculation
        e = 1 / len(self.__outputs) * np.sum((self.__outputs - self.__labels) ** 2, axis = 0)
        self.__nr_correct += int(np.argmax(self.__outputs) == np.argmax(self.__labels))

        # Back propogation, output -> hidden
        delta_o = self.__outputs - self.__labels
        delta_o.shape += (1,)
        h = np.array(self.__h)
        h.shape += (1,)
        self.__who += -self.__learn_rate * delta_o @ np.transpose(h)
        bho = np.array(self.__bho)
        bho.shape += (1,)
        bho += -self.__learn_rate * delta_o
        self.__bho = [i[0] for i in bho]
        # Back propogation, hidden -> input
        ord_list = np.array(self.__ord_list)
        ord_list.shape += (1,)
        delta_h = np.transpose(self.__who) @ delta_o * (h * (1 - h))
        self.__wih += -self.__learn_rate * delta_h @ np.transpose(ord_list)
        bih = np.array(self.__bih)
        bih.shape += (1,)
        bih += -self.__learn_rate * delta_h
        self.__bih = [i[0] for i in bih]

    def step(self):
        total_value = sum(self.__outputs)
        probability_table = [i / total_value for i in self.__outputs]
        choice = random.choices(self.__outputs, weights=probability_table)
        if choice == self.__outputs[0]:
            if self.__x >= self.__size:
                self.__x -= self.__size
        elif choice == self.__outputs[1]:
            if self.__x <= self.__map_width - 2 * self.__size:
                self.__x += self.__size
        elif choice == self.__outputs[2]:
            if self.__y >= self.__size:
                self.__y -= self.__size
        else:
            if self.__y <= self.__map_height - 2 * self.__size:
                self.__y += self.__size