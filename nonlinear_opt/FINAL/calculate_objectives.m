function [obj, al] = calculate_objectives(x, gamma, Q0, c, A, lambda, mu, D)
    % Calculate the objective value
    obj = obj_func(x, gamma, Q0, c, D);
    % Calculate the augmented Lagrangian
    al = aug_lag(x, gamma, Q0, c, A, lambda, mu, D);
end
