function [x, obj] = hwk6p1(m_values, n, s, p)
    rng(s); % set the random number generator seed

    % initialize arrays to store results for each m
    x = cell(length(m_values), 1);
    obj = zeros(length(m_values), 1);
    all_mean_time = zeros(length(m_values), 1);
    all_std_time = zeros(length(m_values), 1);
    all_degeneracy_count = zeros(length(m_values), 1);

    for m_idx = 1:length(m_values)
        m = m_values(m_idx); 
        elapsed_times = zeros(1, 10); % store times for 10 random instances
        obj_values = zeros(1, 10); % store objective values for each run
        degeneracy_count = 0; % count how many times degeneracy occurs
        best_obj = Inf; % initialize best objective value to infinity
        best_x = zeros(n, 1); % initialize best solution as empty vector

        for i = 1:10
            A = randn(m, n); 
            e = [ones(m, 1); zeros(n-m, 1)]; 
            b = A * e; 
            c = [ones(m, 1); 50 * rand(n - m, 1)];

            % run the simplex algorithm
            [x_current, time_current, is_optimal, is_degenerate] = run_simplex(A, b, c, m, n, p);

            elapsed_times(i) = time_current; % record the time for this run
            if ~is_degenerate && is_optimal && (c' * x_current < best_obj)
                best_obj = c' * x_current; % update the best objective value
                best_x = x_current; % update the best solution
            end

            if is_degenerate
                degeneracy_count = degeneracy_count + 1; % increment degeneracy count
            end

            % record the objective value even if it's degenerate for reporting
            obj_values(i) = c' * x_current;
        end

        % store the best non-degenerate solution and objective for the current m
        x{m_idx} = best_x;
        obj(m_idx) = -best_obj; % negating because we are maximizing

        % calculate and store mean and standard deviation of elapsed times for the current m
        all_mean_time(m_idx) = mean(elapsed_times);
        all_std_time(m_idx) = std(elapsed_times);

        % store the number of degeneracies encountered for the current m
        all_degeneracy_count(m_idx) = degeneracy_count;

        % display results
        fprintf('For m = %d:\n', m);
        fprintf('The best non-degenerate optimal objective value found: %f\n', obj(m_idx));
        fprintf('Mean elapsed time over 10 runs: %f seconds\n', all_mean_time(m_idx));
        fprintf('Standard deviation of elapsed time over 10 runs: %f seconds\n', all_std_time(m_idx));
        fprintf('Number of degeneracies encountered: %d\n', all_degeneracy_count(m_idx));
        fprintf('Best solution vector x:\n');
        disp(x{m_idx});
    end
end

% function [x, obj] = hwk6p1(m, n, s, p)
%     rng(s); % set the random number generator seed
%     elapsed_times = zeros(1, 10); % store times for 10 random instances
%     obj_values = zeros(1, 10); % store objective values for each run
%     degeneracy_count = 0; % count how many times degeneracy occurs
%     best_obj = Inf; % initialize best objective value to infinity
%     best_x = zeros(n, 1); % initialize best solution as empty vector
% 
%     for i = 1:10
%         A = randn(m, n); 
%         e = [ones(m, 1); zeros(n-m, 1)]; 
%         b = A * e; 
%         c = [ones(m, 1); 50 * rand(n - m, 1)]; 
% 
%         % run the simplex algorithm
%         [x_current, time_current, is_optimal, is_degenerate] = run_simplex(A, b, c, m, n, p);
% 
%         elapsed_times(i) = time_current; % record the time for this run
%         if ~is_degenerate && is_optimal && (c' * x_current < best_obj)
%             best_obj = c' * x_current; % update the best objective value
%             best_x = x_current; % update the best solution
%         end
% 
%         if is_degenerate
%             degeneracy_count = degeneracy_count + 1; % increment degeneracy count
%         end
% 
%         % record the objective value even if it's degenerate for reporting
%         obj_values(i) = c' * x_current;
%     end
% 
%     % calculate mean and standard deviation of elapsed times
%     mean_time = mean(elapsed_times);
%     std_time = std(elapsed_times);
% 
%     % return the best non-degenerate solution and objective
%     x = best_x;
%     obj = -best_obj; % negating the objective value because we are maximizing
% 
%     % display results
%     fprintf('The best non-degenerate optimal objective value found: %f\n', obj);
%     fprintf('Mean elapsed time over 10 runs: %f seconds\n', mean_time);
%     fprintf('Standard deviation of elapsed time over 10 runs: %f seconds\n', std_time);
%     fprintf('Number of degeneracies encountered: %d\n', degeneracy_count);
%     fprintf('Best solution vector x:\n');
%     disp(x);
% end