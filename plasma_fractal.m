%% plasma fractal 
% the script creates a plasma fractal by using the diamond-square algorithm
% https://en.wikipedia.org/wiki/Diamond-square_algorithm

clear all
close all

%######################## PARAMETERS HERE!!! ##############################

it = 9; % (2^x)+1, final dimension of the matrix

%##########################################################################

tic
startMat=rand(2,2);
cellit= cell(1,it);
for ii=1:it
    %% take old values and enlarge them to a bigger matrix

    % progression unit
    unit=(2^ii)+1;

    % create vector with startMat values
    vectStart=zeros(1,numel(startMat));
    vectStart(:)=startMat;

    % create new vector
    lenMat = unit^2;
    newVect = nan(1,lenMat);
    whloop = 0;
    orLoop = 1;
    while whloop<lenMat
        acc = 1;
        while acc<=unit
            if mod(acc,2)==0
                newVect(:,whloop+acc)=0;
            else
                newVect(:,whloop+acc)=vectStart(orLoop);
                orLoop=orLoop+1;
            end
            acc=acc+1;
        end
    whloop=whloop+acc;          
    newVect(whloop:(whloop+unit-1))=0;
    whloop=whloop+unit-1;    
    end
    
    newVect((unit^2+1):end)=[];
    
    % create new starting matrix
    swapMat=zeros(unit);
    swapMat(:)=newVect;

    %% algorithm 
    logIndx=(swapMat==0);
    linIndx=find(logIndx);
    diamVer=linIndx(rem(linIndx,2)~=0);
    sqrEdge=linIndx(rem(linIndx,2)==0); logIndx=zeros(unit);
    logIndx(sqrEdge)=sqrEdge;
    
    % create "crown"
    northCrown=logIndx(1,:); logIndx(1,:)=0;
    southCrown=logIndx(end,:); logIndx(end,:)=0;
    westCrown=logIndx(:,1); logIndx(:,1)=0;
    eastCrown=logIndx(:,end); logIndx(:,end)=0;
    innerSqr=find(logIndx);
    
    %% diamonds vertex
    for wkw=1:numel(diamVer)
        p1D=diamVer(wkw)-unit-1;p2D=diamVer(wkw)-unit+1;p3D=diamVer(wkw)+unit-1;p4D=diamVer(wkw)+unit+1;
        swapMat(diamVer(wkw))=mean(swapMat([p1D p2D p3D p4D]))+(2*rand()-1)/(3*ii^2);
    end
    %% square edges
    % create vectors
    northCrown=northCrown(northCrown~=0);
    southCrown=southCrown(southCrown~=0);
    eastCrown=eastCrown(eastCrown~=0);
    westCrown=westCrown(westCrown~=0);
    
    for nn=1:numel(northCrown)
        n1=northCrown(nn)-unit; n2=northCrown(nn)+1; n3=northCrown(nn)+unit;
        swapMat(northCrown(nn))=mean(swapMat([n1 n2 n3]))+(2*rand()-1)/(3*ii^2);
    end
    for ss=1:numel(southCrown)
        s1=southCrown(ss)-unit; s2=southCrown(ss)-1; s3=southCrown(ss)+unit;
        swapMat(southCrown(ss))=mean(swapMat([s1 s2 s3]))+(2*rand()-1)/(3*ii^2);
    end
    for ee=1:numel(eastCrown)
        e1=eastCrown(ee)-1; e2=eastCrown(ee)-unit; e3=eastCrown(ee)+1;
        swapMat(eastCrown(ee))=mean(swapMat([e1 e2 e3]))+(2*rand()-1)/(3*ii^2);
    end
    for ww=1:numel(westCrown)
        w1=westCrown(ww)-1; w2=westCrown(ww)+unit; w3=westCrown(ww)+1;
        swapMat(westCrown(ww))=mean(swapMat([w1 w2 w3]))+(2*rand()-1)/(3*ii^2);
    end
    if isempty(innerSqr)==0
        for kwk=1:numel(innerSqr)
            p1S=innerSqr(kwk)-1; p2S=innerSqr(kwk)+1; p3S=innerSqr(kwk)+unit; p4S=innerSqr(kwk)-unit;
            swapMat(innerSqr(kwk))=mean(swapMat([p1S p2S p3S p4S]))+(2*rand()-1)/(3*ii^2);
        end
    end
    
    
    startMat=swapMat;
    
    cellit{ii}=swapMat;
    
    outMat=uint8(repmat(swapMat*255,1,1,3));
    image(outMat)
    pause(0.4)

    
end



     
elTime = toc;

disp(['elapsed time for ' num2str(it) ' iterations: ' num2str(elTime) 'sec'])
            
    