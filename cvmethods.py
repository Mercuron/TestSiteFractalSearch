import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.image import imread
import matplotlib.pyplot as plt
import cv2
import os

from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import imutils
import pandas as pd

def structure(path_in,path_out):
    image = cv2.imread(path_in)
    print('STRUCTURE',path_in)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7,7), 0.33)
    v = np.median(gray)
    sigma=0.33
    #---- apply automatic Canny edge detection using the computed median----
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(gray, lower, upper)
    edged = cv2.dilate(edged, None, iterations=1)
    edged = cv2.erode(edged, None, iterations=1)
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    i=1
    index=[]
    while i <= len(cnts):
        print(i)
        s='c'+str(i)
        index.append(s)
        i=i+1
    columns=['Area','Per','Emin','Emaj','Circularity','Roundness','AR','Solidity','x','Axc','q']
    df = pd.DataFrame(index=index, columns=columns)
    orig = image.copy()
    (cnts, _) = contours.sort_contours(cnts)
    i=1
    import math
    for c in cnts:
        box = cv2.minAreaRect(c)
        box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
        box = np.array(box, dtype="int")
        box = perspective.order_points(box)
        x,y,w,h = cv2.boundingRect(c)
        text='c'+str(i)
        i=i+1
        cv2.putText(orig, text,
                    (int(x+ w/2), int(y+h/2)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                0.65, (255, 0, 255), 2)
        df.loc[text]['Area']=cv2.contourArea(c)
        df.loc[text]['Per']=cv2.arcLength(c,True)
        ellipse = cv2.fitEllipse(c)
        (xc,yc),(d1,d2),angle = ellipse
        df.loc[text]['Emin']=d1
        df.loc[text]['Emaj']=d2
        df.loc[text]['Circularity']=(4*math.pi*cv2.contourArea(c))/(cv2.arcLength(c,True)*cv2.arcLength(c,True))
        df.loc[text]['Roundness']=4*cv2.contourArea(c)/(math.pi *d2*d2)
        df.loc[text]['AR']=d2/d1
        hullArea = cv2.contourArea(cv2.convexHull(c))
        df.loc[text]['Solidity']=cv2.contourArea(c)/hullArea
        df.loc[text]['x']=w/2
        df.loc[text]['Axc']=w/2*w/2*d2/d1*math.pi/4
    AxcC=df['Axc'].max()
    df['q']=AxcC/df['Axc']
    Q=df['q'].sum()
    df['s_sum']=df['Axc']*df['Circularity']
    AxsNC=df['Axc'].sum()
    s_=df['s_sum'].sum()/AxsNC
    plt.imshow(orig)
    plt.axis('off')
    plt.savefig(path_out,bbox_inches='tight')
    return df,AxsNC,s_

def pca_im(path_in,path_out):#PCA image
    image_raw = imread(path_in)
    image_sum = image_raw.sum(axis=2)
    print(image_sum.shape)

    image_bw = image_sum/image_sum.max()
    print(image_bw.max())
    #plt.figure(figsize=[12,8])
    #plt.imshow(image_bw, cmap=plt.cm.gray)
    from sklearn.decomposition import PCA, IncrementalPCA
    pca = PCA()
    pca.fit(image_bw)

    # Getting the cumulative variance

    var_cumu = np.cumsum(pca.explained_variance_ratio_)*100

    # How many PCs explain 95% of the variance?
    k = np.argmax(var_cumu>95)
    print("Number of components explaining 95% variance: "+ str(k))
    #print("\n")

    plt.figure(figsize=[10,5])
    plt.title('Cumulative Explained Variance explained by the components. 95% Var ='+str(k)+' components')
    plt.ylabel('Cumulative Explained variance')
    plt.xlabel('Principal components')
    plt.axvline(x=k, color="k", linestyle="--")
    plt.axhline(y=95, color="r", linestyle="--")
    ax = plt.plot(var_cumu)
    name_graph=os.path.splitext(path_out)[0]+'gr.jpg'
    plt.savefig(name_graph)
    #/\ IMAGE GRAPH
    ipca = IncrementalPCA(n_components=k)
    image_recon = ipca.inverse_transform(ipca.fit_transform(image_bw))

    # Plotting the reconstructed image
    plt.figure(figsize=[12,8])
    plt.imshow(image_recon,cmap = plt.cm.gray)
    plt.axis('off')
    plt.savefig(path_out,bbox_inches='tight')
    return name_graph,path_out
    #OUTPUT RECONSTRUCT

#FOURIER
def fourier (pathin,pathout):
    img = cv2.imread(pathin) # load an image
    img = img[:,:,2] # blue channel
    plt.imshow(img, cmap='gray')
    f = cv2.dft(np.float32(img), flags=cv2.DFT_COMPLEX_OUTPUT)
    f_shift = np.fft.fftshift(f)
    f_complex = f_shift[:,:,0] + 1j*f_shift[:,:,1]
    f_abs = np.abs(f_complex) + 1 # lie between 1 and 1e6
    f_bounded = 20 * np.log(f_abs)
    f_img = 255 * f_bounded / np.max(f_bounded)
    f_img = f_img.astype(np.uint8)
    cv2.imwrite(pathout,f_img)
    return True
