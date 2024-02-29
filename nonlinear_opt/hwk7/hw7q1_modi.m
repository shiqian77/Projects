function hw7q1_modified()
    ms = [7, 10, 13, 15, 20];
    num_instances = 10;
    times = zeros(num_instances, length(ms));
    
    for idx = 1:length(ms)
        m = ms(idx);
        n = 2 * m;
        
        for instance = 1:num_instances
            rng(instance);
            
            A = randn(m, n);
            e = ones(n, 1);
            b = A * e;
            u = rand(n, 1);
            c = e + 100 * u;
            
            x0 = e;
            lambda0 = zeros(m, 1);
            s0 = c - A' * lambda0;
            
            try
                tic;
                [x, lambd, s] = long_step_interior_point(A, b, c, x0, lambda0, s0, 0.5, 1e-8, 100);
                times(instance, idx) = toc;
            catch exception
                fprintf('Error at m=%d, instance=%d: %s\n', m, instance, exception.message);
                times(instance, idx) = NaN;
            end  % This 'end' closes the 'try' block
        end
    end
    
    % Use mean and isnan functions instead of nanmean which might not be available in some MATLAB versions
    mean_times = zeros(1, length(ms));
    std_dev_times = zeros(1, length(ms));
    
    for idx = 1:length(ms)
        valid_times = times(~isnan(times(:, idx)), idx);  % Filter out NaN values
        mean_times(idx) = mean(valid_times);
        std_dev_times(idx) = std(valid_times);
    end
    
    for idx = 1:length(ms)
        fprintf('m = %d: mean time = %.6f s, std dev = %.6f s\n', ms(idx), mean_times(idx), std_dev_times(idx));
    end
end

function [x, lambd, s] = long_step_interior_point(A, b, c, x0, lambda0, s0, gamma, tol, max_iter)
    [m, n] = size(A);
    x = x0;
    lambd = lambda0;
    s = s0;
    
    for i = 1:max_iter
        % Compute residuals

        r_b = A * x - b;
        r_c = A' * lambd + s - c;
        r_xs = x .* s;  % Elementwise multiplication
        
        % Compute the centering parameter
        mu = sum(r_xs) / n;
        
        % Compute right-hand side
        % delta_xs = -r_xs + gamma * mu;

        % Compute right-hand side
        delta_xs = -x .* s + gamma * mu * ones(n, 1);
        
        
        % Solve for direction
        [delta_x, delta_lambda, delta_s] = solve_direction(A, x, s, r_b, r_c, delta_xs);
        
        % Compute step length
        alpha_x = min(-x(delta_x < 0) ./ delta_x(delta_x < 0));  % Correct element-wise division
        alpha_s = min(-s(delta_s < 0) ./ delta_s(delta_s < 0));  % Correct element-wise division
        alpha = min(1, 0.9 * min(alpha_x, alpha_s));
        
        % Update variables
        x = x + alpha * delta_x;
        lambd = lambd + alpha * delta_lambda;
        s = s + alpha * delta_s;
        
        % Check convergence
        if norm(r_b) < tol && norm(r_c) < tol && mu < tol
            break;
        end
    end
end

function [delta_x, delta_lambda, delta_s] = solve_direction(A, x, s, r_b, r_c, delta_xs)
    [m, n] = size(A);

    % Create block matrix for KKT conditions
    M = [zeros(n, n), A', eye(n); A, zeros(m, m), zeros(m, n); diag(s), zeros(n, m), diag(x)];

    % Solve for direction
    rhs = [-r_c; -r_b; -delta_xs];

    direction = M \ rhs;

    % Extract directions
    delta_x = direction(1:n);
    delta_lambda = direction(n+1:n+m);
    delta_s = direction(n+m+1:end);
end