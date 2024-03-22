function al = aug_lag(x, gamma, Q0, c, A, lambda, mu, D)
    lin_term = 0;
    quad_term = 0;
    
    i = 1;
    while i <= size(A, 2)
        ci = A(:, i)' * x + gamma * x' * D{i} * x;  
        lin_term = lin_term + lambda(i) * ci;
        quad_term = quad_term + (ci ^ 2);
        i = i + 1;
    end
    
    al = obj_func(x, gamma, Q0, c, D) - lin_term + (mu/2) * quad_term;
end
