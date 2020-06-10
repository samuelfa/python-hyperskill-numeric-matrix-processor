import copy

class Matrix:
    def __init__(self, rows=None, cols=None, values=None):
        self.rows = rows
        self.cols = cols
        self.values = values

    def same_size(self, other_matrix):
        return self.rows == other_matrix.rows \
                and self.cols == other_matrix.cols

    def multiply_by_constant(self, other):
        result = self.values[:]
        for i in range(self.rows):
            for j in range(self.cols):
                result[i][j] *= other

        return Matrix(self.rows, self.cols, result)

    def multiply_by_matrix(self, other):
        if self.cols != other.rows:
            return "ERROR"

        values = []
        for i in range(self.rows):
            row = []
            for j in range(other.cols):
                number = 0
                for x in range(self.cols):
                    number += self.values[i][x] * other[x][j]
                row.append(number)
            values.append(row)

        return Matrix(self.rows, self.cols, values)

    def __getitem__(self, i):
        return self.values[i]

    def __add__(self, other):
        if not self.same_size(other):
            return "ERROR"

        result = self.values[:]
        for i in range(self.rows):
            for j in range(self.cols):
                result[i][j] += other[i][j]

        return Matrix(self.rows, self.rows, result)

    def __mul__(self, other):
        if type(other) is Matrix:
            return self.multiply_by_matrix(other)
        else:
            return self.multiply_by_constant(other)

    def __str__(self):
        rows = []
        for row in self.values:
            rows.append(' '.join(list(map(str, row))))

        return '\n'.join(rows)

    def transpose_main_diagonal(self):
        values = copy.deepcopy(self.values)
        for i in range(self.rows):
            for j in range(self.cols):
                values[j][i] = self.values[i][j]
        return Matrix(self.cols, self.rows, values)

    def transpose_side_diagonal(self):
        values = copy.deepcopy(self.values)

        for i in range(self.rows):
            for j in range(self.cols):
                values[self.rows - j - 1][self.cols - i - 1] = self.values[i][j]

        return Matrix(self.cols, self.rows, values)

    def transpose_vertical_line(self):
        values = copy.deepcopy(self.values)
        for rows in values:
            rows.reverse()
        return Matrix(self.rows, self.cols, values)

    def transpose_horizontal_line(self):
        values = copy.deepcopy(self.values)
        values.reverse()
        return Matrix(self.rows, self.cols, values)

    def determinant(self):
        if self.cols != self.rows:
            raise Exception('The operation cannot be performed.')
        if self.cols == 1:
            return self.values[0][0]
        if self.cols == 2:
            return self.values[0][0] * self.values[1][1] - self.values[1][0] * self.values[0][1]

        determinant = 0
        for i in range(self.rows):
            minor = Matrix(self.rows - 1, self.cols - 1, [[self.values[x][j] for j in range(self.cols) if j != i] for x in range(1, self.rows)])
            determinant += self.values[0][i] * minor.determinant() * (-1)**(1+i+1)
        return determinant

    def cofactor_matrix(self):
        matrix = Matrix(self.rows, self.cols, copy.deepcopy(self.values))

        for i in range(self.rows):
            for j in range(self.cols):
                values = [[self.values[x][y] for y in range(self.cols) if y != j] for x in range(self.rows) if i != x]
                minor = Matrix(self.rows - 1, self.cols - 1, values)
                determinant = minor.determinant()
                value = determinant * (-1)**(i+j)
                matrix.values[i][j] = value

        return matrix

    def inverse(self):
        determinant = self.determinant()
        if determinant == 0:
            raise RuntimeError('Invalid operation')

        matrix = self.cofactor_matrix()
        matrix = matrix.transpose_main_diagonal()
        return matrix.multiply_by_constant(1 / determinant)


class Menu:
    @staticmethod
    def options():
        print("1. Add matrices")
        print("2. Multiply matrix by a constant")
        print("3. Multiply matrices")
        print("4. Transpose matrix")
        print("5. Calculate a determinant")
        print("6. Inverse matrix")
        print("0. Exit")

    def sum_matrices(self):
        matrix_a = self.create_matrix('Enter size of first matrix: ', 'Enter first matrix:')
        matrix_b = self.create_matrix('Enter size of second matrix: ', 'Enter second matrix:')
        print('The result is:')
        print(matrix_a + matrix_b)

    def mul_matrix_by_constant(self):
        matrix = self.create_matrix('Enter size of matrix: ', 'Enter matrix:')
        number = float(input('Enter constant: '))
        print('The result is:')
        print(matrix * number)

    def mul_matrices(self):
        matrix_a = self.create_matrix('Enter size of first matrix: ', 'Enter first matrix:')
        matrix_b = self.create_matrix('Enter size of second matrix: ', 'Enter second matrix:')
        print('The result is:')
        print(matrix_a * matrix_b)

    def transpose_matrix(self):
        print('1. Main diagonal')
        print('2. Side diagonal')
        print('3. Vertical line')
        print('4. Horizontal line')

        option = int(input("Your choise: "))
        matrix = self.create_matrix('Enter size of matrix: ', 'Enter matrix:')
        if option == 1:
            another_matrix = matrix.transpose_main_diagonal()
        elif option == 2:
            another_matrix = matrix.transpose_side_diagonal()
        elif option == 3:
            another_matrix = matrix.transpose_vertical_line()
        elif option == 4:
            another_matrix = matrix.transpose_horizontal_line()
        else:
            return

        print("The result is:")
        print(another_matrix)

    def matrix_determinant(self):
        matrix = self.create_matrix('Enter size of matrix: ', 'Enter matrix:')
        value = matrix.determinant()

        print("The result is:")
        print(value)

    def matrix_inverse(self):
        matrix = self.create_matrix('Enter size of matrix: ', 'Enter matrix:')
        try:
            value = matrix.inverse()
        except RuntimeError:
            print("This matrix doesn't have an inverse.")
            return

        print("The result is:")
        print(value)


    @staticmethod
    def create_matrix(message_size, message_values):
        rows, cols = map(int, input(message_size).split())
        print(message_values)
        values = []
        for i in range(rows):
            row = list(map(float, input().split(maxsplit=cols)))
            values.append(row)

        return Matrix(rows, cols, values)

    def run(self):
        while True:
            self.options()
            option = int(input('Your choice: '))
            if option == 1:
                self.sum_matrices()
            elif option == 2:
                self.mul_matrix_by_constant()
            elif option == 3:
                self.mul_matrices()
            elif option == 4:
                self.transpose_matrix()
            elif option == 5:
                self.matrix_determinant()
            elif option == 6:
                self.matrix_inverse()
            else:
                break


menu = Menu()
menu.run()
