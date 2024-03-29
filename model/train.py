import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from tensorflow.keras.callbacks import LearningRateScheduler
from tensorflow.keras.optimizers import Adam


def model_build(n):
    # shape of X_train: (120584, 310), shape of X_test: (30147, 310)
    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(64, input_shape=(n,)),
        tf.keras.layers.Activation('relu'),
        tf.keras.layers.Dense(128),
        tf.keras.layers.Activation('relu'),
        tf.keras.layers.Dense(64),
        tf.keras.layers.Activation('relu'),
        tf.keras.layers.Dense(1)
    ])
    model.compile(optimizer=Adam(learning_rate=0.1), loss='mse', metrics=['mae'])
    return model


def scheduler(epoch):
    # 每隔100个epoch，学习率减小为原来的1/10
    if epoch % 50 == 0 and epoch != 0:
        lr = tf.keras.backend.get_value(model.optimizer.lr)
        tf.keras.backend.set_value(model.optimizer.lr, lr * 0.8)
        print("lr changed to {}".format(lr * 0.8))
    return tf.keras.backend.get_value(model.optimizer.lr)


def load_dataset():
    X_train_load = np.load('../data/X_train.npy')
    Y_train_load = np.load('../data/Y_train.npy')
    X_test_load = np.load('../data/X_test.npy')
    Y_test_load = np.load('../data/Y_test.npy')
    return X_train_load, Y_train_load, X_test_load, Y_test_load


def train(model, EPOCHS, X_train, Y_train, X_test, Y_test):
    # data normalization
    mean_area = X_train[:, -1].mean(axis=0)
    std_area = X_train[:, -1].std(axis=0)
    print(f"X_train_area_data: {X_train[:, -1]}")
    X_train[:, -1] -= mean_area
    X_train[:, -1] /= std_area
    X_test[:, -1] -= mean_area
    X_test[:, -1] /= std_area
    print(f"After normalization: X_train_area_data: {X_train[:, -1]}")
    reduce_lr = LearningRateScheduler(scheduler)

    # training begin
    history = model.fit(X_train, Y_train, epochs=EPOCHS, batch_size=128, validation_split=0.2,
                        verbose=2, callbacks=[reduce_lr])
    # save the model
    model.save("model\\model_weight.model", overwrite=True)
    return model, history


def evaluate(model, X_train_eva, Y_train_eva, X_test_eva, Y_test_eva):
    # evaluate model
    print("train data: ", end="")
    model.evaluate(X_train_eva, Y_train_eva, verbose=2)
    print("test data: ", end="")
    model.evaluate(X_test_eva, Y_test_eva, verbose=2)


def plt_history(history):
    # 绘制训练 & 验证的平均绝对误差值
    plt.plot(history.history['mae'])
    plt.plot(history.history['val_mae'])
    plt.title('Model mean absolute error')
    plt.ylabel('mean absolute error')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.show()

    # 绘制训练 & 验证的损失值
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Model loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.show()


if __name__ == '__main__':
    # print(f"X's shape: {X.shape}, Y's shape: {Y.shape}")
    EPOCHS = 200
    X_train, Y_train, X_test, Y_test = load_dataset()  # load data set
    model = model_build(X_train.shape[1])  # build model
    model.summary()  # print the structure of model
    model, history = train(model, EPOCHS, X_train, Y_train, X_test, Y_test)
    evaluate(model, X_train, Y_train, X_test, Y_test)
    plt_history(history)
