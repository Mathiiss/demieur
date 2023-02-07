class Utils:
    # genere un tableau avec toutes les valeurs ou l'on ne peut pas mettre de bombes, cad 3x3 autour de la génération

    def impossible_array(self, i, j, row, column):
        total = [[i, j]]
        if j > 0:
            total.append([i, (j-1)])
        if i > 0:
            total.append([(i-1), j])
        if i < column-1:
            total.append([(i+1), j])
        if j < row-1:
            total.append([i, (j+1)])
        if i > 0 and j > 0:
            total.append([(i-1), (j-1)])
        if i < column-1 and j < row-1:
            total.append([(i+1), (j+1)])
        if i > 0 and j < row-1:
            total.append([(i-1), (j+1)])
        if i < column-1 and j > 0:
            total.append([(i+1), (j-1)])
        return total
        # verifie le nombre de bombe a une coordonnée precise

    def get_adjacent_numbers(self, grid, i, j, row, column):
        total = []
        if j > 0:
            total.append(grid[i][(j-1)])
        if i > 0:
            total.append(grid[(i-1)][j])
        if i < column-1:
            total.append(grid[(i+1)][j])
        if j < row-1:
            total.append(grid[i][(j+1)])
        if i > 0 and j > 0:
            total.append(grid[(i-1)][(j-1)])
        if i < column-1 and j < row-1:
            total.append(grid[(i+1)][(j+1)])
        if i > 0 and j < row-1:
            total.append(grid[(i-1)][(j+1)])
        if i < column-1 and j > 0:
            total.append(grid[(i+1)][(j-1)])
        return str(total.count('b'))

    def get_adjacent_numbers2(self, grid, i, j, row, column):
        total = []
        if j > 0:
            if (grid[j-1][i] == '0'):
                total.append([i, (j-1)])
        if i > 0:
            if (grid[j][i-1] == '0'):
                total.append([i-1, j])
        if i < row-1:
            if (grid[j][i+1] == '0'):
                total.append([(i+1), j])
        if j < column-1:
            if (grid[j+1][i] == '0'):
                total.append([i, j+1])
        if i > 0 and j > 0:
            if (grid[(j-1)][(i-1)] == '0'):
                total.append([(i-1), (j-1)])
        if i < row-1 and j < column-1:
            if (grid[(j+1)][(i+1)] == '0'):
                total.append([(i+1), (j+1)])
        if i > 0 and j < column-1:
            if (grid[(j+1)][(i-1)] == '0'):
                total.append([(i-1), (j+1)])
        if i < row-1 and j > 0:
            if (grid[(j-1)][(i+1)] == '0'):
                total.append([(i+1), (j-1)])
        return total

    def get_nb_flag(self, grid, grid_hide, i, j, row, column):
        total = 0
        arthur = []
        if j > 0:
            if (grid_hide[j-1][i] == 'F'):
                total += 1
        if i > 0:
            if (grid_hide[j][i-1] == 'F'):
                total += 1
        if i < row-1:
            if (grid_hide[j][i+1] == 'F'):
                total += 1
        if j < column-1:
            if (grid_hide[j+1][i] == 'F'):
                total += 1
        if i > 0 and j > 0:
            if (grid_hide[(j-1)][(i-1)] == 'F'):
                total += 1
        if i < row-1 and j < column-1:
            if (grid_hide[(j+1)][(i+1)] == 'F'):
                total += 1
        if i > 0 and j < column-1:
            if (grid_hide[(j+1)][(i-1)] == 'F'):
                total += 1
        if i < row-1 and j > 0:
            if (grid_hide[(j-1)][(i+1)] == 'F'):
                total += 1

        if int(grid[j][i]) <= total and grid_hide[j][i] != '*':
            if j > 0:
                if (grid_hide[j-1][i] == '*'):
                    arthur.append([i, j-1])
            if i > 0:
                if (grid_hide[j][i-1] == '*'):
                    arthur.append([i-1, j])
            if i < row-1:
                if (grid_hide[j][i+1] == '*'):
                    arthur.append([i+1, j])
            if j < column-1:
                if (grid_hide[j+1][i] == '*'):
                    arthur.append([i, j+1])
            if i > 0 and j > 0:
                if (grid_hide[(j-1)][(i-1)] == '*'):
                    arthur.append([(i-1), (j-1)])
            if i < row-1 and j < column-1:
                if (grid_hide[(j+1)][(i+1)] == '*'):
                    arthur.append([(i+1), (j+1)])
            if i > 0 and j < column-1:
                if (grid_hide[(j+1)][(i-1)] == '*'):
                    arthur.append([(i-1), (j+1)])
            if i < row-1 and j > 0:
                if (grid_hide[(j-1)][(i+1)] == '*'):
                    arthur.append([(i+1), (j-1)])
            # print(arthur)
        return arthur
        # verifie le nombre de bombe a une coordonnée precise

    def tryMiddleClick(self, grid, i, j, row, column):
        arthur = []
        if grid[j][i] != '*':
            if j > 0:
                if (grid[j-1][i] == '*'):
                    arthur.append([i, j-1])
            if i > 0:
                if (grid[j][i-1] == '*'):
                    arthur.append([i-1, j])
            if i < row-1:
                if (grid[j][i+1] == '*'):
                    arthur.append([i+1, j])
            if j < column-1:
                if (grid[j+1][i] == '*'):
                    arthur.append([i, j+1])
            if i > 0 and j > 0:
                if (grid[(j-1)][(i-1)] == '*'):
                    arthur.append([(i-1), (j-1)])
            if i < row-1 and j < column-1:
                if (grid[(j+1)][(i+1)] == '*'):
                    arthur.append([(i+1), (j+1)])
            if i > 0 and j < column-1:
                if (grid[(j+1)][(i-1)] == '*'):
                    arthur.append([(i-1), (j+1)])
            if i < row-1 and j > 0:
                if (grid[(j-1)][(i+1)] == '*'):
                    arthur.append([(i+1), (j-1)])

        return arthur
