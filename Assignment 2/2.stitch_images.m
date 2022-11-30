
imagefiles = dir('*.jpeg');
img1 = imread(imagefiles(1).name);
grayim1 = im2gray(img1);
pnts = detectSURFFeatures(grayim1);
[features, pnts] = extractFeatures(grayim1,pnts);

nimgs = numel(imagefiles);
tforms(nimgs) = projtform2d;

disp(nimgs)

imgSize = zeros(nimgs,2);

for i = 2:nimgs
    prev_pnts = pnts;
    prev_features = features;

    I = imread(imagefiles(i).name);
    grayim = im2gray(I);

    imgSize(i,:) = size(grayim);

    pnts = detectSURFFeatures(grayim);
    [features, pnts] = extractFeatures(grayim,pnts);

    indexes = matchFeatures(features, prev_features, 'Unique', true);

    matched = pnts(indexes(:,1),:);
    prev_matched = prev_pnts(indexes(:,2),:);

    tforms(i) = estgeotform2d(matched, prev_matched,'projective', 'Confidence', 89.9, 'MaxNumTrials',4000);

    tforms(i).A = tforms(i-1).A * tforms(i).A;

end

for i = 1:numel(tforms)
    [xlim(i,:), ylim(i,:)] = outputLimits(tforms(i), [1 imgSize(i,2)], [1 imgSize(i,1)]);
end

avgXlim = mean(xlim, 2);
[~,idx] = sort(avgXlim);
centerIdx = floor((numel(tforms)+1)./2);
centerImageIdx = idx(centerIdx);

Tinv = invert(tforms(centerImageIdx));
for i = 1:numel(tforms)    
    tforms(i).A = Tinv.A * tforms(i).A;
end

%creating empty panorama
for i = 1:numel(tforms)           
    [xlim(i,:), ylim(i,:)] = outputLimits(tforms(i), [1 imgSize(i,2)], [1 imgSize(i,1)]);
end

maxImageSize = max(imgSize);

% Find the minimum and maximum output limits. 
xMin = min([1; xlim(:)]);
xMax = max([maxImageSize(2); xlim(:)]);

yMin = min([1; ylim(:)]);
yMax = max([maxImageSize(1); ylim(:)]);

% Width and height of panorama.
width  = round(xMax - xMin);
height = round(yMax - yMin);

% Initialize the "empty" panorama.
panorama = zeros([height width 3], 'like', I);

%creating panorama

blender = vision.AlphaBlender('Operation', 'Binary mask', ...
    'MaskSource', 'Input port');  

% Create a 2-D spatial reference object defining the size of the panorama.
xLimits = [xMin xMax];
yLimits = [yMin yMax];
panoramaView = imref2d([height width], xLimits, yLimits);

% Create the panorama.
for i = 1:nimgs
    
    I = imread(imagefiles(i).name); 
   
    % Transform I into the panorama.
    warpedImage = imwarp(I, tforms(i), 'OutputView', panoramaView);
                  
    % Generate a binary mask.    
    mask = imwarp(true(size(I,1),size(I,2)), tforms(i), 'OutputView', panoramaView);
    
    % Overlay the warpedImage onto the panorama.
    panorama = step(blender, panorama, warpedImage, mask);
end

figure
imshow(panorama)

baseFileName = sprintf('result.png');
fullFileName = fullfile('', baseFileName);
imwrite(panorama, fullFileName);