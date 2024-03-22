function grad = grad_aug_lag(x, gamma, Q0, c, A, lambda, mu, D)
    grad_contribs = cellfun(@(Di) Di * x, D, 'UniformOutput', false);
    grad_contribs_mat = cat(2, grad_contribs{:}); % Concatenate
    grad_f = c + 2 * Q0 * x + 2 * gamma * sum(grad_contribs_mat, 2);
    
    grad_c = A * (lambda - mu * (A' * x));
    
    grad = grad_f - grad_c;
end
