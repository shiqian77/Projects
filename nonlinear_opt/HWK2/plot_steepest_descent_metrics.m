function plot_steepest_descent_metrics(starting_points, alpha_bar, rho, armijo_c, C, max_iters)
    % Cell arrays to store metrics for each starting point
    convergence_metric = cell(1, size(starting_points, 1));
    true_error = cell(1, size(starting_points, 1));

    % Run the steepest descent from each starting point
    for idx = 1:size(starting_points, 1)
        [x_star, h, hh, g, err] = steepest_descent_armijo(starting_points(idx, :)', alpha_bar, rho, armijo_c, C, max_iters);
        convergence_metric{idx} = g;
        true_error{idx} = err;
        fprintf('Final point x* from starting point [%d, %d]: x* = (%f,%f)\n', ...
            starting_points(idx, 1), starting_points(idx, 2), x_star(1), x_star(2));
    end

    % Plotting the convergence metrics for different starting points
    figure;
    for idx = 1:4
        sp = subplot(2, 2, idx);
        axis square; 
        yyaxis left;
        p1 = semilogy(true_error{idx}, 'b-'); 
        ylabel('Log True Error');
        yyaxis right;
        p2 = semilogy(convergence_metric{idx}, 'Color', [0.8500, 0.3250, 0.0980], 'LineStyle', '-'); 
        ylabel('Norm of Gradient');
        title(['Starting Point [', num2str(starting_points(idx, :)), ']']);
        xlabel('Iteration');
        legend(sp, [p1, p2], 'True Error', 'Norm of Gradient', 'Location', 'best');
    end
    sgtitle('Convergence Metrics for Different Starting Points');

    % Plotting the convergence rate across iterations
    figure;
    for idx = 1:4
        % Calculate the ratio of the gradient norm
        ratios = convergence_metric{idx}(2:end) ./ convergence_metric{idx}(1:end-1);
        subplot(2, 2, idx);
        plot(ratios, 'LineWidth', 2); 
        xlabel('Iteration');
        ylabel('Ratio of Gradient Norm');
        title(['Convergence Rate for Starting Point [', num2str(starting_points(idx, :)), ']']);
    end
    sgtitle('Convergence Rate Across Iterations');
end


function [x, s, k, g, err] = steepest_descent_armijo(x0, alpha_bar, rho, armijo_c, C, max_iters)
    x = x0;
    s = 0;
    k = [];
    g = [];
    err = [];

    conv_bound = (C - 1) / (C + 1); % the convergence rate bound

    % Set a threshold as a small multiple of the convergence bound
    threshold = conv_bound * 1e-16;
    % 1000 iterations or until the stopping criterion is met
    for i = 1:max_iters
        grad_val = grad(x, C); % Calculate gradient
        p = -grad_val; % Find descent direction
        alpha = BTLS(x, alpha_bar, rho, armijo_c, p, grad_val, C); % Backtracking line search for step size
        x_new = x + alpha * p;
        f_new = f(x_new, C);
        err_new = norm(x_new - [0; 0]); % Assuming x* = [0; 0]
        s = s + 1;
        k(end+1) = f_new;
        g(end+1) = norm(grad_val);
        err(end+1) = err_new;
        
        % Calculate the actual decrease
        if i > 1
            actualDecrease = k(end-1) - f_new;
            % Check for the stopping criteria
            if actualDecrease < threshold || i >= 1000
                fprintf('Stopping criterion triggered at iteration %d.\n', i);
                break;
            end
        end
        x = x_new; 
    end
end

function val = f(x, C)
    val = x(1)^2 + C * x(2)^2; % define the gradient fuction
end

function gradient = grad(x, C)
    gradient = [2*x(1); 2*C*x(2)]; % define the gradient
end

function alpha = BTLS(x, alpha_bar, rho, armijo_c, p, gradient, C)
    alpha = alpha_bar;
    % Perform the backtracking line search
    while f(x + alpha * p, C) > f(x, C) + armijo_c * alpha * (gradient' * p)
        alpha = rho * alpha;
    end
end