import numpy as np, random, string

class Organism:
    def __init__(self, x, y, map_width, map_height, size, learn_rate=0.01):
        self.__x = x
        self.__y = y
        self.__map_width = map_width
        self.__map_height = map_height
        self.__size = size
        self.__genome = self.create_genome()
        self.__wih = np.random.uniform(-0.5, 0.5, (8, 16))
        self.__who = np.random.uniform(-0.5, 0.5, (4, 8))
        self.__bih = [0 for _ in range(8)]
        self.__bho = [0 for _ in range(4)]
        self.__outputs = self.f_prop()
        self.__learn_rate = learn_rate

    def get_position(self):
        return (self.__x, self.__y)
    
    def create_genome(self):
        # Return 16 character string
        return random.choices(string.ascii_letters, k=16)
        

    def f_prop(self):
        ord_list = [ord(char) for char in self.__genome]

        # Forward propogation, input -> hidden
        h_pre = self.__bih + self.__wih @ ord_list
        h = 1 / (1 + np.exp(-h_pre))
        # Forward propogation, hidden -> output
        o_pre = self.__bho + self.__who @ h
        o = 1 / (1 + np.exp(-o_pre))
        return o

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


# Testing
        
# s = random.choices(string.ascii_letters, k=16)
# ord_list = [ord(char) for char in s]

# wih = np.random.uniform(-0.5, 0.5, (8, 16))
# who = np.random.uniform(-0.5, 0.5, (4, 8))
# bih = [0 for _ in range(8)]
# bho = [0 for _ in range(4)]

# # Forward propogation, input -> hidden
# h_pre = bih + wih @ ord_list
# h = 1 / (1 + np.exp(-h_pre))
# # Forward propogation, hidden -> output
# o_pre = bho + who @ h
# o = 1 / (1 + np.exp(-o_pre))
# print(o)
# total_value = sum(o)
# probability_table = [i / total_value for i in o]
# print(probability_table)
# move = random.choices(o, weights=probability_table)
# print(move)
# if move == o[0]:
#     print("left")
# elif move == o[1]:
#     print("right")
# elif move == o[2]:
#     print("up")
# elif move == o[3]:
#     print("down")