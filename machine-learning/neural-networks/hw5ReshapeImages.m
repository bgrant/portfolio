function rsImages = hw5ReshapeImages(trainImages)
% HW5RESHAPEIMAGES  Reshape the given image matrix into a simpler 2-D matrix
%
% uint8[Y x X x 1 x N1] -> double[(Y*X) x N1]

% author: Robert Grant
%   date: 2009-10-13

rsImages = squeeze(trainImages);
[Y, X, N1] = size(rsImages);
rsImages = double(reshape(rsImages, Y*X, N1));

end
