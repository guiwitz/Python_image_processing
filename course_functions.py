import os, sys
import numpy as np
import skimage.morphology as skm
import skimage.filters as skf

from skimage.measure import label, regionprops

from skimage.feature import match_template, peak_local_max

#Define the path of leading to Data folder
def define_data_path():
    if 'google.colab' in sys.modules:
        datapath = '/content/gdrive/My Drive/'
    else:
        datapath = '../'
        
    return datapath


    
def detect_nuclei(image, size = 200, shape = 0.8):

    """Detect nuclei in image using binary operations
    
    Parameters
    ----------
    image : 2D numpy array
        image to be segmented
    size: number  
        maximal nucleus size
    shape: float
        minimal nucleus eccentricity
        
    Returns
    -------
    newimage : 2D numpy array
        mask of nuclei
    """
    
    
    #median filter
    image_med = skf.rank.median(image,selem=np.ones((2,2)))
    #otsu thresholding
    image_local_threshold = skf.threshold_local(image_med,block_size=51)
    image_local = image > image_local_threshold
    #remove tiny features
    image_local_eroded = skm.binary_erosion(image_local, selem= skm.disk(1))
    #label image
    image_labeled = label(image_local_eroded)
    #analyze regions
    our_regions = regionprops(image_labeled)
    #create a new mask with constraints on the regions to keep
    newimage = np.zeros(image.shape)
    #fill in using region coordinates
    for x in our_regions:
        if (x.area>200):# and (x.eccentricity>shape):
            newimage[x.coords[:,0],x.coords[:,1]] = 1
            
    return newimage


def create_disk_template(radius):
    
    """Create a disk image
    
    Parameters
    ----------
    radius : int
        radius of disk
        
    Returns
    -------
    template : 2D numpy array
        binary image of a disk
    """
    
    template = np.zeros((2*radius+5,2*radius+5))
    center = [(template.shape[0]-1)/2,(template.shape[1]-1)/2]
    Y, X = np.mgrid[0:template.shape[0],0:template.shape[1]]
    dist_from_center = np.sqrt((X - center[0])**2 + (Y-center[1])**2)
    template[dist_from_center<=radius] = 1
    
    return template



def detect_nuclei_template(image, template):

    """Detect nuclei in image using template matching
    
    Parameters
    ----------
    image : 2D numpy array
        image to be segmented
    template: 2D numpy array  
        template for nucleus shape
        
    Returns
    -------
    masked_peaks : 2D numpy array
        mask where each nucleus is represented by a single white pixel
    otsu_mask : maks obtained using the Otsu threshold
    """
    
    matched = match_template(image=image, template=template, pad_input=True)

    local_max = peak_local_max(matched, min_distance=10,indices=False)

    otsu = skf.threshold_otsu(image)
    otsu_mask = image>otsu
    
    otsu_mask = skm.binary_dilation(otsu_mask, np.ones((5,5)))
    masked_peaks = local_max*otsu_mask
    
    return masked_peaks, otsu_mask
