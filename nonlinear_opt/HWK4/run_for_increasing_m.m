function run_for_increasing_m()
    seed = 123; % Seed value for reproducibility
    max_runtime = 3600; % Maximum total runtime in seconds (1 hour)
    max_single_run_time = 300; % Maximum time allowed for a single run 
    start_time = tic; % Start the timer for the entire process
    
    m = 5; % Start with problem size m = 5
    while toc(start_time) < max_runtime
        fprintf('Running for m = %d...\n', m);
        
        run_start_time = tic; % Timer for this run
        [mean_time, std_dev_time, results] = run_random_instances(m, seed);
        run_elapsed_time = toc(run_start_time); % Time taken for this run

        fprintf('Results for m = %d:\n', m);
        fprintf('Mean time: %f seconds\n', mean_time);
        fprintf('Standard deviation of time: %f seconds\n', std_dev_time);
        for i = 1:length(results)
            fprintf('Run %d: fval = %f, exit flag = %d\n', i, results(i).fval, results(i).exitflag);
        end
        
        if run_elapsed_time > max_single_run_time
            fprintf('Single run exceeded the maximum allowed time of %d seconds. Stopping at m = %d.\n', max_single_run_time, m);
            break;
        end
        
        m = m + 5; % Increment m by 5 for the next run
    end
end

function [mean_time, std_dev_time, results] = run_random_instances(m, seed)
    rng(seed); % Set the random number generator seed
    n = 2 * m;
    times = zeros(1, 10); % Store times for 10 random instances
    results(numel(times)) = struct('x', [], 'fval', NaN, 'exitflag', NaN); % Initialize results structure
    
    for i = 1:10
        A = randn(m, n);
        b = rand(m, 1);
        c = [ones(m, 1); 50 * rand(n - m, 1)];
        [x, elapsed_time, is_optimal] = run_simplex(A, b, c, m, n);
        times(i) = elapsed_time;
        
        % Store results
        results(i).x = x;
        results(i).fval = c' * x; 
        results(i).exitflag = is_optimal;
    end
    
    mean_time = mean(times);
    std_dev_time = std(times);
end

function [x, elapsed_time, is_optimal] = run_simplex(A, b, c, m, n)
    B_indices = 1:m;
    N_indices = (m+1):n;
    B = A(:, B_indices);
    N = A(:, N_indices);
    cB = c(B_indices);
    cN = c(N_indices);
    xB = B \ b;

    tic;
    while true
        [p, q, is_optimal, is_unbounded] = simplex_step(B, N, cB, cN, xB);

        if is_optimal || is_unbounded
            break;
        end

        % Update B, N, cB, cN, xB
        entering = N_indices(q);
        leaving = B_indices(p);
        B(:, p) = N(:, q);
        N(:, q) = full(sparse(p, 1, 1, m, 1)); % Corrected line
        B_indices(p) = entering;
        N_indices(q) = leaving;
        cB(p) = cN(q);
        cN(q) = c(leaving);
        xB = B \ b;
    end

    x = zeros(n, 1);
    x(B_indices) = xB;
    elapsed_time = toc;
end

function [p, q, is_optimal, is_unbounded] = simplex_step(B, N, cB, cN, b)
    lambda = B' \ cB;
    sN = cN - (N' * lambda);

    if all(sN >= 0)
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

    theta = b ./ dq;
    theta(dq <= 0) = inf;
    [min_theta, p] = min(theta);

    b = b - dq * min_theta;
    b(p) = min_theta;
    is_optimal = false;
    is_unbounded = false;
end

