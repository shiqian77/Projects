function is_pd = pos_def_on_null_cholesky(hess, x_opt, A, gamma, D, m)
    % Construct the Jacobian of the constraints
    J = zeros(m, length(x_opt));
    for i = 1:m
        J(i, :) = A(:, i)' + 2 * gamma * (D{i} * x_opt)';
    end
    
    % Calculate the basis for the null space of the Jacobian
    null_space_basis = null(J);
    
    % Project the Hessian onto the null space of the Jacobian
    projected_Hessian = null_space_basis' * hess * null_space_basis;
    
    % Attempt Cholesky decomposition to check for positive definiteness
    try
        chol(projected_Hessian);
        is_pd = true;
    catch
        is_pd = false;
    end
end