def main():
    # Input the data
    s = [float(x) for x in input("Enter the coefficients of supply S: ").split()]

    d = [float(x) for x in input("Enter the coefficients of demand D: ").split()]

    print("Enter the cost matrix C:")
    c = [[] for _ in range(len(s))]
    for i in range(len(s)):
        c[i] = [float(x) for x in input(f"row {i + 1}: ").split()]
    print()

    # Print the data
    print("The transportation problem is:")
    print_matrix(s, d, c)
    print()

    # Check if all values are positive and not all are 0's
    finish = 1
    for i in s:
        if i < 0:
            print("The method is not applicable!")
            return
        if i > 0:
            finish = 0

    if finish == 1:
        print("The method is not applicable!")
        return

    # Check if the problem is balanced
    if sum(s) != sum(d):
        print("The problem is not balanced!")
        return

        # Check if all values are positive and not all are 0's
        finish = 1
        for i in d:
            if i < 0:
                print("The method is not applicable!")
                return
            if i > 0:
                finish = 0

        if finish == 1:
            print("The method is not applicable!")
            return

        # Check if all values are positive and not all are 0's
        for i in c:
            finish = 1
            for j in i:
                if j < 0:
                    print("The method is not applicable!")
                    return
                if j > 0:
                    finish = 0
            if finish == 1:
                print("The method is not applicable!")
                return

    # Find the initial feasible solution using the North-West Corner Rule
    print("The initial feasible solution using the North-West Corner Rule is:")
    x0_northwest = northwest(s, d, c)
    print_matrix(s, d, x0_northwest)
    print(f"Cost: {find_cost(c, x0_northwest)}")
    print()

    # Find the initial feasible solution using the Vogel's Approximation Method
    print("The initial feasible solution using the Vogel's Approximation Method is:")
    x0_vogel = vogel(s, d, c)
    print_matrix(s, d, x0_vogel)
    print(f"Cost: {find_cost(c, x0_vogel)}")
    print()

    # Find the initial feasible solution using the Russell's Approximation Method
    print("The initial feasible solution using the Russell's Approximation Method is:")
    x0_russel = russel(s, d, c)
    print_matrix(s, d, x0_russel)
    print(f"Cost: {find_cost(c, x0_russel)}")


def northwest(s, d, c):
    # Initialize the solution
    x = [[0 for _ in range(len(d))] for _ in range(len(s))]
    # Copy the variables
    s = s.copy()
    d = d.copy()

    # Construct the solution
    row = 0
    col = 0
    while row < len(s) and col < len(d):
        # Find the amount to be transported
        if s[row] < d[col]:
            x[row][col] = s[row]
            d[col] -= s[row]
            s[row] = 0
        elif s[row] > d[col]:
            x[row][col] = d[col]
            s[row] -= d[col]
            d[col] = 0
        else:
            x[row][col] = s[row]
            s[row] = 0
            d[col] = 0

        # print(f"Select S{row+1} D{col+1} ({x[row][col]})")
        # print_matrix(s, d, x)

        # Check if the supply or demand is empty
        if s[row] == 0:
            row += 1
        if d[col] == 0:
            col += 1

    return x


def vogel(s, d, c):
    # Initialize the solution
    x = [[0 for _ in range(len(d))] for _ in range(len(s))]
    # Copy the variables
    s = s.copy()
    d = d.copy()
    c = [[v for v in row] for row in c]

    # Construct the solution
    while sum(s) != 0 and sum(d) != 0:
        # Find differences
        diff_row = [0 for _ in range(len(s))]
        for row in range(len(s)):
            if s[row] == 0:
                diff_row[row] = -1
                continue
            min1 = min2 = 1000000000
            for col in range(len(d)):
                if d[col] == 0:
                    continue
                if c[row][col] <= min1:
                    min2 = min1
                    min1 = c[row][col]
                elif c[row][col] <= min2:
                    min2 = c[row][col]

                if min1 == -1:
                    diff_row[row] = 1000000000
                elif min2 == 1000000000:
                    diff_row[row] = min1
                else:
                    diff_row[row] = min2 - min1
        diff_col = [0 for _ in range(len(d))]
        for col in range(len(d)):
            if d[col] == 0:
                diff_col[col] = -1
                continue
            min1 = min2 = 1000000000
            for row in range(len(s)):
                if s[row] == 0:
                    continue
                if c[row][col] <= min1:
                    min2 = min1
                    min1 = c[row][col]
                elif c[row][col] <= min2:
                    min2 = c[row][col]

            if min1 == -1:
                diff_col[col] = 1000000000
            elif min2 == 1000000000:
                diff_col[col] = min1
            else:
                diff_col[col] = min2 - min1

        # Find the maximum difference
        max_diff_row = max(diff_row)
        max_diff_col = max(diff_col)
        if max_diff_row > max_diff_col:
            row = diff_row.index(max_diff_row)
            col = None
            for i in range(len(c[row])):
                if d[i] == 0:
                    continue
                if col is None or c[row][i] < c[row][col]:
                    col = i
        else:
            col = diff_col.index(max_diff_col)
            row = None
            for i in range(len(c)):
                if s[i] == 0:
                    continue
                if row is None or c[i][col] < c[row][col]:
                    row = i

        # Find the amount to be transported
        if s[row] < d[col]:
            x[row][col] = s[row]
            d[col] -= s[row]
            s[row] = 0

            for i in range(len(d)):
                c[row][i] = 0

        elif s[row] > d[col]:
            x[row][col] = d[col]
            s[row] -= d[col]
            d[col] = 0

            for i in range(len(s)):
                c[i][col] = 0
        else:
            x[row][col] = s[row]
            s[row] = 0
            d[col] = 0

            for i in range(len(d)):
                c[row][i] = 0

            for i in range(len(s)):
                c[i][col] = 0

        # print(f"Select S{row+1} D{col+1} ({x[row][col]})")
        # print_matrix(s, d, x)

    return x


def russel(s, d, c):
    # Initialize the solution
    x = [[0 for _ in range(len(d))] for _ in range(len(s))]
    # Copy the variables
    s = s.copy()
    d = d.copy()
    c = [[v for v in row] for row in c]

    # Construct the solution
    while sum(s) != 0 and sum(d) != 0:
        # Find the largest unit cost in each row and column
        max_row = [0 for _ in range(len(s))]
        max_col = [0 for _ in range(len(d))]
        for row in range(len(s)):
            if s[row] == 0:
                continue
            for col in range(len(d)):
                if d[col] == 0:
                    continue
                if c[row][col] > max_row[row]:
                    max_row[row] = c[row][col]
                if c[row][col] > max_col[col]:
                    max_col[col] = c[row][col]

        # Find the largest difference
        max_diff = 0
        row = col = None
        for i in range(len(s)):
            if s[i] == 0:
                continue
            for j in range(len(d)):
                if d[j] == 0:
                    continue
                diff = c[i][j] - max_row[i] - max_col[j]
                if diff < max_diff:
                    max_diff = diff
                    row = i
                    col = j

        # Find the amount to be transported
        if s[row] < d[col]:
            x[row][col] = s[row]
            d[col] -= s[row]
            s[row] = 0
        elif s[row] > d[col]:
            x[row][col] = d[col]
            s[row] -= d[col]
            d[col] = 0
        else:
            x[row][col] = s[row]
            s[row] = 0
            d[col] = 0

        # print(f"Select S{row+1} D{col+1} ({x[row][col]})")
        # print_matrix(s, d, x)

    return x


def find_cost(c, x):
    cost = 0
    for row in range(len(x)):
        for col in range(len(x[0])):
            cost += x[row][col] * c[row][col]
    return cost


def print_matrix(s, d, c):
    print("\t\t|", end="")
    for col in range(len(d)):
        print(f"\tD{col + 1}", end="")
    print("\t| Supply")

    for col in range(len(d) + 5):
        print("----", end="")
    print()

    for row in range(len(s)):
        print(f"S{row + 1}", end="")
        print("\t\t|", end="")
        for col in range(len(d)):
            print(f"\t{c[row][col]}", end="")
        print(f"\t| {s[row]}")

    for col in range(len(d) + 5):
        print("----", end="")
    print()

    print("Demand\t|", end="")
    for col in range(len(d)):
        print(f"\t{d[col]}", end="")
    print(f"\t| {sum(d)}")


if __name__ == '__main__':
    main()
