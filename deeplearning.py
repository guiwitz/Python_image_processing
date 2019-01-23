from keras.models import Model
from keras.layers import Input, concatenate, Conv2D, MaxPooling2D, Conv2DTranspose, Reshape, Flatten
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint
from keras import backend as K

import numpy as np
import matplotlib.pyplot as plt
import pandas as  pd

K.set_image_data_format('channels_last')  # TF dimension ordering in this code
smooth = 1.
output = None


#define the dice coefficient
def dice_coef(y_true, y_pred):
    smooth = 1
    y_true_f = K.flatten(y_true)
    y_pred_f = K.flatten(y_pred)
    intersection = K.sum(y_true_f * y_pred_f)
    return (2. * intersection + smooth) / (K.sum(y_true_f) + K.sum(y_pred_f) + smooth)


#define the deep learning network, here a U-net architecture
def get_unet(dims,img_rows,img_cols):
    inputs = Input((img_rows, img_cols, dims))
    conv1 = Conv2D(32, (3, 3), activation='relu', padding='same')(inputs)
    conv1 = Conv2D(32, (3, 3), activation='relu', padding='same')(conv1)
    pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)

    conv2 = Conv2D(64, (3, 3), activation='relu', padding='same')(pool1)
    conv2 = Conv2D(64, (3, 3), activation='relu', padding='same')(conv2)
    pool2 = MaxPooling2D(pool_size=(2, 2))(conv2)

    conv3 = Conv2D(128, (3, 3), activation='relu', padding='same')(pool2)
    conv3 = Conv2D(128, (3, 3), activation='relu', padding='same')(conv3)
    pool3 = MaxPooling2D(pool_size=(2, 2))(conv3)

    conv4 = Conv2D(256, (3, 3), activation='relu', padding='same')(pool3)
    conv4 = Conv2D(256, (3, 3), activation='relu', padding='same')(conv4)
    pool4 = MaxPooling2D(pool_size=(2, 2))(conv4)

    conv5 = Conv2D(512, (3, 3), activation='relu', padding='same')(pool4)
    conv5 = Conv2D(512, (3, 3), activation='relu', padding='same')(conv5)

    up6 = concatenate([Conv2DTranspose(256, (2, 2), strides=(2, 2), padding='same')(conv5), conv4], axis=3)
    conv6 = Conv2D(256, (3, 3), activation='relu', padding='same')(up6)
    conv6 = Conv2D(256, (3, 3), activation='relu', padding='same')(conv6)

    up7 = concatenate([Conv2DTranspose(128, (2, 2), strides=(2, 2), padding='same')(conv6), conv3], axis=3)
    conv7 = Conv2D(128, (3, 3), activation='relu', padding='same')(up7)
    conv7 = Conv2D(128, (3, 3), activation='relu', padding='same')(conv7)

    up8 = concatenate([Conv2DTranspose(64, (2, 2), strides=(2, 2), padding='same')(conv7), conv2], axis=3)
    conv8 = Conv2D(64, (3, 3), activation='relu', padding='same')(up8)
    conv8 = Conv2D(64, (3, 3), activation='relu', padding='same')(conv8)

    up9 = concatenate([Conv2DTranspose(32, (2, 2), strides=(2, 2), padding='same')(conv8), conv1], axis=3)
    conv9 = Conv2D(32, (3, 3), activation='relu', padding='same')(up9)
    conv9 = Conv2D(32, (3, 3), activation='relu', padding='same')(conv9)

    conv10 = Conv2D(1, (1, 1), activation='sigmoid')(conv9)
    
    conv11 = Reshape((img_rows*img_cols,1),input_shape=(img_rows,img_cols,1))(conv10)

    model = Model(inputs=[inputs], outputs=[conv11])
    
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=[dice_coef], sample_weight_mode='temporal')
        
    return model


#routine to train the network
def nuclei_train(folder, img_rows,img_cols, dims=1, batch_size = 32, epochs = 100, weights = None):

    imgs_train = np.load(folder+'imgs_train.npy')
    imgs_mask_train = np.load(folder+'imgs_mask_train.npy')
    imgs_weight_train = np.load(folder+'imgs_weight_train.npy')
    
    imgs_train = imgs_train.astype('float32')

    imgs_mask_train = imgs_mask_train[..., np.newaxis]
    imgs_mask_train = imgs_mask_train.astype('float32')
    
    imgs_weight_train = imgs_weight_train.astype('float32')

    nuclei_model = get_unet(dims,img_rows,img_cols)
    model_checkpoint = ModelCheckpoint(folder+'weights.h5', monitor='val_loss', save_best_only=True)
    
    if weights:
        nuclei_model.load_weights(weights)
        
    nuclei_model.fit(imgs_train, imgs_mask_train, batch_size=batch_size, epochs=epochs, verbose=1, shuffle=True,
              validation_split=0.2,sample_weight = imgs_weight_train,
              callbacks=[model_checkpoint])