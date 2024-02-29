function compare_methods()
    ms = [7, 9, 11,13, 15, 17, 19, 21, 23, 25];
    num_instances = 10;
    max_steps = 100;

    mean_times_simplex = zeros(length(ms), 1);
    mean_times_interior_point = zeros(length(ms), 1);

    for idx = 1:length(ms)
        m = ms(idx);
        n = 2 * m;
        times_simplex = zeros(num_instances, 1);
        times_interior_point = zeros(num_instances, 1);

        for instance = 1:num_instances
            rng(instance);
            A = randn(m, n);
            e = ones(n, 1);
            b = A * e;
            u = rand(n, 1);
            c = e + 100 * u;

            % Run simplex method
            [~, elapsed_time_simplex, ~, ~] = run_simplex(A, b, c, m, n, max_steps);
            times_simplex(instance) = elapsed_time_simplex;

            % Run long step interior point method
            x0 = e;
            lambda0 = zeros(m, 1);
            s0 = c - A' * lambda0;
            [~, elapsed_time_interior_point, ~] = long_step_interior_point(A, b, c, x0, lambda0, s0, 0.5, 1e-8, 100);
            times_interior_point(instance) = elapsed_time_interior_point;
        end

        % Compute mean times for each method
        mean_times_simplex(idx) = mean(times_simplex);
        mean_times_interior_point(idx) = mean(times_interior_point);
    end

    % Plot the results
    figure;
    plot(ms, mean_times_simplex, '-o', 'DisplayName', 'Simplex Method');
    hold on;
    plot(ms, mean_times_interior_point, '-x', 'DisplayName', 'Long Step Interior Point Method');
    hold off;
    xlabel('Problem Size (m)');
    ylabel('Mean Time to Solution (s)');
    title('Comparison of Simplex and Long Step Interior Point Methods');
    legend;
end

function [x, elapsed_time, is_optimal] = long_step_interior_point(A, b, c, x0, lambda0, s0, gamma, tol, max_iter)
    tic;  
    [m, n] = size(A);
    x = x0;
    lambd = lambda0;
    s = s0;
    is_optimal = false;

    for i = 1:max_iter
        % Compute residuals
        r_b = A * x - b;
        r_c = A' * lambd + s - c;
        r_xs = x .* s;  

        mu = sum(r_xs) / n;

        delta_xs = -x .* s + gamma * mu * ones(n, 1);

        % Solve for direction
        [delta_x, delta_lambda, delta_s] = solve_direction(A, x, s, r_b, r_c, delta_xs);

        % Compute step length
        alpha_x = min(-x(delta_x < 0) ./ delta_x(delta_x < 0));  
        alpha_s = min(-s(delta_s < 0) ./ delta_s(delta_s < 0));  
        alpha = min(1, 0.9 * min(alpha_x, alpha_s));

        x = x + alpha * delta_x;
        lambd = lambd + alpha * delta_lambda;
        s = s + alpha * delta_s;

        % Check convergence
        if norm(r_b) < tol && norm(r_c) < tol && mu < tol
            is_optimal = true;
            break;
        end
    end

    elapsed_time = toc;  
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


function [x, elapsed_time, is_optimal, is_degenerate] = run_simplex(A, b, c, m, n, max_steps)
    B_indices = 1:m;
    N_indices = (m+1):n;
    B = A(:, B_indices);
    N = A(:, N_indices);
    cB = c(B_indices);
    cN = c(N_indices);
    xB = B \ b;
    is_optimal = false;
    elapsed_time = 0;
    is_degenerate = false;

    tic;
    step_count = 0;
    while step_count < max_steps
        [p, q, is_optimal, is_unbounded, is_degenerate] = simplex_step(B, N, cB, cN, xB);
        
        % break if optimal solution is found or problem is unbounded
        if is_optimal || is_unbounded || is_degenerate
            break;
        end
        
        % update matrices B and N, and cost vectors cB and cN
        entering = N_indices(q);
        leaving = B_indices(p);
        B(:, p) = N(:, q);
        N(:, q) = full(sparse(p, 1, 1, m, 1));  
        B_indices(p) = entering;
        N_indices(q) = leaving;
        cB(p) = cN(q);
        cN(q) = c(leaving);
        xB = B \ b;
        
        % increment step count
        step_count = step_count + 1;
    end

    elapsed_time = toc;

    % construct the full solution vector
    x = zeros(n, 1);
    x(B_indices) = xB;

    % if the maximum number of steps was reached without finding an optimal solution
    if step_count >= max_steps
        disp('Maximum number of steps reached without finding an optimal solution.');
        is_optimal = false;
    end
end

function [p, q, is_optimal, is_unbounded, is_degenerate] = simplex_step(B, N, cB, cN, xB)
    is_degenerate = false;  % initialize the flag for degeneracy
    lambda = B' \ cB;       % compute dual variables
    sN = cN - (N' * lambda); % compute reduced costs

    if all(sN >= 0)         % if all reduced costs are non-negative, we're done
        p = -1; q = -1; is_optimal = true; is_unbounded = false;
        return;
    end

    [min_sN, q] = min(sN);  
    Aq = N(:, q);     
    dq = B \ Aq;           

    if all(dq <= 0)         
        p = -1; q = -1; is_optimal = false; is_unbounded = true;
        return;
    end

    theta = xB ./ dq;       % maximum step we can take in the direction dq
    theta(dq <= 0) = Inf;   % set it to Inf where dq is non-positive to avoid division by zero
    [min_theta, p] = min(theta); 

    % check for degeneracy that if there's more than one minimum theta, it's degenerate
    is_degenerate = sum(theta == min_theta) > 1;

    if ~is_degenerate       % If not degenerate, perform the pivot
        xB = xB - dq * min_theta; 
        xB(p) = min_theta;    
        is_optimal = false;       % haven't yet checked optimality
        is_unbounded = false;     % haven't yet checked unboundedness
    else
        % if degenerate, do not pivot; report back to the calling function
        is_optimal = false;
        is_unbounded = false;
    end
end



