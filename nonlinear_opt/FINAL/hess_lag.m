function hess_mat = hess_lag(x_opt, lambda_opt, Q0, gamma, D, A, m)
    hess_f = 2 * Q0 + 2 * gamma * sum(cat(3, D{2:end}), 3);
    
    hess_c = zeros(size(Q0));
    for i = 1:m
        hess_c = hess_c + lambda_opt(i) * (2 * gamma * D{i+1});
    end
    
    hess_mat = hess_f + hess_c;
end