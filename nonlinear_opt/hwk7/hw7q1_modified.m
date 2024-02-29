ms = [8, 10, 13];

for idx = 1:length(ms)
    m = ms(idx);
    n = 2 * m;
    rng(idx); 
    A = randn(m, n);
    b = rand(m, 1);
    c = rand(n, 1);

    % Solve the LP problem using the simplex method
    [x_feasible, x_opt, elapsed_time, is_optimal] = solve_lp_with_simplex(A, b, c);

    % Display results
    fprintf('Problem size m = %d, n = %d:\n', m, n);
    fprintf('Simplex Method:\n');
    if is_optimal
        fprintf('Optimal solution found in %.4f seconds.\n', elapsed_time);
        disp('Feasible solution:');
        disp(x_feasible);
        disp('Optimal solution:');
        disp(x_opt);
    else
        disp('Failed to find an optimal solution.');
    end
    fprintf('\n');
end

function [x_feasible, x_opt, elapsed_time, is_optimal] = solve_lp_with_simplex(A, b, c)
    [m, n] = size(A);
    is_optimal = false;
    elapsed_time = 0;
    x_feasible = [];
    x_opt = [];

    % Solve the problem using the simplex method
    [x_opt, elapsed_time, is_optimal, is_degenerate] = run_simplex(A, b, c, m, n, 100);
    if is_optimal
        x_feasible = x_opt; % In simplex, the optimal solution is also the feasible solution
        fprintf('Simplex: Optimal solution found in %.4f seconds.\n', elapsed_time);
    else
        disp('Simplex: Failed to find the optimal solution.');
    end
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
