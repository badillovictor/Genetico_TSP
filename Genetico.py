import math
import random
import os
import numpy


def calculate_fitness():
    for solution in range(size):
        fitness[solution] = 0
        for j in range(n - 1):
            fitness[solution] += matrix[population[solution][j]][population[solution][j + 1]]
        fitness[solution] += matrix[population[solution][-1]][population[solution][0]]


def crossover():
    for child in range(size):
        # region Find parents
        if not live_status[child]:
            parent1 = random.randint(0, size - 1)
            while not live_status[parent1]:
                parent1 = random.randint(0, size - 1)
            parent2 = random.randint(0, size - 1)
            while not live_status[parent2] or parent2 == parent1:
                parent2 = random.randint(0, size - 1)
            # endregion
            # region Genes Parent1
            j1 = random.randint(0, n)
            j2 = random.randint(0, n)
            if j2 < j1:
                temp = j2
                j2 = j1
                j1 = temp
            genes = [0 for y in range(n)]
            for j in range(n):
                population[child][j] = -1
            for j in range(j1, j2):
                population[child][j] = population[parent1][j]
                genes[population[parent1][j]] = 1
            # endregion
            # region Genes Parent2
            j2 = 0
            for j1 in range(n):
                while j2 < n and population[child][j2] != -1:
                    j2 += 1
                if genes[population[parent2][j1]] == 0:
                    population[child][j2] = population[parent2][j1]
                    j2 += 1
            # endregion
            # region Mutation
            mutation = random.randint(1, 100)
            if mutation == 1:
                x1 = random.randint(0, n - 1)
                x2 = random.randint(0, n - 1)
                while x2 == x1:
                    x2 = random.randint(0, n - 1)
                temp = population[child][x1]
                population[child][x1] = population[child][x2]
                population[child][x2] = temp
            # endregion
            live_status[child] = True


def selection():
    max_dead = size * .75
    average = numpy.average(fitness)
    for solution in range(size):
        if max_dead > 0 and fitness[solution] > average:
            max_dead -= 1
            live_status[solution] = False


if __name__ == '__main__':
    export = []
    paths = []
    for path in os.listdir('TSP Instances'):
        if os.path.isfile(os.path.join('TSP Instances', path)):
            paths.append(path)
    for path in paths:
        # region Lecture and TSP Graph Creation
        with open('TSP Instances/{0}'.format(path), 'r') as file:
            file.readline()
            file.readline()
            file.readline()
            n = int(file.readline().strip().split(':')[1])
            file.readline()
            file.readline()
            cities = numpy.zeros((n, 2))
            for i in range(n):
                cities[i] = file.readline().strip().split(' ')[1:]
            matrix = numpy.zeros((n, n))
            for i in range(n - 1):
                for j in range(i + 1, n):
                    matrix[i][j] = int(
                        math.sqrt((cities[i][0] - cities[j][0]) ** 2 + (cities[i][1] - cities[j][1]) ** 2))
                    matrix[j][i] = matrix[i][j]
        # endregion
        # region Initial Population
        size = 200
        population = [[0 for i in range(n)] for i in range(size)]
        live_status = [False for i in range(size)]
        fitness = [0 for i in range(size)]
        patient_zero = [i for i in range(n)]
        generations_to_stop = 10
        for i in range(0, 100):
            population[i] = random.sample(patient_zero, len(patient_zero))
            live_status[i] = True
        crossover()
        calculate_fitness()
        selection()
        # endregion
        # region Loop
        last_best = min(fitness)
        generations_since_last_upgrade = 0
        while generations_since_last_upgrade != generations_to_stop:
            crossover()
            calculate_fitness()
            selection()
            generations_since_last_upgrade += 1
            if min(fitness) != last_best:
                generations_since_last_upgrade = 0
                last_best = min(fitness)
        temp = [path, last_best]
        export.append(temp)
        print('File {0} has a best solution with a distance of {1}'.format(path, last_best))
        # endregion
    with open('Export.csv', 'w') as f:
        for e in export:
            e[1] = str(e[1])
            f.write(','.join(e))
            f.write('\n')
