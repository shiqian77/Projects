function compare_methods(n_values, max_iters, alpha_bar, rho, armijo_c, beta)
    dogleg_linear_solves = [];
    dogleg_times = [];
    nwhm_linear_solves = [];
    nwhm_times = [];
    
    for i = 1:length(n_values)
        n = n_values(i);
        x0 = 2 * ones(n, 1); 

        % Calculate the stopping criterion based on the initial gradient
        [~, g_initial, ~] = rosenbrock(x0);
        tol = min(1e-3, norm(g_initial) / 100);  % Stopping criterion
        
        % Run Dogleg Trust-Region method
        t1=tic;
        [~, ~, dogleg_linear_solve_count] = dogleg_trust_region(@rosenbrock, x0, max_iters, tol);
        dogleg_times(end+1) = toc(t1);
        dogleg_linear_solves(end+1) = dogleg_linear_solve_count;
        
        % Run Newton's Method with Hessian Modification
        t1 = tic;
        [~, ~, nwhm_linear_solve_count] = run_optimization_methods_rosenbrock(x0, tol, max_iters, alpha_bar, rho, armijo_c, beta);
        nwhm_times(end+1) = toc(t1);
        nwhm_linear_solves(end+1) = nwhm_linear_solve_count;
    end

    
    % Plot for the number of linear systems solved
    figure;
    plot(n_values, dogleg_linear_solves, 'b-o', n_values, nwhm_linear_solves, 'r-x');
    title('Comparison of Linear Systems Solved');
    xlabel('Dimension (n)');
    ylabel('Number of Linear Systems Solved');
    legend('Dogleg Trust-Region', 'NWHM');
    grid on;
    
    % Plot for the computation times
    figure;
    plot(n_values, dogleg_times, 'b-o', n_values, nwhm_times, 'r-x');
    title('Comparison of Computation Times');
    xlabel('Dimension (n)');
    ylabel('Computation Time (seconds)');
    legend('Dogleg Trust-Region', 'NWHM');
    grid on;

end

function [x_opt, num_linear_solves, num_func_evals] = dogleg_trust_region(rosenbrock, x0, max_iter, tol)
 
    delta_hat = 10; 
    xk = x0;
    delta = 2;
    eta = 0.1;
    num_linear_solves = 0;
    num_func_evals = 0;
    
    [fk, gk, Hk] = rosenbrock(xk);
    num_func_evals = num_func_evals + 1;

    k = 0; 
    % Convert Hessian to sparse format and solve the linear system
    while k < max_iter && norm(gk, 2) > tol
        k = k + 1; 
        Hk = sparse(double(Hk)); 
        pk = -Hk\gk;  
        num_linear_solves = num_linear_solves + 1;
        
        %  Compute the scaled gradient
        gkHk = gk' * Hk * gk;
        if gkHk <= 0
            tau = 1;
        else
            tau = min(norm(gk)^3 / (delta * gkHk), 1);
        end
        pu = -tau * (delta / norm(gk)) * gk;
        
        % Compute the dogleg path combining Newton and gradient steps
        p = compute_dogleg_path(pk, pu, delta);
        
        % Update the solution estimate
        x_new = xk + p;
        [fk_new, gk_new, Hk_new] = rosenbrock(x_new);
        num_func_evals = num_func_evals + 1;

        % Update the solution if the step is accepted
        rho_k = (fk - fk_new) / (-gk'*p - 0.5*p'*Hk*p);
        
        % Update the trust region radius based on the ratio
        if rho_k > 3/4 && norm(p) == delta
            delta = min(2*delta, delta_hat);
        elseif rho_k < 1/4
            delta = 1/4 * delta;
        end

        if rho_k > eta
            xk = x_new;
            fk = fk_new;
            gk = gk_new;
            Hk = Hk_new;
        end
    end
    
    % return the optimal solution 
    x_opt = xk;
end

% Determine whether to use the Newton step or a combination of gradient and Newton steps
function p = compute_dogleg_path(pk, pu, delta)
    % If Newton step is outside the trust region, use a combination
    if norm(pk) > delta
        pb = pu + (delta - norm(pu)) * (pk - pu) / norm(pk - pu);
        p = pb;
    else
         % If Newton step is inside the trust region, use it directly
        p = pk;
    end
end



function [f, g, H] = rosenbrock(x0)
    syms x [1 length(x0)];
    f_sym = 0;
    for i = 1:(length(x) - 1)
        f_sym = f_sym + 100*(x(i+1) - x(i)^2)^2 + (1 - x(i))^2;
    end

    grad_sym = gradient(f_sym, x);
    Hess_sym = hessian(f_sym, x);

    f = double(vpa(subs(f_sym, x, x0'), 15));
    g = double(vpa(subs(grad_sym, x, x0'), 15));
    H = double(vpa(subs(Hess_sym, x, x0'), 15));
end

function [x, fval, num_iters, num_linear_solves] = run_optimization_methods_rosenbrock(x0, tol, max_iters, alpha_bar, rho, armijo_c, beta)
    num_iters = 0;
    num_linear_solves = 0;
    x = x0;
    [fval, grad, H] = rosenbrock(x);
    
    while norm(grad) > tol && num_iters < max_iters
        H_modified = Chol_Added_Multiple_Identity(beta, H);
        p = -H_modified \ grad;
        num_linear_solves = num_linear_solves + 1; % Increment the linear solve counter
        
        alpha = BTLS(x, alpha_bar, rho, armijo_c, p, grad, @rosenbrock);
        x = x + alpha * p;
        [fval, grad, H] = rosenbrock(x);
        
        num_iters = num_iters + 1;
    end
end

% Modify Hessian to be positive definite if necessary
function H_modified = Chol_Added_Multiple_Identity(beta, H)
    n = size(H, 1);
    tau = 0;
    % Attempt Cholesky decomposition
    [R, flag] = chol(H);
    while flag ~= 0
        tau = max(tau + beta, beta);
        [R, flag] = chol(H + tau * eye(n));
    end
    H_modified = H + tau * eye(n);
end

% Backtracking line search function
function alpha = BTLS(x, alpha_bar, rho, c, p, grad, rosenbrock)
    alpha = alpha_bar;
    [fx, ~] = rosenbrock(x);
    [fx_new, ~] = rosenbrock(x + alpha * p);
    while fx_new > fx + c * alpha * grad' * p
        alpha = rho * alpha;
        [fx_new, ~] = rosenbrock(x + alpha * p);
    end
end



