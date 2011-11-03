function nnet = hw5TrainB(trainImages, trainLabels, passes)
% HW5TRAINB trains a backpropagation-based neural net to classify handwritten
% digit images
%
% Parameters:
% * `trainImages` is a [YxXx1xN1] matrix of images
% * `trainLabels` is a [1xN1] matrix of labels
% * `passes` is the number of training passes to use (default = 10)
% between 0 and 1. (default=1)
%
% Return Values:
% * `nnet` is the trained neural network 

% author: Robert Grant
%   date: 2009-10-13

if nargin == 2,
    passes = 10;
end

%% Condition the input data
rsImages = hw5ReshapeImages(trainImages);
vecLabels = hw5VectorizeLabels(trainLabels);

nnet = newff(rsImages, vecLabels, [20], {'tansig','tansig'});

%nnet.trainParam.epochs = passes;
%nnet = train(nnet, rsImages, vecLabels);

nnet.adaptParam.passes = passes;
nnet = adapt(nnet, rsImages, vecLabels);
end
