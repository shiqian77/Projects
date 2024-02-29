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
