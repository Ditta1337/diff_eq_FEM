import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate

def e(x, i, h):
    if x < (i - 1) * h or x > (i + 1) * h:
        return 0
    elif x < i * h:
        return x / h - i + 1
    else:
        return -x / h + i + 1
    
def e_prim(x, i, h):
    if x < (i - 1) * h or x > (i + 1) * h:
        return 0
    elif x < i * h:
        return 1 / h
    else:
        return -1 / h
    
def phi_tilde(x, i, h):
    return 2 * x / 3 + 5

def phi_tilde_prim(x, i, h):
    return 2 / 3
    
def B(phi_prim, v_prim, i, j, h, lower, upper):
    return -integrate.quad(lambda x: phi_prim(x, i, h) * v_prim(x, j, h), lower, upper)[0]

def L(v, i, h, lower, upper):
    def rho(x):
        if x < 1 or x > 2:
            return 0
        else:
            return 1
        
    return 4 * np.pi * G * integrate.quad(lambda x: v(x, i, h) * rho(x), lower, upper)[0]

def get_B_matrix(num_elements, h):
    B_matrix = np.zeros((num_elements, num_elements))

    B_matrix[0][0] = 1
    B_matrix[num_elements - 1][num_elements - 1] = 1

    for i in range(1, num_elements - 1):
        for j in range(1, num_elements - 1):
            if i == j:
                upper = omega_max * max(0, (i - 1) / num_elements)
                lower = omega_max * min(1, (i + 1) / num_elements) 
                B_matrix[i][j] = B(e_prim, e_prim, i, j, h, lower, upper)
            elif i - j == 1 or i - j == -1:
                upper = omega_max * max(0, min(i, j) / num_elements)
                lower = omega_max * min(1, max(i, j) / num_elements) 
                B_matrix[i][j] = B(e_prim, e_prim, i, j, h, lower, upper)

                
    return B_matrix


def get_L_vector(num_elements, h):
    L_vector = np.zeros(num_elements)

    L_vector[0] = 5
    L_vector[num_elements - 1] = 7

    for i in range(1, num_elements - 1):
        upper = omega_max * max(0, (i - 1) / num_elements)
        lower = omega_max * min(1, (i + 1) / num_elements)
        L_vector[i] = L(e, i, h, lower, upper) - B(phi_tilde_prim, e_prim, i, i, h, lower, upper)
    
    return L_vector


def get_solution(num_elements):
    global G
    global omega_max

    # final function phi = phi1 * e1 + phi2 * e2 + ... + phin-1 * en-1 + phi_tilde
    def phi_final(x):
        result = 0
        for i in range(1, num_elements - 1):
            result += phi[i] * e(x, i, h)

        result += phi_tilde(x, -1, -1)
        return result
    
    omega_max = 3.
    G = 1
    h = omega_max / num_elements

    B_matrix = get_B_matrix(num_elements, h)
    L_vector = get_L_vector(num_elements, h)

    phi = np.linalg.solve(B_matrix, L_vector)
    x = np.linspace(0, omega_max, num_elements)
    y = [phi_final(x) for x in x]

    fig = plt.figure("Solution", figsize=(8, 5))
    plt.plot(x, y)
    plt.yticks(np.arange(int(min(y)) - 1, int(max(y)) + 1, 1))
    plt.xticks(np.arange(0, omega_max + 0.5, 0.5))
    plt.title("Gravitational potential $\phi(x)$\n Number of elements: " + str(num_elements))
    plt.ylabel("$\phi(x)$")
    plt.xlabel("Distance $x$")
    fig.savefig("solution.png")
    fig.show()



    




