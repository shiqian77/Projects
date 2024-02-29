"""
use this file to script the creation of plots, run experiments, print information etc.

Please put in comments and docstrings in to make your code readable
"""
from matlib import *
# Problem 0

if __name__ == '__main__':
# part A...
    '''
    matrix_sizes = [1000, 200, 400, 800, 1600]
    params = []
    for n in matrix_sizes:
        e_list = matrixandeigenvalue(n, 100,'a')
        # Plotting histogram
        hist_values, bin_edges, _ = plt.hist(e_list, bins=100, density=True, alpha=0.6, label='Empirical Data')
        # Guessing Gaussian distribution and getting fit parameters
        mu, std = norm.fit(e_list)
        params.append((mu, std))
        # Generating Gaussian fit data
        x_vals = np.linspace(min(e_list), max(e_list), 100)
        pdf = norm.pdf(x_vals, mu, std)
        # Plotting Gaussian fit
        plt.plot(x_vals, pdf, 'k', linewidth=2, label='Gaussian Fit')
        # Computing and plotting error
        error = hist_values - norm.pdf(bin_edges[:-1], mu, std)
        plt.plot(bin_edges[:-1], error, 'r', linewidth=2, label='Error')
        plt.legend()
        plt.xlabel(f'Eigenvalues (Matrix size: {n}x{n})')
        plt.ylabel('Probability Density')
        plt.title('Eigenvalue Distribution and Error')
        # Saving the plot
        filename = f'eigenvalue_distribution_{n}x{n}.png'
        plt.savefig(filename)
        print(f"Saved plot as {filename}")
  
        plt.clf()

    for n, (mu, std) in zip(matrix_sizes, params):
        print(f"For matrix size {n}x{n}: Mean (mu) = {mu:.2f}, Standard Deviation (std) = {std:.2f}")

# part B...
    e_list = matrixandeigenvalue(200, 1000, 'b')
    plt.hist(e_list, bins=100, density=True)
    plt.xlabel('Largest Eigenvalues')
    plt.ylabel('Probability Density')
    plt.title('Distribution of Largest Eigenvalues')
    plt.savefig('Largest_Eigenvalues_distribution.png')

# part C...
    e_list = matrixandeigenvalue(200, 1000, 'c')
    plt.hist(e_list, bins = 1000, density=True)
    plt.xlabel('largest gap between consecutive eigenvalues')
    plt.ylabel('Probability Density') 
    plt.title('Distribution of largest gap between consecutive eigenvalues')
    plt.savefig('largest_gap_between_consecutive_eigenvalues_distribution.png')
  
# part D...
    num = [200, 400, 800, 1600]
    for n in num:
        e_list = matrixandeigenvalue(n, 100, 'd')
        plt.hist(e_list, bins = 100, density=True)
        plt.xlabel('Singular values')
        plt.ylabel('Probability Density') 
        plt.title('eigenvalue distribution')
        # Saving the plot
        filename = f'singular_value_distribution_{n}x{n}.png'
        plt.savefig(filename)
        print(f"Saved plot as {filename}")
        plt.clf()

  
# part E...
    nn = [200,400,800,1600]
    for n in nn:
        e_list = matrixandeigenvalue(n, 100, 'e')
        plt.hist(e_list, bins = 100, density=True)
        plt.xlabel('Condition number')
        plt.ylabel('Probability Density') 
        plt.title(f'Condition Number Distribution for {n}x{n} Matrix')
        # Saving the plot
        filename = f'condition_number_distribution_{n}x{n}.png'
        plt.savefig(filename)
        print(f"Saved plot as {filename}")
        plt.clf()
'''

 

# Problem 1
    main()




# Problem 2
