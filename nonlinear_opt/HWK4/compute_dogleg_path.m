% Determine whether to use the Newton step or a combination of gradient and Newton steps
function p = compute_dogleg_path(pk, pu, delta)
    % If Newton step is outside the trust region, use a combination
    if norm(pk) > delta
        pb = pu + (delta - norm(pu)) * (pk - pu) / norm(pk - pu);
        p = pb;
    else
         % If Newton step is inside the trust region, use it directly
        p = pk;
    end
end

