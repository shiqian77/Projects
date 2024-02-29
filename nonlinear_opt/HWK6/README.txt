1.Git pull two files "hwk6p1.m","run_simplex.m" to local(they must in the same directory).
2.Open all the files in matlab
3.In the matlab command window, type:
s = 1; 
p = 100;
m_values = [5,10,15,20]; 
n_values = 2 .* m_values; 

for i = 1:length(m_values)
    m = m_values(i);
    n = n_values(i);
    fprintf('Running hwk6p1 with m=%d and n=%d\n', m, n);
    [x, obj] = hwk6p1(m, n, s, p);
end
press enter

If in the command window, shows something like unrecognized function or variable, just run all the files, it might notify you to add to the path. Then repeat step 3. It will show you all the outputs(the best non-degenerate optimal objective value, mean elapsed time over 10 runs, standard deviation of elapsed time over 10 runs, number of degeneracies encountered, and the best solution vector x) for m = 5,10,15,20 respectively.

If you only want to run the output for one value of m, you can comment this function and uncomment the below function, and in the Matlab command window, type: 
[x, obj] = hwk6p1(5, 10, 123, 1000);
press enter, and it will show you all the outputs(the best non-degenerate optimal objective value, mean elapsed time over 10 runs, standard deviation of elapsed time over 10 runs, number of degeneracies encountered, and the best solution vector x) for m = 5(you can change it to any number, so does n, s, and p).