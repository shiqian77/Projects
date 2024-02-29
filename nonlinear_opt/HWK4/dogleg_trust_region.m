function [x_opt, num_linear_solves, num_func_evals] = dogleg_trust_region(rosenbrock, x0, max_iter, tol)
 
    delta_hat = 10; 
    xk = x0;
    delta = 2;
    eta = 0.1;
    num_linear_solves = 0;
    num_func_evals = 0;
    
    [fk, gk, Hk] = rosenbrock(xk);
    num_func_evals = num_func_evals + 1;

    k = 0; 
    % Convert Hessian to sparse format and solve the linear system
    while k < max_iter && norm(gk, 2) > tol
        k = k + 1; 
        Hk = sparse(double(Hk)); 
        pk = -Hk\gk;  
        num_linear_solves = num_linear_solves + 1;
        
        %  Compute the scaled gradient
        gkHk = gk' * Hk * gk;
        if gkHk <= 0
            tau = 1;
        else
            tau = min(norm(gk)^3 / (delta * gkHk), 1);
        end
        pu = -tau * (delta / norm(gk)) * gk;
        
        % Compute the dogleg path combining Newton and gradient steps
        p = compute_dogleg_path(pk, pu, delta);
        
        % Update the solution estimate
        x_new = xk + p;
        [fk_new, gk_new, Hk_new] = rosenbrock(x_new);
        num_func_evals = num_func_evals + 1;

        % Update the solution if the step is accepted
        rho_k = (fk - fk_new) / (-gk'*p - 0.5*p'*Hk*p);
        
        % Update the trust region radius based on the ratio
        if rho_k > 3/4 && norm(p) == delta
            delta = min(2*delta, delta_hat);
        elseif rho_k < 1/4
            delta = 1/4 * delta;
        end

        if rho_k > eta
            xk = x_new;
            fk = fk_new;
            gk = gk_new;
            Hk = Hk_new;
        end
    end
    
    % return the optimal solution 
    x_opt = xk;
end



