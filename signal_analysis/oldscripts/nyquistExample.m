%% nyquist example
% the script shows how the sampling frequency changes the discrete representation of a continuous signal.
% run the script and update with button press.

clearvars;
close all

% function to sample
x =(0:0.001:2-0.001);

y = sin(5*x*2*pi)+sin(x*2*pi)+cos(10*x*2*pi);

figure
plot(x,y,'k','LineWidth',2)
% hold on 
% plot(plotX,sin(pi*plotX))

Nloop = 25;

legendCell = cell(1,Nloop+2);
legendCell{1} = 'signal to be sampled';
legend(legendCell{1})
title('nyquist demonstration')


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% start loop approximation


for nn = 2:Nloop
    
    coordNewSample = round(linspace(1,numel(x),2*nn));
    
    wKey = waitforbuttonpress;
    
    plot(x,y,'k','LineWidth',2)
    hold on
    plot(x(coordNewSample),y(coordNewSample),'r-o', 'LineWidth',1)
    hold off
    
    legendCell{nn}=[num2str(nn) 'Hz Sample frequency'];
    legend(legendCell{nn})  
    title('nyquist demonstration')

end
