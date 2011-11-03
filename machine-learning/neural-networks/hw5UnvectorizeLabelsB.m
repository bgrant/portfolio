function labels = hw5UnvectorizeLabels(vecLabels)
% HW5UNVECTORIZELABELS  Transform binary vector labels back into integers
%
%        0 1 2 3 4 5 6 7 8 9
% e.g., [0 0 0 0 0 1 0 0 0 0] -> 5

% author: Robert Grant
%   date: 2009-10-13

% if no neurons fired, pick one randomly
[maxes, indices] = max(vecLabels);
labels = indices - 1;

end

