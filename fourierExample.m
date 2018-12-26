%% fourier example for saw function

% the script shows approximation of a "saw function" via different order
% fourier series

clearvars;
close all

% saw function y = x+2
x =0:0.01:2-0.01;
newX = repmat(x,1,4);
plotX=0:0.01:8-0.01;
y = newX+2;

figure
plot(plotX,y,'k','LineWidth',3)

Nloop = 20;

legendCell = cell(1,Nloop+2);
legendCell{1} = 'y = x+2';
legend(legendCell{1})
title('fourier series demonstration')

hold on

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% start loop approximation

yApprox = zeros(Nloop,numel(plotX));
yApprox(1,:) = 3;

wKey = waitforbuttonpress;

plot(plotX,yApprox(1,:), 'LineWidth',2)

ySeries = zeros(Nloop,numel(plotX));
ySeries(1,:)=sin(pi*plotX);

for nn = 2:Nloop
    
    ySeries(nn,:)=ySeries(nn-1,:)+(sin(nn*pi*plotX)/(nn));
    
end


for nn = 2:Nloop

    legendCell{nn}=[num2str(nn-2) '° order approximation'];
    title(legendCell{nn})
    
    yApprox(nn,:) =yApprox(1,:)-(2/pi)*ySeries(nn-1,:);
    
    wKey = waitforbuttonpress;

    plot(plotX,yApprox(nn,:), 'LineWidth',2)
    
end