function [f, g, H] = rosenbrock(x0)
    % Ensure x0 is a column vector
    x0 = x0(:);
    
    % Define symbolic variables as a column vector
    syms x [length(x0) 1];
    
    % Rosenbrock function definition
    f_sym = 0;
    for i = 1:(length(x) - 1)
        f_sym = f_sym + 100*(x(i+1) - x(i)^2)^2 + (1 - x(i))^2;
    end

    % Calculate the gradient and the Hessian
    grad_sym = gradient(f_sym, x);
    Hess_sym = hessian(f_sym, x);

    % Substitute numerical values into the symbolic expressions
    f = double(subs(f_sym, x, x0));
    g = double(subs(grad_sym, x, x0));
    H = double(subs(Hess_sym, x, x0));
end
