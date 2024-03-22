function [x_opt, lambda_opt, obj_val, is_sosc] = solve_prob(m, n, seed, p, gamma)
    rng(seed); % Set the random seed for reproducibility
    
    % Generate random problem data
    Q0 = diag(0.5 + rand(n, 1));
    c = 10 * rand(n, 1);
    A = rand(n, m); % Constraint matrix
    
    D = cell(m+1, 1);
    for j = 0:m
        dj = 2 * rand(n, 1) - 1;
        D{j+1} = diag(dj);
    end
    
    l = -ones(n, 1); % Lower bounds
    u = ones(n, 1); % Upper bounds
    
    x0 = zeros(n, 1); 
    lambda0 = ones(m, 1); % Initial Lagrange multipliers
    
    % Solve the bound-constrained Lagrangian problem
    [x_opt, lambda_opt] = bcl(x0, lambda0, l, u, gamma, Q0, c, A, D, p, m);
    
    % Calculate the objective value
    obj_val = obj_func(x_opt, gamma, Q0, c, D);
    
    % Calculate the Hessian of the Lagrangian at the solution
    hess = hess_lag(x_opt, lambda_opt, Q0, gamma, D, A, m);
    
    % Check if the second-order sufficient condition is satisfied
    is_sosc = pos_def_on_null_cholesky(hess, x_opt, A, gamma, D, m);
end