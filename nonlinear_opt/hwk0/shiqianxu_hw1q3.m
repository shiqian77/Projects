fprintf('3c:' );
[x1,num_of_iter1] = newtons_method_fentons([3,2],100,1e-16)
fprintf('It converges at x = [%f,%f].\n', x1(1),x1(2));
fprintf('--------------------\n' );
fprintf('3d:' );
[x2,num_of_iter2] = newtons_method_fentons([3,4],100,1e-16)
fprintf('It converges at x = [%f,%f].\n', x2(1),x2(2));

function [f, g, H] = fentonfgH(x)
    % Our goal fuction
    f = (12 + x(1)^2 + (1+x(2)^2)/x(1)^2 + (x(1)^2 * x(2)^2 + 100)/(x(1)*x(2))^4) / 10; 
    % Gradient of the fuction
    g = [
    (1/10)*(2*x(1) + 2*((-x(1)^2*x(2)^2 - 200)/(x(1)^5*x(2)^4)) - 2*((x(2)^2 + 1)/x(1)^3)); 
    (1/10)*(2*(x(1)^2*x(2)^6 - 200)/(x(1)^4*x(2)^5) - 2*(x(1)^2*x(2)^2)/(x(1)^4*x(2)^5))
];
    % Hessian matrix of the fuction
    H = [
    (1/10)*(6/(x(1)^4)*(x(2)^2+1) + 20/(x(1)^6*x(2)^4)*(x(1)^2*x(2)^2+100)),...
    (1/10)*((-14/(x(1)^4*x(2)^2) + 2/x(1)^2))
    (1/10)*((-4*x(2)/x(1)^3) - (12/(x(1)^3*x(2)^3)) + (16/(x(1)^5*x(2)^5))*(x(1)^2*x(2)^2+100)),...
    (1/10)*((20*(x(1)^2*x(2)^2+100))/(x(1)^4*x(2)^6) + 2/x(1)^2 - 14/(x(1)^2*x(2)^4))
];
end

function alpha = line_search(f_func, x, p_k, alpha_bar, rho, c)
    alpha = alpha_bar;
    [f, grad_f, hh] = f_func(x); % Evaluate the function and gradient at the current x
    while true
        [f_new, hhh, hhhh] = f_func(x + alpha * p_k); % Evaluate the new function value
        if f_new <= f + c * alpha .* grad_f' .* p_k
            break;
        end
        alpha = rho * alpha; % update alpha
    end
end

function [x, num_of_iter] = newtons_method_fentons(x0, max_iter, tol)
    x = x0;
    num_of_iter = 0;
    for k = 1:max_iter
        [hhhhh, g, H] = fentonfgH(x); % Get the function value, gradient, and Hessian matrix
        if norm(g, Inf) < tol
            break; % Stop if the gradient norm is less than the tolerance
        end
        [hhhhhh,p] = chol(H); % Apply Cholesky decomposition to check if H is positive definite
        if p > 0
            E = eye(length(x));
            H = H + E; % if H is not positive definite, make H positive definite
        end
        p_k = -H\g; % Compute the Newton step
        alpha_k = line_search(@fentonfgH, x, p_k', 1, 0.5, 1e-4); % Perform a line search
        x = x + alpha_k * p_k' % Update the current estimate 
        num_of_iter = k; % Update the number of iterations
    end
end