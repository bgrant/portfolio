function labels = hw5TestL(testImages, nnet)
% HW5TESTL uses a single-layer perceptron to classify handwritten digit images
%
% Parameters:
% * `testImages` is a [YxXx1xN2] matrix of images
% * `nnet` is the neural network returned by hw5TrainL
%
% Return Values:
% * `labels` is a [1xN2] array of labels for the `testImages`

% author: Robert Grant
%   date: 2009-10-13

%% Condition the data
rsImages = hw5ReshapeImages(testImages);
[R N] = size(rsImages);

Y = sim(nnet, rsImages);
labels = uint8(hw5UnvectorizeLabelsL(Y))';

end
