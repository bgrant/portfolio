function error_rates = hw2ClassifyEigenfaces(data_struct, train_fraction)
% HW2CLASSIFYEIGENFACES(data_struct, train_function)  Nearest neighbor classification of vectors.
% 
% error_rates = hw2ClassifyEigenfaces(data_struct, train_fraction)
%  
% Return values:
% * 'error_rates' is a vector representing the error rate of the
% classification algorithm for each variable with a label vector
%
% Parameters:
% * 'data_struct' is one of the data structures returned by 
% hw2LoadPictureFiles.
% * 'train_fraction' is a floating point number between 0 and 1 indicating
% how much of the dataset to devote to training.  For example, if
% train_fraction is set to 0.4, the first 40% of the dataset will be
% devoted to training, and the remaining 60% will be used as a test set.

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

%% Train on first train_fraction of data, test on rest
ntraining = floor(data_struct.nimages * train_fraction);
ntest = data_struct.nimages - ntraining;
train_set = data_struct.gallery(:, 1:ntraining);
test_set = data_struct.gallery(:, ntraining+1:end);

[m, V] = hw2FindEigenfaces(train_set); % mean vector, eigenvectors of cov
train_projection = ((train_set - repmat(m,1,ntraining))'*V)';
test_projection = ((test_set - repmat(m,1,ntest))'*V)';

train_truth = data_struct.labels(1:ntraining, :)';
test_truth = data_struct.labels(ntraining+1:end, :)';

%% Classify test_set as nearest train_set neighbor in eigenspace 
%(metric is sum-squared error)
test_decisions = zeros(3,ntest);
for i=1:ntest,
    test_matrix = repmat(test_projection(:,i), 1, ntraining);
    [sq_err, best_match] = min(sum((train_projection - test_matrix).^2));
    test_decisions(:,i) = train_truth(:, best_match);
end

%% Score algorithm (error rate)
error_rates = sum((test_decisions - test_truth).^2, 2) / ntest;
