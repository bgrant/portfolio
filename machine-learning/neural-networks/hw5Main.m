% author: Robert Grant
%   date: 2009-10-13

% This script runs hw5Train{L,B} and hw5Test{L,B}, linearly increasing the
% number percentage of training used and explores the effects.

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

