% This script runs hw5Train{L,B} and hw5Test{L,B}, linearly increasing the
% number percentage of training used and explores the effects.

% :author: Robert David Grant <robert.david.grant@gmail.com>
%
% :date: 2009-10-13
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

load hw5;

pmin = 1;
pmax = 20;
testPattern = 'backprop';

%% Test perceptron network
if strcmp(testPattern, 'perceptron') || strcmp(testPattern, 'all'), 
    errL = -1 * ones(1,pmax);
    for j = 1:pmax,
        nnetL = hw5TrainL(trainImages, trainLabels, 10*j);
        labelsL = hw5TestL(testImages, nnetL);
        errL(j) = hw5ErrorRate(labelsL, testLabels)
    end
end

%% Test backpropagation
if strcmp(testPattern, 'backprop') || strcmp(testPattern, 'all'), 
    errB = -1 * ones(1,pmax);
    for j = 1:pmax,
        nnetB = hw5TrainB(trainImages, trainLabels, 10*j);
        labelsB = hw5TestB(testImages, nnetB);
        errB(j) = hw5ErrorRate(labelsB, testLabels)
    end
end

figure;
if strcmp(testPattern, 'perceptron'), 
    plot([1:pmax], errL, 'bo-');
elseif strcmp(testPattern, 'backprop'), 
    plot([1:pmax], errB, 'ro-');
else
    plot([1:pmax], errL, 'bo-');
    hold on;
    plot([1:pmax], errB, 'ro-');
end
title('Neural Network Error Rate vs. Number of Training Passes');
xlabel('Number of Training Passes');
ylabel('Error Rate');
legend('Perceptron', 'Backpropagation');

