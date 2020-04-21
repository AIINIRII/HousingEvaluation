import numpy as np

from model.train import model_build, train, evaluate, plt_history


def load_dataset():
    X_train_load = np.load('../data/X_train_323.npy')
    Y_train_load = np.load('../data/Y_train_323.npy')
    X_test_load = np.load('../data/X_test_323.npy')
    Y_test_load = np.load('../data/Y_test_323.npy')
    return X_train_load, Y_train_load, X_test_load, Y_test_load


if __name__ == '__main__':
    # print(f"X's shape: {X.shape}, Y's shape: {Y.shape}")
    EPOCHS = 200
    SEED = 2020
    X_train, Y_train, X_test, Y_test = load_dataset()  # load data set
    model = model_build(X_train.shape[1])  # build model
    model.summary()  # print the structure of model
    model, history = train(model, EPOCHS, X_train, Y_train, X_test, Y_test, SEED)
    evaluate(model, X_train, Y_train, X_test, Y_test)
    plt_history(history)
