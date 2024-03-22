function [mean_t, std_t, sosc_freq_array] = optimization_and_plot(m_vals, p)
    mean_t = zeros(length(m_vals), 1);
    std_t = zeros(length(m_vals), 1);
    sosc_freq_array = zeros(length(m_vals), 1);

    for idx = 1:length(m_vals)
        m = m_vals(idx);
        n = 2 * m;
        
        % Run the optimization problem multiple times and calculate mean and standard deviation of time
        [mean_time, std_time, sosc_freq] = run_optim(m, n, 10, p);
        
        % Store the mean and standard deviation values
        mean_t(idx) = mean_time;
        std_t(idx) = std_time;
        sosc_freq_array(idx) = sosc_freq;
        
        fprintf('For m = %d: Mean Time = %.4f s, Std Time = %.4f s, SOSC Satisfied = %.2f%%\n', m, mean_time, std_time, sosc_freq * 100);
    end
end
