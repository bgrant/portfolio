function [hasConverged, change] = hw3HasConverged(dW, thresh)
% HW3HASCONVERGED  This function detects algorithm convergence or
% divergence.
%
% This function determines whether Independent Component Analysis has
% converged by computing whether a metric has fallen below a threshold.  If
% the metric becomes 'NaN', it determines that the algorithm has diverged.
% 
% Parameters:
% * 'dW' is the matrix of change from one iteration of gradient descent to
% another.
% * 'thresh' is the threshold below which the 'change' metric must fall for 
% us to consider the algorithm to have converged.
%
% Return Values:
% * 'hasConverged' is a boolean value indicating whether the metric has
% fallen below the threshold, or is 'NaN' (has diverged).
% * 'change' is the actual metric computed from 'dW'.  I use the metric
% sqrt(max(max(dW.^2))), which finds the maximum absolute value in 'dW'.

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

% set metric
% sqrt of maximum change in an element
change = sqrt(max(max(dW.^2)));

% determine convergence
if change < thresh
    hasConverged = true;
elseif isnan(change) % has diverged
    hasConverged = true;
else
    hasConverged = false;
end
