% question (v)
function [x] = hwk3p3(x0, niter, eps)
    % Set the parameters for the optimization methods inside hwk3p3
    tol = eps; 
    max_iters = niter; 
    alpha_bar = 1;
    rho = 0.5; 
    armijo_c = 1e-4; 
    beta = 1e-3; 

    % Call the run_optimization_methods_rosenbrock function with the parameters
    run_optimization_methods_rosenbrock(x0, tol, max_iters, alpha_bar, rho, armijo_c, beta);
end

%For question (v), In command window, put 
% clear;
% x0 = [5,10];
% niter = 1000; 
% eps = 1e-6;
% x = hwk3p3(x0, niter, eps); 

%% This is for question (iv)
% function [x] = hwk3p3(x0, niter, eps)
%     % Set the parameters for the optimization methods inside hwk3p3
%     tol = eps; 
%     max_iters = niter; 
%     alpha_bar = 1;
%     rho = 0.5; 
%     armijo_c = 1e-4; 
%     beta = 1e-3; 
% 
%     % Call the run_optimization_methods_rosenbrock function with the parameters
%     run_optimization_methods(x0, tol, max_iters, alpha_bar, rho, armijo_c, beta);
% end

%For question (iv), In command window, put 
% clear;
% x0 = [[3,2];[3,4]];
% niter = 1000; 
% eps = 1e-6;
% x = hwk3p3(x0, niter, eps); 
 



