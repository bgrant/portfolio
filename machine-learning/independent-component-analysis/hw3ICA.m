function [Y, W, R] = hw3ICA(X, W, eta, R_max)
% HW3ICA  This function performs independent component analysis on data.
%
% This algorithm performs independent component analysis as a way of doing
% blind source separation on the matrix X.  It does this using gradient
% ascent, searching for a point of maximum entropy, and returns an estimate
% of original source signals, assuming that column vectors in X have been
% formed by a linear combination of source vectors.
% 
% Sizes used in descriptions:
% * 'n' is the number of original source signals
% * 'm' is the number of received signals
% * 't' is the length of each received signal in samples
% We assume n == m for this algorithm.
% 
% Parameters:
% * 'X' is the set of m received signals, size [m,t]
% * 'W' is the initial estimate of the separation matrix, size [n,m]
% * 'eta' is the scalar learning rate
% * 'R_max' is the maximum number of iterations to run the algorithm.  The
% algorithm may return early if it detects convergence.
%
% Return Values:
% * 'Y' is the final estimate of the matrix of separated signals, size [n,t]
% * 'W' is the final estimate of the separation matrix, size [n,m]
% * 'R' is the number of iterations the algorithm actually ran.  It may
% be less than R_max if algorithm convergence or divergence was detected.
%
%
% We assume X = AU, where size(A) == [m,n]
%   X  =    A   *  U
% [m,t]   [m,n]  [n,t]
%  
% Y is our current estimate of U (the source signals)
%   Y  =    W   *  X
% [n,t]   [n,m]  [m,t]
%
%  W = A^-1

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

% Homework #3
% Robert Grant
% 2009-09-20

changes = zeros(1,R_max);
for R = [1:R_max],
    Y = W*X;
    Z = 1./(1+exp(-Y));
    dW = eta*(eye(size(W)) + (1-2*Z)*Y')*W;
    W = W + dW;
    
    [hasConverged, changes(R)] = hw3HasConverged(dW, 1e-10);
    if hasConverged
        break;
    end
    
%    if mod(R,R_max/10) == 0
%        display(R);
%        display(changes(R));
%    end
end
%figure;
%loglog(changes(1:R),'x-'); 
%title('Algorithm Convergence');
%xlabel('Iterations');
%ylabel('sqrt(max(max(dW.^2)))');
