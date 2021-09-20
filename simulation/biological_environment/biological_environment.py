import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

INIT_PHYSICAL = 10.0
INIT_SPEED = 0.3
INIT_INTELLIGENCE = 0.2
DEVIATION_PHYSICAL = 0.2
DEVIATION_SPEED = 0.1
DEVIATION_INTELLIGENCE = 0.1


class Animal:
    def __init__(self, field,
                 physical=random.uniform(INIT_PHYSICAL-DEVIATION_PHYSICAL, INIT_PHYSICAL+DEVIATION_PHYSICAL),
                 speed=random.uniform(INIT_SPEED-DEVIATION_SPEED, INIT_SPEED+DEVIATION_SPEED),
                 intelligence=random.uniform(INIT_INTELLIGENCE-DEVIATION_INTELLIGENCE,
                                             INIT_INTELLIGENCE+DEVIATION_INTELLIGENCE)):
        self.physical = physical
        self.life = self.physical
        self.age = 0
        self.speed = speed
        self.food_volume = self.physical/5
        self.intelligence = intelligence
        self.field = field
        self.pos = [np.random.random()*(self.field.size[0]-1), np.random.random()*(self.field.size[1]-1)]

    def action(self):
        self.move()
        self.eat()
        self.age += 1

    def move(self):
        # ランダム行動の場合
        if random.random() > self.intelligence:
            self.pos[0] = self.pos[0] + (np.random.random() - 0.5) * self.speed
            self.pos[1] = self.pos[1] + (np.random.random() - 0.5) * self.speed
            if self.pos[0] < -0.5: self.pos[0] += self.field.size[0]
            if self.pos[0] > self.field.size[0] - 0.5: self.pos[0] -= self.field.size[0]
            if self.pos[1] < 0.5: self.pos[1] += self.field.size[1]
            if self.pos[1] > self.field.size[1] - 0.5: self.pos[1] -= self.field.size[1]
        # 知能行動
        else:
            # 現在エリアを算出
            x, y = round(self.pos[0]), round(self.pos[1])
            x_1 = (x+1) % self.field.size[0]
            y_1 = (y+1) % self.field.size[1]
            # 自エリア周りの9マスで一番食料があるエリアを検索
            search_list = [[y-1, x-1, -1, -1], [y-1, x, -1, 0], [y-1, x_1, -1, 1], [y, x-1, 0, -1],
                           [y, x, np.random.random() - 0.5, np.random.random() - 0.5],
                           [y, x_1, 0, 1], [y_1, x-1, 1, -1], [y_1, x, 1, 0], [y_1, x_1, 1, 1]]
            max_value, target_pos = 0, (y, x)
            for s in search_list:
                if self.field.field[s[0], s[1]] > max_value:
                    max_value = self.field.field[s[0], s[1]]
                    target_dir = (s[2], s[3])
            self.pos[0] = self.pos[0] + (0.5 * target_dir[0]) * self.speed
            self.pos[1] = self.pos[1] + (0.5 * target_dir[1]) * self.speed
            if self.pos[0] < -0.5: self.pos[0] += self.field.size[0]
            if self.pos[0] > self.field.size[0] - 0.5: self.pos[0] -= self.field.size[0]
            if self.pos[1] < 0.5: self.pos[1] += self.field.size[1]
            if self.pos[1] > self.field.size[1] - 0.5: self.pos[1] -= self.field.size[1]
        self.life -= self.food_volume/2

    def eat(self):
        x, y = round(self.pos[0]), round(self.pos[1])
        if self.field.field[y, x] > self.food_volume:
            self.field.field[y, x] -= self.food_volume
            self.life += self.food_volume


class Breeder:
    def __init__(self, animals, field):
        self.animals = animals
        self.field = field
        self.breed_length = 0.5

    def breed(self):
        pair = self.select_pair()
        if pair is not None:
            physical = random.uniform(self.animals[pair[0]].physical, self.animals[pair[1]].physical) + \
                random.uniform(-DEVIATION_PHYSICAL, DEVIATION_PHYSICAL)
            speed = random.uniform(self.animals[pair[0]].speed, self.animals[pair[1]].speed) + \
                random.uniform(-DEVIATION_SPEED, DEVIATION_SPEED)
            intelligence = random.uniform(self.animals[pair[0]].intelligence, self.animals[pair[1]].intelligence) + \
                random.uniform(-DEVIATION_INTELLIGENCE, DEVIATION_INTELLIGENCE)
            child = Animal(field=self.field, physical=physical, speed=speed, intelligence=intelligence)
            self.animals.append(child)

    def select_pair(self):
        pairs = []
        for i in range(len(self.animals)-1):
            for j in range(i+1, len(self.animals)):
                if abs(self.animals[i].pos[0] - self.animals[j].pos[0]) < self.breed_length and \
                   abs(self.animals[i].pos[1] - self.animals[j].pos[1]) < self.breed_length:
                    pairs.append((i, j))
        if len(pairs) != 0:
            return random.choice(pairs)


class Enemy:
    def __init__(self, physical, speed, intelligence, field, animals):
        self.physical = physical
        self.speed = speed
        self.intelligence = intelligence
        self.field = field
        self.pos = [np.random.random()*(self.field.size[0]-1), np.random.random()*(self.field.size[1]-1)]
        self.animals = animals
        self.eat_range = 0.5

    def action(self):
        self.move()
        self.eat()

    def move(self):
        self.pos[0] = self.pos[0] + (np.random.random() - 0.5) * self.speed
        self.pos[1] = self.pos[1] + (np.random.random() - 0.5) * self.speed
        if self.pos[0] < -0.5: self.pos[0] += self.field.size[0]
        if self.pos[0] > self.field.size[0] - 0.5: self.pos[0] -= self.field.size[0]
        if self.pos[1] < 0.5: self.pos[1] += self.field.size[1]
        if self.pos[1] > self.field.size[1] - 0.5: self.pos[1] -= self.field.size[1]

    def eat(self):
        candidates = []
        for i, a in enumerate(self.animals):
            if abs(self.animals[i].pos[0] - self.pos[0]) < self.eat_range and \
               abs(self.animals[i].pos[1] - self.pos[1]) < self.eat_range:
                candidates.append(i)
        if len(candidates) != 0:
            target = random.choice(candidates)
            del self.animals[target]


class Field:
    def __init__(self, size, wealth, grow_speed=5, grow_interval=30):
        self.size = size
        self.wealth = wealth
        self.field = np.random.randint(self.wealth/4, self.wealth*3/4, size)
        self.grow_filter = np.full(size, grow_speed)
        self.grow_interval = grow_interval

    def grow(self, steps):
        if steps % self.grow_interval == 0:
            self.field += self.grow_filter
            self.field = np.where(self.field >= self.wealth, self.wealth, self.field)


class Simulator:
    def __init__(self, size):
        self.field = Field(size=size, wealth=30.)
        self.animals = [Animal(field=self.field) for i in range(20)]
        self.enemies = [Enemy(physical=30., speed=1., intelligence=.1, field=self.field, animals=self.animals) \
                        for i in range(3)]
        self.breeder = Breeder(animals=self.animals, field=self.field)
        self.images = []
        self.steps = 0
        self.record_data = []

    def step(self):
        self.steps += 1
        dead_list = []
        for i, a in enumerate(self.animals):
            a.action()
            if a.life <= 0:
                dead_list.append(i)
        for d in reversed(dead_list):
            del self.animals[d]
        for e in self.enemies:
            e.action()
        self.field.grow(self.steps)
        self.breeder.breed()
        self.plot()
        self.record()

    def record(self):
        if len(self.animals) != 0:
            max_age = max([a.age for a in self.animals])
            ave_age = np.average([a.age for a in self.animals])
            ave_physical = np.average([a.physical for a in self.animals])
            ave_speed = np.average([a.speed for a in self.animals])
            ave_intelligence = np.average([a.intelligence for a in self.animals])
            self.record_data.append([max_age, ave_age, ave_physical, ave_speed, ave_intelligence])
            print('steps:', self.steps, ', animals:', len(self.animals))
        else:
            print('steps:', self.steps, ', Destruction!')

    def draw_graph(self):
        ages = [[i[0], i[1]] for i in self.record_data]
        plt.plot(ages)
        plt.legend(['max_age', 'ave_age'])
        plt.savefig('max_ave_age.png')
        plt.show()
        ability = [[i[2]] for i in self.record_data]
        plt.plot(ability)
        plt.legend(['ave_physical'])
        plt.savefig('ave_physical.png')
        plt.show()
        ability = [[i[3]] for i in self.record_data]
        plt.plot(ability)
        plt.legend(['ave_speed'])
        plt.savefig('ave_speed.png')
        plt.show()
        ability = [[i[4]] for i in self.record_data]
        plt.plot(ability)
        plt.legend(['ave_intelligence'])
        plt.savefig('ave_intelligence.png')
        plt.show()

    def plot(self):
        ax = []
        title = plt.text(0.0, -1.0, 'steps:'+format(self.steps), fontsize='large')
        ax.append(title)
        a = plt.imshow(self.field.field, cmap='YlGn', interpolation='nearest', vmin=0, vmax=self.field.wealth)
        ax.append(a)
        for animal in self.animals:
            a, = plt.plot(animal.pos[0], animal.pos[1], marker='o', markersize=10, color='#4682b4')
            ax.append(a)
        for enemy in self.enemies:
            e, = plt.plot(enemy.pos[0], enemy.pos[1], marker='o', markersize=15, color='#ff6347')
            ax.append(e)
            axes = plt.gca()
            circle = plt.Circle((enemy.pos[0], enemy.pos[1]), 0.5, color='#ff6347', fill=False)
            ax.append(axes.add_patch(circle))
        self.images.append(ax)


if __name__ == '__main__':
    fig = plt.figure()

    size = [10, 10]
    sim = Simulator(size=size)
    for i in range(1000):
        sim.step()

    ani = animation.ArtistAnimation(fig, sim.images, interval=250)
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=10, metadata=dict(artist='Me'), bitrate=1800)
    ani.save('result.mp4', writer=writer)
    plt.show()

    sim.draw_graph()
