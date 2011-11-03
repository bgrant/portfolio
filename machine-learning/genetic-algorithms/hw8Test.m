function sorted_matrix = hw8Test(unsorted_matrix, sorting_net)
% sorted_array = hw8Test(unsorted_matrix, sorting_net)
% Apply the sorting network evolved in hw8Train.
%
% :Parameters:
% `unsorted_matrix`: a 1x8 matrix of double values to sort
% `sorting_net`: an evolved sorting network from the population (Nx2 matrix)
%
% :Return Values:
% `sorted_array`: a permutation of `unsorted_array`
%
% This function permutes `unsorted_matrix` via the swap instructions in the
% simple sorting network `sorting_net`. `sorting_net` is implemented as an
% Nx2 matrix, each row being a pair of indicies of the array to swap.  The
% swap pairs are all applied in order, and the elements are only swapped if
% the second is greater than the first.

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

[nrows, ncols] = size(sorting_net);
assert(ncols == 2);

for i=1:nrows
    swap = sort(sorting_net(i,:));
    % swap the two numbers iff the earlier number in the matrix is greater
    if unsorted_matrix(swap(1)) > unsorted_matrix(swap(2))
        temp = unsorted_matrix(sorting_net(i,1));
        unsorted_matrix(sorting_net(i,1)) = ...
            unsorted_matrix(sorting_net(i,2));
        unsorted_matrix(sorting_net(i,2)) = temp;
    end
end

sorted_matrix = unsorted_matrix;


