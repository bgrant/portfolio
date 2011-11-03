function labels = hw5TestB(testImages, nnet)
% HW5TESTB uses a backpropagation-based neural net to classify handwritten
% digit images
%
% Parameters:
% * `testImages` is a [YxXx1xN2] matrix of images
% * `nnet` is the neural network returned by hw5TrainB
%
% Return Values:
% * `labels` is a [1xN2] array of generated labels for the `testImages`

% author: Robert Grant
%   date: 2009-10-13

%% Condition the data
rsImages = hw5ReshapeImages(testImages);

Y = sim(nnet, rsImages);
labels = uint8(hw5UnvectorizeLabelsB(Y));

end
