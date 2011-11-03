function [m,V] = hw2FindEigenfaces(A)
% HW2FINDEIGENFACES(A)  Perform principle component analysis of A.
% 
% [m, V] = hw2FindEigenfaces(A)
%  
% Return values:
% * 'm' is the D x 1 mean column vector of A
% * 'V' is a matrix containing the first k eigenvectors of covariance
% matrix of A (after the mean has been subtracted), sorted in descending
% order by eigenvalue and normalized
%
% Parameters:
% * 'A' is a matrix of dimensions [D,N], with each of its N columns being a
% face image reshaped to a vector of length D

% Robert Grant
% Homework #2
% 2009-09-13

%% Preliminaries
X = (double(A))'; % cast to make builtins work
[N,D] = size(X); % get dimensions

%% Compute return values
m = mean(X)'; % mean column
[Vp,L] = eig((1/N)*X*X'); % compute eigenvectors of projected space matrix
l = sum(L); % collapse matrix into a row
U_cell = arrayfun(@(i)(1/((N*l(i))^(1/2)))*X'*Vp(:,i), 1:length(l), ...
    'UniformOutput', 0);
U = cell2mat(U_cell); % eigenfaces

%% Sort eigenvectors
[l_sorted, sort_indices] = sort(l, 'descend');
V = U(:, sort_indices);