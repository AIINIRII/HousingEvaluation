import tensorflow as tf
from tensorflow_core.python.keras.saving.save import load_model
from model.train import load_dataset, price_accuracy


def analysis_model(model: tf.keras.Model):
    X_train, Y_train, X_test, Y_test = load_dataset()
    model.evaluate(X_train, Y_train, verbose=2)
    model.evaluate(X_test, Y_test, verbose=2)


if __name__ == '__main__':
    model = load_model("./model_weight.model", custom_objects={'price_accuracy': price_accuracy})
    analysis_model(model)
