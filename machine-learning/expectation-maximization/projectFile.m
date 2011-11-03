% This script defines two 2-d gaussians, performs Expectation Maximization 
% as described in PRML Ch. 9.2, classifies the data, then plots some 
% informative graphs.

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

% Homework #1
% Robert Grant
% 2009-09-06


clear;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 1. Build a model (mixture of Gaussians)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
ndata = 2000;

coeff1 = 0.1; % mixing coefficient
mu1 = [1 -1]; % mean
cov1 = [0.9 0.4; 0.4 0.3]; % covariance matrix

coeff2 = 0.9; % mixing coefficient
mu2 = [1 0];  % mean
cov2 = [0.5 0.0; 0.0 0.5]; % covariance matrix


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 2. Generate data
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
data1 = mvnrnd(mu1, cov1, coeff1*ndata);
data2 = mvnrnd(mu2, cov2, coeff2*ndata);
data = [data1; data2];


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 3. Expectation maximization
% (Algorithm from PRML p.438-439)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
thresh = 0.001;
[i, c1, m1, s1, c2, m2, s2] = em(data, thresh);

% Classify points
[class1_hard, class2_hard] = classify_gaussian(data, 'hard', c1, m1, s1, c2, m2, s2);
[class1_soft, class2_soft] = classify_gaussian(data, 'soft', c1, m1, s1, c2, m2, s2);

% Analyze and print out results
i
c1, m1, s1
c2, m2, s2


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 4. Create plots
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
figure;
hold on;
plot(data1(:,1), data1(:,2), '.g');
plot(data2(:,1), data2(:,2), '.r');
title('2-d Gaussian Data as Generated')

figure;
hold on;
plot(class1_hard(:,1), class1_hard(:,2), '.g');
plot(class2_hard(:,1), class2_hard(:,2), '.r');
title('Data with Hard Classification')

figure;
hold on;
plot(class1_soft(:,1), class1_soft(:,2), '.g');
plot(class2_soft(:,1), class2_soft(:,2), '.r');
title('Data with Soft Classification')

% [EOF] 
