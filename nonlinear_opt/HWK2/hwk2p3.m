function x = hwk2p3(x0, c)
    armijo_c = 0.001;
    alpha_bar = 1;
    rho = 0.5;
    max_iters = 1000;
    starting_points = [1, 1; -1, 1; -1, -1; 1, -1];
    % Call the plot_steepest_descent_metrics function
    plot_steepest_descent_metrics(starting_points, alpha_bar, rho, armijo_c, c, max_iters);
end
