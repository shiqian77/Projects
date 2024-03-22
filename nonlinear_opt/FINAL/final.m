function [x, obj] = final(m, n, s, p)
    m_vals = m;
    
    % Call the optimization_and_plot function
    [mean_t, std_t, sosc_freq_array] = optimization_and_plot(m_vals, p);
    
    % Set the value of gamma
    gamma = 100;
    
    % Call the solve_prob function for the last value of m and n
    [x, ~, obj, ~] = solve_prob(m(end), n(end), s, p, gamma);
    
    % Plot the mean and standard deviation versus m
    figure;
    plot(m_vals, mean_t, 'o-', 'LineWidth', 1.5);
    xlabel('m');
    ylabel('Mean Time (s)');
    title('Mean Optimization Time vs. m');
    grid on;
    figure;
    plot(m_vals, std_t, 'o-', 'LineWidth', 1.5);
    xlabel('m');
    ylabel('Standard Deviation (s)');
    title('Standard Deviation of Optimization Time vs. m');
    grid on;
end

