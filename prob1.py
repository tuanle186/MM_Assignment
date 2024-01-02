import pandas as pd
import numpy as np
import os

# -------------------------------------------------------------------------------------------------------
def main():
    unit_preorder_cost, unit_prod_cost, unit_price, salvage_cost, a_matrix, demand, scenario_probability = get_user_input()
    unit_preorder_cost, unit_prod_cost, unit_price, salvage_cost, a_matrix, demand, scenario_probability = data_double_check(unit_preorder_cost, unit_prod_cost, unit_price, salvage_cost, a_matrix, demand, scenario_probability)
    clearTerminal()
    problem_1, x, y, z = solve_model(unit_preorder_cost, unit_prod_cost, unit_price, salvage_cost, a_matrix, demand, scenario_probability)
    show_results(problem_1, x, y, z)
    
    
# -------------------------------------------------------------------------------------------------------
''' This section consists of functions to get user input and process input data
'''
number_of_parts = 0
number_of_products = 0
def get_m_and_n():
    ''' Function to get user's data for the number of
        parts (m) and products (n)
    '''

    global number_of_parts, number_of_products
    while True:
        try:
            number_of_parts = int(input("Number of parts (m): "))
            number_of_products = int(input("Number of products (n): "))
            break;
        except ValueError: # Error handling
            print("Invalid input. Please enter an integer.\n")


def get_b():
    ''' Function to get user's data for unit pre-order cost vector (b)
    '''

    print("------------- PRE-ODER COST (b) -------------")
    unit_preorder_cost = []
    for i in range(1, number_of_parts + 1):
        while True:
            try:
                unit_preorder_cost.append(float(input(f"Preorder cost (b) of part {i}: ")))
                break
            except ValueError:
                print("Invalid input. Please enter an integer or a float.\n")
    return pd.DataFrame({'b': unit_preorder_cost})


def get_s():
    ''' Function to get user's data for salvage cost vector (s)
    '''

    print("------------- SALVAGE COST (s) --------------")
    salvage_cost = []
    for i in range(1, number_of_parts + 1):
        while True:
            try:
                salvage_cost.append(float(input(f"Salvage cost (s) of part {i}: ")))
                break
            except ValueError:
                print("Invalid input. Please enter an integer or a float.\n")
    return pd.DataFrame({'s': salvage_cost})


def get_l():
    ''' Function to get user's data for unit production cost vector (l)
    '''

    print("---------- UNIT PRODUCTION COST (l) ---------")
    unit_prod_cost = []
    for i in range(1, number_of_products + 1):
        while True:
            try:
                unit_prod_cost.append(float(input(f"Unit production (l) cost of product {i}: ")))
                break
            except ValueError:
                print("Invalid input. Please enter an integer or a float.\n")
    return pd.DataFrame({'l': unit_prod_cost})


def get_q():
    ''' Function to get user's data for unit price vector (q)
    '''

    print("-------------- UNIT PRICE (q) ---------------")
    unit_price = []
    for i in range(1, number_of_products + 1):
        while True:
            try:
                unit_price.append(int(input(f"Unit price (a) of product {i}: ")))
                break
            except ValueError:
                print("Invalid input. Please enter an integer or a float.\n")
    return pd.DataFrame({'q': unit_price})


import tkinter as tk
def get_a():
    print("---------- NUMBER OF PARTS NEEDED FOR PRODUCTION (a) ----------")
    print("Please enter matrix a in the pop-up window")
    global number_of_products
    global number_of_parts

    window = tk.Tk()

    for c in range(number_of_parts):
        l = tk.Label(window, text="Part " + str(c+1))
        l.grid(row=0, column=c+1)

    all_entries = []
    for r in range(number_of_products):
        entries_row = []
        l = tk.Label(window, text="Product " + str(r+1))
        l.grid(row=r+1, column=0)
        for c in range(number_of_parts):
            e = tk.Entry(window, width=5)  # 5 chars
            e.insert('end', 0)
            e.grid(row=r+1, column=c+1)
            entries_row.append(e)
        all_entries.append(entries_row)

    a_matrix = []
    b = tk.Button(window, text='OK', command=lambda: get_data_a(all_entries, a_matrix, window))
    b.grid(row=number_of_products+1, column=0, columnspan=number_of_parts)
    window.mainloop()
    df = pd.DataFrame(np.array(a_matrix))
    df.index.name = 'Product'
    df.columns.name = 'Part'
    print(df)
    return df
    
    
def get_data_a(all_entries, data, window):
    for r, row in enumerate(all_entries):
        row_data = []
        for c, entry in enumerate(row):
            text = entry.get()
            row_data.append(int(text))
        data.append(row_data)
    window.destroy()
    return data


def get_is_stochastic():
    # Get user's choice: stochastic or deterministic ------------------------------------
    print("----------------------- Stage-2 demand (d) ----------------------")
    while True:
        try:
            is_stochastic = input("Is the demand of product stochastic [s] or deterministic [d]? ")
            if is_stochastic != 'd' and is_stochastic != 's':
                raise ValueError
            else:
                is_stochastic = is_stochastic == 's'
            break
        except ValueError:
            print("Invalid input. Please enter valid value ([s] or [d]).\n")
    return is_stochastic


def get_number_of_scenarios():
    ''' Function to get the number of scenarios of stage 2
    '''
    while True:
        try:
            n_scenarios = int(input("Number of scenarios: "))
            break
        except ValueError:
            print("Invalid input. Please enter an integer.\n")
    return n_scenarios


def get_deterministic_d(n_scenarios):
    demand = []
    scenario_probability = []
    for i in range(1, n_scenarios + 1):
        print("------------------------------------")
        print(f"Scenario {i}")
        d_row = []
        for j in range (1, number_of_products + 1):
            while True:
                try:
                    d_row.append(int(input(f"Demand (d) of product {j}: ")))
                    break;
                except ValueError:
                    print("Invalid input. Please enter an integer.\n")
        
        while True:
            try:
                p_tmp = float(input("Scenario probability of happening: "))
                if p_tmp < 0 or p_tmp > 1:
                    raise ValueError
                scenario_probability.append(p_tmp)
                break
            except ValueError:
                print("Invalid input. Please enter valid value for probability (float, 0 < p < 1).\n")
        demand.append(d_row)

    demand_df = pd.DataFrame(np.array(demand))
    demand_df.index.name = 'Scenario'
    demand_df.columns.name = 'Product'

    scenario_probability_df = pd.DataFrame({'(p)': scenario_probability})
    scenario_probability_df.index.name = "Scenario"
    scenario_probability_df.columns.name = "Probability"

    return demand_df, scenario_probability_df


def get_stochastic_d(n_scenarios):
    print("Choose a probability distribution for each scenario \n - [b] Binomial \n - [n] Normal \n - [p] Poisson \n - [e] Exponential \n - [u] Uniform \n - [g] Gamma")
    demand = []
    scenario_probability = []
    for i in range(1, n_scenarios + 1):
        print("------------------------------------")
        print(f"- Scenario {i}")
        d_row = []
        while True:
            dis_choice = input("Distribution: ")
            if dis_choice == 'b':  # Binomial
                try:
                    n_trials = int(input("Number of trials: "))
                    probability = float(input("Probability of success: "))
                    d_row = np.random.binomial(n_trials, probability, size=number_of_products)
                    break
                except ValueError:
                    print("Invalid input. Please enter valid values.\n")

            elif dis_choice == 'n':  # Normal
                try:
                    mean = float(input("Mean value (float): "))
                    std_dev = float(input("Standard deviation (float): "))
                    d_row = np.random.normal(mean, std_dev, size=number_of_products)
                    break
                except ValueError:
                    print("Invalid input. Please enter valid values.\n")

            elif dis_choice == 'p':  # Poisson
                try:
                    lambda_param = float(input("Lambda parameter: "))
                    d_row = np.random.poisson(lambda_param, size=number_of_products)
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid value.\n")

            elif dis_choice == 'u':  # Uniform
                try:
                    lower_bound = float(input("Lower bound: "))
                    upper_bound = float(input("Upper bound: "))
                    d_row = np.random.uniform(lower_bound, upper_bound, size=number_of_products)
                    break
                except ValueError:
                    print("Invalid input. Please enter valid values.\n")

            elif dis_choice == 'g':  # Gamma
                try:
                    shape_param = float(input("Shape parameter (a or k): "))
                    scale_param = float(input("Scale parameter (b or 1/θ): "))
                    d_row = np.random.gamma(shape_param, scale_param, size=number_of_products)
                    break
                except ValueError:
                    print("Invalid input. Please enter valid values.\n")

            else:
                print("Invalid distribution choice, please choose again.\n")
        
        # Get the probability of happening of each scenario -------------------------
        while True:
            try:
                p_tmp = float(input("Scenario probability of happening: "))
                if p_tmp < 0 or p_tmp > 1:
                    raise ValueError
                scenario_probability.append(p_tmp)
                break
            except ValueError:
                print("Invalid input. Please enter valid value for probability (float, 0 < p < 1).\n")
        
        demand.append(d_row)

    demand_df = pd.DataFrame(np.array(demand))
    demand_df.index.name = 'Scenario'
    demand_df.columns.name = 'Product'

    scenario_probability_df = pd.DataFrame({'(p)': scenario_probability})
    scenario_probability_df.index.name = "Scenario"
    scenario_probability_df.columns.name = "Probability"
    return demand_df, scenario_probability_df


def get_d():
    is_stochastic = get_is_stochastic()
    n_scenarios = get_number_of_scenarios()
    demand = []
    scenario_probability = []
    if is_stochastic: 
        demand, scenario_probability = get_stochastic_d(n_scenarios)
    else:
        demand, scenario_probability = get_deterministic_d(n_scenarios)
    return demand, scenario_probability


def get_user_input():
    clearTerminal()
    get_m_and_n()
    print()
    unit_preorder_cost = get_b()
    print()
    salvage_cost = get_s()
    print()
    unit_production_cost = get_l()
    print()
    unit_price = get_q()
    print()
    a_matrix = get_a()
    print()
    demand, scenario_probability = get_d()
    return unit_preorder_cost, unit_production_cost, unit_price, salvage_cost, a_matrix, demand, scenario_probability


# -------------------------------------------------------------------------------------------------------
def data_double_check(unit_preorder_cost, unit_prod_cost, unit_price, salvage_cost, a_matrix, demand, scenario_probability):
    ''' Function that allows user to double check and edit data
    '''

    input_data = ''
    while input_data != 'ok':
        clearTerminal()
        print("PLEASE DOUBLE CHECK YOUR DATA: ")
        print("-------------------------------------------------")
        print("Unit preorder cost (b):")
        print(unit_preorder_cost)
        print('Enter [b] to edit')

        print("-------------------------------------------------")
        print("Unit production cost (l):")
        print(unit_prod_cost)
        print('Enter [l] to edit')

        print("-------------------------------------------------")
        print("Unit price (q):")
        print(unit_price)
        print('Enter [q] to edit')

        print("-------------------------------------------------")
        print("Salvalge cost (s):")
        print(salvage_cost)
        print('Enter [s] to edit')

        print("-------------------------------------------------")
        print("Number of parts needed for each product (A):")
        print(a_matrix)
        print('Enter [a] to edit')

        print("-------------------------------------------------")
        print("Stage-2 demand (d):")
        print(demand)
        print()
        print("Scenario probabilities (p):")
        print(scenario_probability)
        print()
        print('Enter [d] to edit')

        print("-------------------------------------------------")
        input_data = input("Or press [ok] to solve: ")
        clearTerminal()
        if input_data == 'b':
            unit_preorder_cost = get_b()
        elif input_data == 'l':
            unit_prod_cost = get_l()
        elif input_data == 'q':
            unit_price = get_q()
        elif input_data == 's':
            salvage_cost = get_s()
        elif input_data == 'a':
            a_matrix = get_a()
        elif input_data == 'd':
            demand, scenario_probability = get_d()
        else:
            return unit_preorder_cost, unit_prod_cost, unit_price, salvage_cost, a_matrix, demand, scenario_probability


# -------------------------------------------------------------------------------------------------------
def solve_model(unit_preorder_cost, unit_prod_cost, unit_price, salvage_cost, a_matrix, demand, scenario_probability):
    from gamspy import Container, Set, Parameter, Variable, Equation, Model, Sum, Sense
    number_of_products = unit_prod_cost.shape[0]
    number_of_parts = unit_preorder_cost.shape[0]
    number_of_scenarios = scenario_probability.shape[0]
    products = []
    for i in range(1, number_of_products + 1):
        products.append(f'product {i}')
    parts = []
    for i in range(1, number_of_parts + 1):
        parts.append(f'parts {i}')
    scenarios = []
    for i in range(1, number_of_scenarios + 1):
        scenarios.append(f'scenario {i}')
    m = Container()

    i = Set(
        container=m,
        name="products",
        records=np.array(products),
        description="Products domain",
    )

    j = Set(
        container=m,
        name="parts",
        records=np.array(parts),
        description="Parts domain",
    )

    k = Set(
        container=m,
        name="scenarios",
        records=np.array(scenarios),
        description="scenarios domain"
    )

    b = Parameter(
        container=m,
        name="b",
        domain=j,
        records=np.array(unit_preorder_cost),
    )

    l = Parameter(
        container=m,
        name="l",
        domain=i,
        records=np.array(unit_prod_cost),
    )

    q = Parameter(
        container=m,
        name="q",
        domain=i,
        records=np.array(unit_price),
    )

    s = Parameter(
        container=m,
        name="s",
        domain=j,
        records=np.array(salvage_cost),
    )

    A = Parameter(
        container=m,
        name="A",
        domain=[i,j],
        records=np.array(a_matrix),
    )

    d = Parameter(
        container=m,
        name="d",
        domain=[k, i],
        records=np.array(demand)
    )

    p = Parameter(
        container=m,
        name="p",
        domain=[k],
        records=np.array(scenario_probability)
    )

    x = Variable(
        container=m,
        name="x",
        type="integer",
        domain=j,
    )

    y = Variable(
        container=m,
        name="y",
        type="integer",
        domain=[k, j]
    )

    z = Variable(
        container=m,
        name="z",
        type="integer",
        domain=[k, i]
    )
    obj = Sum(j, b[j]*x[j]) + Sum(k, p[k]*(Sum(i, (l[i] - q[i])*z[k, i]) - Sum(j, s[j]*y[k, j])))
    demand_constraint = Equation(
        container=m,
        name="demand_constraint",
        domain=[k, i]
    )

    relationship = Equation(
        container=m,
        name="relationship",
        domain=[k, j]
    )

    demand_constraint[k, i] = 0 <= z[k, i] <= d[k, i]
    relationship[k, j] = y[k, j] == x[j] - Sum(i, A[i, j]*z[k, i])

    problem_1 = Model(
        container=m,
        name="problem_1",
        equations=m.getEquations(),
        problem="MIP",
        sense=Sense.MIN,
        objective=obj,
    )

    viewSolverconsole = input("View solver's console [y/n]? ")
    clearTerminal()
    if viewSolverconsole == 'y':
        import sys
        problem_1.solve(output=sys.stdout)
        input("Press enter to show result summary")
        print("-------------------------------------------------------------------------")
    else:
        problem_1.solve()
    return problem_1, x,  y, z


# -------------------------------------------------------------------------------------------------------
def show_results(problem_1, x, y, z):
    print("Objective value = ", problem_1.objective_value)
    print("-------------------------------------------------------------------------")
    print("The numbers of parts to be ordered before production (x) - here-and-now")
    print(x.records)
    print("-------------------------------------------------------------------------")
    print("The numbers of parts left in inventory (y) - wait-and-see")
    print(y.records)
    print("-------------------------------------------------------------------------")
    print("The number of units to be produced (z) - wait-and-see")
    print(z.records)
    return 0
# -------------------------------------------------------------------------------------------------------
def clearTerminal():
    os.system('cls' if os.name == 'nt' else 'clear')


# -------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()