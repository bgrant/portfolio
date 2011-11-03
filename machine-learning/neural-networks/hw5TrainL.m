function nnet = hw5TrainL(trainImages, trainLabels, passes)
% HW5TRAINL trains a single-layer perceptron to classify handwritten digit
% images
%
% Parameters:
% * `trainImages` is a [YxXx1xN1] matrix of images
% * `trainLabels` is a [1xN1] matrix of labels
% * `passes` is the number of training passes to use (default=10)
% between 0 and 1. (default=1)
%
% Return Values:
% * `nnet` is the trained perceptron

% author: Robert Grant
%   date: 2009-10-13

if nargin == 2,
    passes = 10;
end

%% Condition the input data
rsImages = hw5ReshapeImages(trainImages);
vecLabels = hw5VectorizeLabels(trainLabels);

%nnet = newp(repmat([0,255], [R, 1]), S, 'hardlim', 'learnp');
nnet = newp(rsImages, vecLabels, 'hardlim', 'learnp');

%% Train the network
nnet.adaptParam.passes = passes;
nnet = adapt(nnet, rsImages, vecLabels);

end
