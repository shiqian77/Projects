function [x_opt, lambda_opt] = bcl(x0, lambda0, l, u, gamma, Q0, c, A, D, p, m)
    mu = 10; % Initial penalty parameter
    omega = 1 / mu; % Initial omega tolerance
    eta = 1 / mu; % Initial eta tolerance

    x = x0; 
    lambda = lambda0; % Initial multipliers

    k = 1; 
    while k <= p
        % Define the augmented Lagrangian function for the current iteration
        aug_lag_func = @(x) calculate_objectives(x, gamma, Q0, c, A, lambda, mu, D);

        % Solve the bound-constrained subproblem using fmincon
        [x_k, ~] = fmincon(aug_lag_func, x, [], [], [], [], l, u, [], optimoptions('fmincon', 'Algorithm', 'sqp', 'Display', 'off'));

        % Projection onto the feasible region (assuming this is what P refers to)
        x_proj = proj(x_k - grad_aug_lag(x_k, gamma, Q0, c, A, lambda, mu, D), l, u);

        % Test for convergence
        if norm(A' * x_k) <= eta && norm(x_k - x_proj) <= omega
            % Convergence achieved
            x_opt = x_k;
            lambda_opt = lambda;
            return;
        end

        % Update multipliers and tighten tolerances if the conditions are met
        if norm(A' * x_k) <= eta
            lambda = lambda - mu * (A' * x_k);
            mu = mu * 0.9; % Reduce mu to a smaller value
            eta = eta / mu;
            omega = omega / mu;
        else
            % Increase penalty parameter and tighten tolerances
            mu = 100 * mu; % Increase mu
            eta = 1 / mu;
            omega = 1 / mu;
        end

        x = x_k; % Update x for the next iteration
        k = k + 1; 
    end

    % If the function reaches here, the maximum number of iterations was reached
    x_opt = x;
    lambda_opt = lambda;
end