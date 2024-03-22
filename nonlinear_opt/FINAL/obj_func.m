function obj = obj_func(x, gamma, Q0, c, D) 
    obj = c' * x + x' * Q0 * x + gamma * sum(cellfun(@(Di) x' * Di * x, D));
end