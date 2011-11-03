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

% :author: Robert David Grant <robert.david.grant@gmail.com>
%
% :copyright:
%    Copyright 2011 Robert David Grant
%
%    Licensed under the Apache License, Version 2.0 (the "License"); you
%    may not use this file except in compliance with the License.  You
%    may obtain a copy of the License at
%
%       http://www.apache.org/licenses/LICENSE-2.0
%
%    Unless required by applicable law or agreed to in writing, software
%    distributed under the License is distributed on an "AS IS" BASIS,
%    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
%    implied.  See the License for the specific language governing
%    permissions and limitations under the License.

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
