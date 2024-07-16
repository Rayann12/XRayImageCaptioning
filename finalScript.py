import json
import io
import sys
import logging
import os
logging.disable(logging.WARNING)
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
# Redirect stdout to a temporary buffer
stdout_buffer = io.StringIO()
stderr_buffer = io.StringIO()
sys.stderr = stderr_buffer
sys.stdout = stdout_buffer
import import_ipynb
from Attention_Model1 import encoder, decoder, tokenizer
from grammify import restructure
import cv2
import numpy as np
import tensorflow as tf

# Clear any previous TensorFlow sessions
tf.keras.backend.clear_session()

# Define input layers
image1 = tf.keras.layers.Input(shape=(224, 224, 3))
image2 = tf.keras.layers.Input(shape=(224, 224, 3))
caption = tf.keras.layers.Input(shape=(26,))

# Connect the input layers to your custom encoder layer
# Assuming encoder takes a list of input tensors
encoder_output = encoder(image1, image2)

# Connect the encoder output and caption input to your custom decoder layer
# Assuming decoder takes a list of input tensors
output = decoder()(encoder_output, caption)

# Define the model
model = tf.keras.Model(inputs=[image1, image2, caption], outputs=output)


def greedy_search_predict(image1, image2, model=model, weights_file='Encoder_Decoder_Weights.h5'):

    # Rest of the function remains the same
    image1 = cv2.imread(image1, cv2.IMREAD_UNCHANGED) / 255
    image2 = cv2.imread(image2, cv2.IMREAD_UNCHANGED) / 255
    image1 = tf.expand_dims(cv2.resize(
        image1, (224, 224), interpolation=cv2.INTER_NEAREST), axis=0)
    image2 = tf.expand_dims(cv2.resize(
        image2, (224, 224), interpolation=cv2.INTER_NEAREST), axis=0)
    model.load_weights('Encoder_Decoder_Weights.h5')
    image1 = model.get_layer('image_encoder')(image1)
    image2 = model.get_layer('image_encoder')(image2)
    image1 = model.get_layer('bkdense')(image1)
    image2 = model.get_layer('bkdense')(image2)

    concat = model.get_layer('concatenate')([image1, image2])
    enc_op = model.get_layer('encoder_batch_norm')(concat)
    enc_op = model.get_layer('encoder_dropout')(enc_op)

    decoder_h, decoder_c = tf.zeros_like(
        enc_op[:, 0]), tf.zeros_like(enc_op[:, 0])
    a = []
    pred = []
    for i in range(26):
        if i == 0:
            caption = np.array(tokenizer.texts_to_sequences(['0']))
        output, decoder_h, attention_weights = model.get_layer(
            'decoder').onestepdecoder(caption, enc_op, decoder_h)

        max_prob = tf.argmax(output, axis=-1)
        caption = np.array([max_prob])
        if max_prob == np.squeeze(tokenizer.texts_to_sequences(['0'])):
            break
        else:
            a.append(tf.squeeze(max_prob).numpy())
    return restructure(tokenizer.sequences_to_texts([a])[0])


def generate_caption(image_path1, image_path2):
    # Generate caption
    caption = greedy_search_predict(image_path1, image_path2)

    return caption


if __name__ == "__main__":
    # Check if correct number of arguments are provided
    # Reset stdout to its original value
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
    
    captions = []
    for i in sys.argv[1:]:
        captions.append(generate_caption(i, i))
    print(json.dumps({"captions": captions}))
