function [x] = hwk4p1(x0, niter, eps)
    tol = eps; 
    max_iters = niter; 
    delta_hat = 5;        
    delta_0 = 1;          
    eta = 0.1;            
    alpha_bar = 1;        
    rho = 0.9;            
    armijo_c = 1e-4;      
    beta = 0.5;    
    %compare_methods(n_values, max_iters, alpha_bar, rho, armijo_c, beta);
    [x_opt, num_linear_solves, num_func_evals] = dogleg_trust_region(@rosenbrock, x0, max_iters, tol);
    x = x_opt;
end
