function run_optimization_methods(initial_points, tol, max_iters, alpha_bar, rho, armijo_c, beta)
    % Suppress all warnings
    warning('off', 'all');

    % Iterate over each initial point
    for i = 1:size(initial_points, 1)
        x0 = initial_points(i, :)'; 

        % Run Newton's Method with Hessian Modification
        [x_NM, s_NM, kth_value_NM, g_NM, x_value_NM] = ...
            Newton_Hessian_Modifi(x0, tol, alpha_bar, rho, armijo_c, @fentonfgH, @fentonfgH, max_iters);

        % Run Vanilla Newton method
        [x_VN, iters_VN] = vanilla_newton(x0, @fentonfgH, tol, max_iters);

        % Display results
        fprintf('Initial point: [%d, %d]\n', initial_points(i, 1), initial_points(i, 2));
        fprintf('NMHM completed in %d iterations. It converges at x = [%f, %f]\n', ...
                s_NM, x_NM(1), x_NM(2));
        fprintf('VN completed in %d iterations. It converges at x = [%f, %f]\n\n', ...
                iters_VN, x_VN(1), x_VN(2));
    end
end


function [f, g, H] = fentonfgH(x)
    % Our goal fuction
    f = (12 + x(1)^2 + (1+x(2)^2)/x(1)^2 + (x(1)^2 * x(2)^2 + 100)/(x(1)*x(2))^4) / 10; 
    % Gradient of the fuction
    g = [
    (1/10)*(2*x(1) + 2*((-x(1)^2*x(2)^2 - 200)/(x(1)^5*x(2)^4)) - 2*((x(2)^2 + 1)/x(1)^3)); 
    (1/10)*(2*(x(1)^2*x(2)^6 - 200)/(x(1)^4*x(2)^5) - 2*(x(1)^2*x(2)^2)/(x(1)^4*x(2)^5))
];
    % Hessian matrix of the fuction
    H = [
    (1/10)*(6/(x(1)^4)*(x(2)^2+1) + 20/(x(1)^6*x(2)^4)*(x(1)^2*x(2)^2+100)),...
    (1/10)*((-14/(x(1)^4*x(2)^2) + 2/x(1)^2))
    (1/10)*((-4*x(2)/x(1)^3) - (12/(x(1)^3*x(2)^3)) + (16/(x(1)^5*x(2)^5))*(x(1)^2*x(2)^2+100)),...
    (1/10)*((20*(x(1)^2*x(2)^2+100))/(x(1)^4*x(2)^6) + 2/x(1)^2 - 14/(x(1)^2*x(2)^4))
];
end


% Function that modifies the Hessian matrix to ensure it is positive definite,by adding a multiple of the identity matrix if necessary.
function Hess_new = Chol_Added_Multiple_Identity(beta, H)
    n = size(H, 1); 
    tau = []; 
    m = min(diag(H)); 
    
    if m > 0
        tau(1) = 0; % If positive, no need to modify the Hessian
    else
        tau(1) = -m + beta; % Otherwise, set tau to make the Hessian positive definite
    end
    
    for k = 1:200
        [R, flag] = chol(H + tau(k) * eye(n)); % Perform Cholesky decomposition
        if flag ~= 0 % If Cholesky decomposition fails, Hessian is not positive definite
            tau(k+1) = max(2 * tau(k), beta); % Increase tau to make Hessian positive definite
        else
            break; 
        end
    end
    Hess_new = H + tau(k) * eye(n); % Return the modified Hessian matrix
end

% Newton's method with modifications to the Hessian
function [x, s, kth_value, g, x_value] = Newton_Hessian_Modifi(x0_newton, tol, alpha_bar, rho, armijo_c, f, fentonfgH, max_iters)
    x = x0_newton; % Start at the initial guess
    [evaluation, gradient, hessian] = fentonfgH(x);
    B = Chol_Added_Multiple_Identity(1e-3, hessian); % Modify Hessian to be positive definite
    B = sparse(B); % Convert to sparse matrix for efficiency
    p = B \ (-gradient); % Calculate the Newton direction
    s = 0; 
    kth_value = [evaluation]; 
    g = [norm(gradient)]; 
    x_value = [x]; 
    
    % Main loop for the Newton's method
    while norm(gradient) >= tol && s <= max_iters
        alpha = BTLS(x, alpha_bar, rho, armijo_c, p, gradient, f); % Find step size with backtracking line search
        x = x + alpha * p; 
        [evaluation, gradient, hessian] = fentonfgH(x); 
        B = Chol_Added_Multiple_Identity(1e-3, hessian); 
        B = sparse(B); 
        p = B \ (-gradient); 
        s = s + 1; 
        kth_value = [kth_value; evaluation]; 
        g = [g; norm(gradient)]; 
        x_value = [x_value; x]; 
    end
end

function step = BTLS(x0, alpha_bar, rho, armijo_c, p, gradient, f)
    alpha = alpha_bar; % Start with the initial step size
    % Continue to reduce step size until Armijo condition is met
    while f(x0 + alpha * p) > f(x0) + armijo_c * alpha * gradient' * p
        alpha = rho * alpha; % Reduce step size by factor of rho
    end
    step = alpha; % Return the found step size
end

% Vanilla Newton method implementation
function [x_new, num_iters] = vanilla_newton(x0, fgh, tol, max_iters)
    x = x0; % Start at the initial guess
    num_iters = 0; 
    
    while num_iters < max_iters
        [evaluation, gradient, hessian] = fentonfgH(x);
        % Check if the Hessian is singular (non-invertible)
        if det(hessian) == 0
            error('Hessian is singular at iteration %d.', num_iters); % Throw an error if singular
        end
        
        x_new = x - hessian\gradient; % Update the current point using the Newton's method formula
        
        % Check for convergence
        if norm(x_new - x, 'inf') < tol
            break; 
        end
        
        x = x_new; % Update x for the next iteration
        num_iters = num_iters + 1; 
    end
end