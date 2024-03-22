function [mean_time, std_time, sosc_freq] = run_optim(m, n, num_runs, p)
    elapsed_times = zeros(num_runs, 1);
    sosc_count = 0; % Initialize counter for SOSC occurrences

    gamma = 100; % Set the value of gamma

    for run = 1:num_runs
        try
            tic; 
            [~, ~, ~, is_sosc] = solve_prob(m(end), n(end), run, p, gamma); % Call solve_prob directly with the last value of m and n
            elapsed_time = toc; 

            elapsed_times(run) = elapsed_time;

            if is_sosc
                sosc_count = sosc_count + 1;
            end
        catch ME
            if ~strcmp(ME.identifier, 'MATLAB:unbounded')
                rethrow(ME);
            else
                fprintf('Encountered an unbounded optimization problem.\n');
            end
        end
    end

    mean_time = mean(elapsed_times);
    std_time = std(elapsed_times);
    sosc_freq = sosc_count / num_runs; % Calculate frequency of SOSC being satisfied
end