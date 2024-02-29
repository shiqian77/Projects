function run_optimization_methods_rosenbrock(n_values, tol, max_iters, alpha_bar, rho, armijo_c, beta)
    compute_times = zeros(length(n_values), 1); 
    for j = 1:length(n_values)
        n = n_values(j);
        x0 = 10 * ones(n, 1); % Starting point with all entries equal to 10
        tol = 1e-6; 
    
        tic; 
    
        % Run Newton's Method with Hessian Modification (NMHM)
        [x_NM, ~, ~, ~, ~] = ...
            Newton_Hessian_Modifi(x0, tol, alpha_bar, rho, armijo_c, beta, @rosenbrock, max_iters);
        
        compute_times(j) = toc;
    
        % Display results for NMHM
        fprintf('For n = %d\n', n);
        fprintf('NMHM completed in %.2f seconds. It converges at x = [%s]\n', ...
                compute_times(j), sprintf('%f ', x_NM));
        
        % Break the loop if computation time exceeds 1 minute
        if compute_times(j) > 60
            fprintf('Computation time exceeded 1 minute for n = %d, stopping at this n value.\n', n);
            break;
        end
    end
    % Plot the compute times for NMHM
    figure;
    plot(n_values, compute_times, '-o');
    xlabel('Value of n');
    ylabel('Compute Time (seconds)');
    title('Compute Time for NMHM for Different Values of n');
    grid on;
end

function [f, g, H] = rosenbrock(x)
    n = length(x);
    f = 0;
    g = zeros(n, 1);
    H = zeros(n, n);
    
    for i = 1:n-1
        f = f + 100*(x(i+1) - x(i)^2)^2 + (1 - x(i))^2;
        g(i) = g(i) - 400*x(i)*(x(i+1) - x(i)^2) - 2*(1 - x(i));
        if i < n
            g(i+1) = g(i+1) + 200*(x(i+1) - x(i)^2);
        end
    end
    
    for i = 1:n
        if i < n
            H(i, i+1) = H(i, i+1) - 400*x(i);
            H(i+1, i) = H(i+1, i) - 400*x(i);
        end
        if i > 1 && i < n
            H(i, i) = 1200*x(i)^2 - 400*x(i+1) + 202;
        elseif i == 1
            H(i, i) = 1200*x(i)^2 - 400*x(i+1) + 2;
        elseif i == n
            H(i, i) = 200;
        end
    end
end

% Modify Hessian to be positive definite if necessary
function Hess_new = Chol_Added_Multiple_Identity(beta, H)
    n = size(H, 1); 
    tau = 0; 
    
    % Attempt Cholesky decomposition and modify Hessian if not positive definite
    [R, flag] = chol(H);
    while flag ~= 0
        tau = max(tau + beta, beta); % Increment tau to ensure positive definiteness
        [R, flag] = chol(H + tau * eye(n)); % Retry Cholesky decomposition
    end
    
    Hess_new = H + tau * eye(n); % Return modified Hessian
end

% Newton's method with modifications to the Hessian
function [x, s, kth_value, g, x_value] = Newton_Hessian_Modifi(x0_newton, tol, alpha_bar, rho, armijo_c, beta, rosenbrock, max_iters)
    x = x0_newton; % Start at the initial guess
    [evaluation, gradient, hessian] = rosenbrock(x);
    B = Chol_Added_Multiple_Identity(beta, hessian); % Modify Hessian to be positive definite
    B = sparse(B); % Convert to sparse matrix for efficiency
    p = B \ (-gradient); % Calculate the Newton direction
    s = 0; 
    kth_value = [evaluation]; 
    g = [norm(gradient)]; 
    x_value = [x]; 
    
    % Main loop for the Newton's method
    while norm(gradient) >= tol && s < max_iters
        alpha = BTLS(x, alpha_bar, rho, armijo_c, p, gradient, rosenbrock); % Find step size with backtracking line search
        x = x + alpha * p; 
        [evaluation, gradient, hessian] = rosenbrock(x); 
        B = Chol_Added_Multiple_Identity(beta, hessian); 
        B = sparse(B); 
        p = B \ (-gradient); 
        s = s + 1; 
        kth_value = [kth_value; evaluation]; 
        g = [g; norm(gradient)]; 
        x_value = [x_value; x]; 
    end
end

% Backtracking line search
function step = BTLS(x0, alpha_bar, rho, armijo_c, p, gradient, rosenbrock)
    alpha = alpha_bar; % Start with the initial step size
    [f0, ~] = rosenbrock(x0); % Get the function value at the initial point
    while true
        [f1, ~] = rosenbrock(x0 + alpha * p); % Get the function value at the new point
        if f1 > f0 + armijo_c * alpha * gradient' * p
            alpha = rho * alpha; % Reduce step size by factor of rho
        else
            break; 
        end
    end
    step = alpha; % Return the found step size
end
