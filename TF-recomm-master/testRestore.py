import tensorflow as tf
import numpy as np
import ops

np.random.seed(13575)

BATCH_SIZE = 1000
USER_NUM = 6040
ITEM_NUM = 3952
DIM = 15
EPOCH_MAX = 100
DEVICE = "/cpu:0"


def clip(x):
    return np.clip(x, 1.0, 5.0)


if __name__ == '__main__':
    user_batch = tf.placeholder(tf.int32, shape=[None], name="id_user")
    item_batch = tf.placeholder(tf.int32, shape=[None], name="id_item")
    rate_batch = tf.placeholder(tf.float32, shape=[None])

    infer, regularizer = ops.inference_svd(user_batch, item_batch, user_num=USER_NUM, item_num=ITEM_NUM, dim=DIM,
                                           device=DEVICE)

    init_op = tf.initialize_all_variables()

    # Add ops to save and restore all the variables.
    saver = tf.train.Saver()

    # Later, launch the model, use the saver to restore variables from disk, and
    # do some work with the model.
    with tf.Session() as sess:
        # Restore variables from disk.
        saver.restore(sess, "/home/test/PycharmProjects/Hackathon-2016/TF-recomm-master/model.ckpt")
        print("Model restored.")

        # Do some work with the model
        pred_batch = sess.run(infer, feed_dict={user_batch: [131], item_batch: [551]})
        pred_batch = clip(pred_batch)
        print("4 => ", pred_batch)
