function errorRate = hw5ErrorRate(outputs, truth)
% HW5ERRORRATE  Computes the fraction of outputs that are incorrect

% author: Robert Grant
%   date: 2009-10-13

errorRate = 1 - sum(outputs == truth) / length(outputs);

end
