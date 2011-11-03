function [class1, class2] = classify_gaussian(data, method, c1, m1, s1, c2, m2, s2)
% CLASSIFY_GAUSSIAN  Classifies points according to mixture of two
% gaussians.
% 
% [class1, class2] = classify_gaussian(data, method, c1, m1, s1, c2, m2, s2)
%  
% Return values:
% * 'class1' is the set of points estimated to be part of the gaussian with
% mixing coefficient 'c1', mean 'm1', and covariance matrix 's1' 
% 
% * 'class2' is the set of points estimated to be part of the gaussian with
% mixing coefficient 'c2', mean 'm2', and covariance matrix 's2' 
%
% Parameters:
% * 'data' is the set of points to classify
% 
% * 'method' is one of either 'hard' or 'soft'. 'hard' classifies a
% point based entirely on which gaussian it is more likely to have come
% from. 'soft' randomly classifies a point, weighting the choice based on
% likelihood.
% 
% * 'cx', 'mx', and 'sx' correspond to the mixing coefficient, mean, and
% covariance matrix of each gaussian we are using to model (and classify)
% the data

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
% Homework #1
% 2009-09-06

prob_in_1 = c1 * mvnpdf(data, m1, s1);
prob_in_2 = c2 * mvnpdf(data, m2, s2);

if strcmp(method, 'hard')
    class1_index = find(prob_in_1 > prob_in_2);
    class2_index = find(prob_in_1 <= prob_in_2);
    
    class1 = data(class1_index, :);
    class2 = data(class2_index, :);
elseif strcmp(method, 'soft')
    totalprob = prob_in_1 ./ (prob_in_1 + prob_in_2);
    selections = binornd(1, totalprob);
    
    class1 = data(find(selections), :);
    class2 = data(find(~selections), :);
else
    assert(0, 'Method must be either "threshold" or "soft"');
end
