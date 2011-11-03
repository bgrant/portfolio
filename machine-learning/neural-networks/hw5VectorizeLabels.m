function vecLabels = hw5VectorizeLabels(trainLabels)
% HW5VECTORIZELABELS  Transform integer labels into binary vectors
%
%             0 1 2 3 4 5 6 7 8 9
% e.g., 5 -> [0 0 0 0 0 1 0 0 0 0]

% author: Robert Grant
%   date: 2009-10-13

[x N] = size(trainLabels);
vecLabels = zeros(10, N);
lindices = sub2ind(size(vecLabels), double(trainLabels+1), [1:N]);
vecLabels(lindices) = 1;

end

