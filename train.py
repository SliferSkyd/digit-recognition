import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing import image as keras_image

from PIL import Image, ImageChops, ImageOps
def plot_image(image, filename):
    plt.figure()
    plt.imshow(image)
    plt.colorbar()
    plt.grid(False)
    plt.savefig(filename + '.png')

mnist = tf.keras.datasets.mnist
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

train_images = train_images / 255.0
test_images = test_images / 255.0

def train_model():
    import os
    if os.path.exists('model') and os.path.exists('model/model.keras'): return

    tf.random.set_seed(42)

    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation ='relu'),
        tf.keras.layers.Dense(64, activation ='relu'),
        tf.keras.layers.Dense(28, activation ='relu'),
        tf.keras.layers.Dense(10, activation='softmax')
    ])

    model.compile(optimizer='adam',
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=['accuracy'])

    model.fit(train_images, train_labels, epochs=15, batch_size=32, validation_data=(test_images, test_labels))
    model.save('model/model.keras')

def make_prediction(image):
    train_model()
    model = tf.keras.models.load_model('model/model.keras')
    image = clean_image(image)
    prediction = model.predict(np.array([image]))
    return (int(np.argmax(prediction)), float(np.max(prediction)))

def clean_image(request):
    image = Image.open(request)
    bg = Image.new("RGBA", image.size, "white")
    image = Image.alpha_composite(bg, image).convert("L")

    image = ImageOps.invert(image)
    image = ImageChops.offset(image, 2, 2)
    image = ImageOps.grayscale(image)
    image = image.resize((28, 28))
    image_array = np.array(image, dtype='float64')
    image_array = image_array / 255.0
    return image_array

if __name__ == '__main__':
    train_model()