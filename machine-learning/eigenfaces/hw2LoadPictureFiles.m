function data = hw2LoadPictureFiles()
% HW2LOADPICTUREFILES()  Load in data and convert to analyzable form
%
% This function loads pictures from disk, and then arranges the data into
% 'gallery' matrices where each column is a vector of pixels.  It then
% packages up some metadata about the gallery with it into a struct, and 
% returns all these structs in a cell array.  My own human classification
% of the photos is one of the pieces of metadata passed back.
%
% Return Values:
% * 'data' is a cell array containing a struct for each set of face data.
% This struct contains the gallery itself, as well as some useful metadata
% about the gallery.
%   Fields: * 'name' is the directory name the data was in
%           * 'gallery' is the matrix of pictures
%           * 'labels' is an n x 3 matrix of labels, where each column is a
%                      human labelled variable. 'smiling', 'glasses', and 
%                      'male' are the variables, where indicates a human 
%                      labelled it true, and 0 indicates false. n is equal
%                      to nimages.
%           * 'height' is the original height in pixels of each picture
%           * 'dims' is the dimensionality of the pictures (height*width)
%           * 'nimages' is the number of images in the gallery

% Homework #2
% Robert Grant
% 2009-09-13

%% Define paths and human supplied labels
face_root = '/Users/bgrant/desktop/machine-learning/homework/hw2/faces/';

class08_path = fullfile(face_root, 'class08faces'); %png, b&w

%          smiling glasses male
class08_labels = [1 1 1;
                  1 1 1;
                  0 1 1;
                  1 1 1;
                  0 1 1;
                  1 1 1;
                  1 1 1;
                  0 0 1;
                  0 0 1;
                  1 0 1;
                  1 0 1;
                  1 0 1;
                  1 0 1;
                  0 0 1;
                  0 0 1;
                  1 1 1;
                  1 0 0;
                  1 0 1;
                  0 1 1;
                  0 0 1;
                  1 1 1;
                  0 1 1;
                  1 1 1;
                  1 1 1;
                  0 1 1;
                  1 1 1;
                  1 0 1;
                  1 0 1;
                  1 0 1;
                  1 0 1;
                  0 1 1;
                  0 0 1;
                  1 1 1;
                  1 0 0;
                  1 0 1;
                  1 1 0;
                  0 1 1;
                  0 0 1;
                  0 0 1;
                  1 0 1];
                  
                  
class09_path = fullfile(face_root, 'class09faces'); %tiff, color
class09_labels = [1 0 1;
                  0 0 1;
                  0 1 1;
                  1 0 1;
                  1 0 1;
                  0 1 0;
                  1 1 1;
                  1 1 1;
                  0 1 1;
                  1 0 0;
                  1 0 1;
                  0 1 1;
                  0 0 1;
                  1 1 1;
                  1 0 1;
                  1 1 1;
                  0 1 1;
                  1 1 1;
                  1 1 1;
                  0 1 1;
                  1 0 0;
                  1 1 1;
                  0 0 1;
                  1 1 1;
                  0 0 1;
                  1 0 0;
                  0 0 1;
                  1 0 0;
                  1 0 1;
                  1 0 1;
                  1 0 1;
                  0 0 1;
                  1 0 0];

yale_path = fullfile(face_root, 'yalefaces'); %png, b&w
yale_labels =    [1 0 1;
                  0 0 1;
                  0 0 1;
                  1 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  1 0 1;
                  1 0 1;
                  0 1 1;
                  1 0 1;
                  0 0 1;
                  1 0 1;
                  1 0 1;
                  1 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 1 1;
                  1 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 1 1;
                  1 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 1 1;
                  1 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  1 0 1;
                  0 1 1;
                  1 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  1 1 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 1 1;
                  1 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  1 0 1;
                  0 0 1;
                  0 0 1;
                  0 1 1;
                  0 1 1;
                  0 1 1;
                  1 1 1;
                  0 1 1;
                  0 0 1;
                  0 1 1;
                  0 1 1;
                  0 1 1;
                  0 1 1;
                  0 1 1;
                  0 0 1;
                  0 0 1;
                  0 1 1;
                  1 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 1 1;
                  1 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 0;
                  0 0 0;
                  0 1 0;
                  1 0 0;
                  0 0 0;
                  0 0 0;
                  0 0 0;
                  0 0 0;
                  0 0 0;
                  0 0 0;
                  0 0 0;
                  0 0 1;
                  0 0 1;
                  0 1 0;
                  1 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 1 1;
                  0 1 1;
                  0 1 1;
                  1 1 1;
                  0 1 1;
                  0 0 1;
                  0 1 1;
                  0 1 1;
                  0 1 1;
                  0 1 1;
                  0 1 1;
                  0 0 1;
                  0 1 1;
                  0 1 1;
                  1 0 1;
                  0 1 1;
                  0 0 1;
                  0 0 1;
                  0 1 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 1 1;
                  1 0 1;
                  0 1 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1;
                  0 0 1];
              

face_paths = {class08_path, class09_path, yale_path};
face_labels = {class08_labels, class09_labels, yale_labels};
ngalleries = length(face_paths);

%% Find picture files and load them into a cell array as a 'gallery matrix'
face_galleries = {}; % gallery matrices
gallery_height = []; % height for pictures each gallery
for i = 1:ngalleries,
    face_path = face_paths{i};
    file_struct = dir(face_path);
    filenames = {file_struct.name};
    fullpaths = cellfun(@(fname)fullfile(face_path, fname), filenames, ...
        'UniformOutput', false);
    fullpaths = {fullpaths{3:end}}; % trim off '.' and '..' entries
    faces = cellfun(@imread, fullpaths, 'UniformOutput', false);
    [rows, cols] = size(faces{1});
    gallery_height(end+1) = rows; 
    
    % if color, make b&w for simplicity
    if strcmp(face_path, class09_path) 
        faces = cellfun(@rgb2gray, faces, 'UniformOutput', false);
    end
        
    % pack images into 'gallery' matrix
    vectorfaces = cellfun(@(A)reshape(A, [], 1), faces, 'UniformOutput', false);
    vectorfaces = double(cell2mat(vectorfaces)); % some functions don't work on uint8
    face_galleries{end+1} = vectorfaces;
end

%% Package up galleries with metadata
data = {};
for m = 1:ngalleries,
    [pathstr, name, ext, versn] = fileparts(face_paths{m});
    [D, nimages] = size(face_galleries{m});
    data{end+1} = struct('name', name, ...
                         'gallery', face_galleries{m}, ...
                         'labels', face_labels{m}, ...
                         'height', gallery_height(m), ...
                         'dims', D, ...
                         'nimages', nimages);
end