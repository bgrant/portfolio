function hw2FindEigenfaces_Test(A)
% HW2FINDEIGENFACES_TEST  Perform simple assertion tests on function.
% 
% When executed, this function will run a series of tests.  If a test
% fails, the function will end with an assertion error.

% Robert Grant
% Homework #2
% 2009-09-13

%% Simple test
A = [1 0;
     0 1];

[m, V] = hw2FindEigenfaces(A);
matassert(m == [0.5, 0.5]');
matassert(V == [1 0; 0 1])

%%
A = [1 0;
     0 1];

[m, V] = hw2FindEigenfaces(A);
matassert(m == [0.5, 0.5]');
matassert(V == [1 0; 0 1])



end




%%
function matassert(cond)
% Generalized assert
    assert(all(reshape(cond,1,[])));
end