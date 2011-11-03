function [i, c1, m1, s1, c2, m2, s2] = em(data, thresh)
% EM    Expectation Maximization Algorithm from PRML p.438-439
% 
% Using Expectiation Maximization, returns the parameters of the mixure of
% 2 gaussians that best represent the 2d dataset given.
% 
% [i, c1, m1, s1, c2, m2, s2] = em(data, thresh)
%  
% Return values:
% * 'i' is the number of iterations used before convergence
% * 'cx' is the estimated mixing coefficient for gaussian x
% * 'mx' is the estimated mean of gaussian x
% * 'sx' is the estimated covariance matrix for gaussian x
%
% Parameters:
% * 'data' is the [n x 2] matrix of data
%
% * 'thresh' defines the minimum much change between mean estimates allowed
% to continue the algorithm.  If norm(current_mean - last_mean) < thresh for 
% both means, the algorithm is considered to have converged.

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


% Initialize estimates
ndata = length(data);

% mixing coefficient estimates
c1 = 0.5; 
c2 = 0.5;

% mean estimates
m1 = [0 0]; 
m2 = [1 1];

% covariance matrix estimates
s1 = eye(2,2); 
s2 = eye(2,2);

% iterations of EM
done = 0;
i = 0;
while ~done,
    i = i+1;
    
    % Evaluate log likelihood
     % likelihoods scaled by mixing coefficients (c1 and c2)
    sl1 = c1 * mvnpdf(data, m1, s1);
    sl2 = c2 * mvnpdf(data, m2, s2);

     % log likelihood
    %ll = sum(log(sl1 + sl2))

    % E step - evaluate responsibilities
    g1 = sl1 ./ (sl1 + sl2);
    g2 = sl2 ./ (sl1 + sl2);

    % M step - re-estimate parameters
    m1_old = m1;
    m2_old = m2;
    
    N1 = sum(g1);
    N2 = sum(g2);

    m1 = (1/N1) * (g1' * data);
    m2 = (1/N2) * (g2' * data);

    m1rep = repmat(m1, ndata, 1);
    m2rep = repmat(m2, ndata, 1);
    moment1 = data - m1rep;
    moment2 = data - m2rep;
    s1n = zeros(2,2);
    s2n = zeros(2,2);
    for n = 1:ndata,
        s1n = s1n + g1(n) * moment1(n,:)' * moment1(n,:);
        s2n = s2n + g2(n) * moment2(n,:)' * moment2(n,:);
    end
    
    s1 = (1/N1) * s1n;
    s2 = (1/N2) * s2n;
        
    c1 = N1/ndata;
    c2 = N2/ndata;
    
    % check for convergence
    if (norm(m1 - m1_old) < thresh) && (norm(m2 - m2_old) < thresh)
        done = 1;
    end
    
end
