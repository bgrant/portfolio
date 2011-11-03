function labels = hw5UnvectorizeLabels(vecLabels)
% HW5UNVECTORIZELABELS  Transform binary vector labels back into integers
%
%        0 1 2 3 4 5 6 7 8 9
% e.g., [0 0 0 0 0 1 0 0 0 0] -> 5

% author: Robert Grant
%   date: 2009-10-13

% if no neurons fired, pick one randomly
[erow, ecol] = find(sum(vecLabels) == 0);
vecLabels(randint(1, length(erow), [1,10]), ecol) = 1; 

% if multiple neurons fire for one pattern, we must break the tie
[row, col] = find(vecLabels);
[b, m, n] = unique(col);
labels = row(m) - 1; 
                     

end

