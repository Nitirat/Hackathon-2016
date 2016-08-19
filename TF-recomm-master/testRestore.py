import tensorflow as tf
import numpy as np
import ops

USER_NUM = 6040
ITEM_NUM = 3952
DIM = 15
DEVICE = "/cpu:0"


def clip(x):
    return np.clip(x, 1.0, 5.0)


def restoreModel():
    # Add ops to save and restore all the variables.
    saver = tf.train.Saver()

    # Later, launch the model, use the saver to restore variables from disk, and
    # do some work with the model.
    with tf.Session() as sess:
        # Restore variables from disk.
        saver.restore(sess, "/tmp/model.ckpt")
        print("Model restored.")
        # Do some work with the model
        print(sess)


user_batch = tf.placeholder(tf.int32, shape=[None], name="id_user")
item_batch = tf.placeholder(tf.int32, shape=[None], name="id_item")
rate_batch = tf.placeholder(tf.float32, shape=[None])

infer, regularizer = ops.inference_svd(user_batch, item_batch, user_num=USER_NUM, item_num=ITEM_NUM, dim=DIM, device=DEVICE)
init_op = tf.initialize_all_variables()
with tf.Session() as sess:
    sess.run(init_op)

    restoreModel()

    pred_batch = sess.run(infer, feed_dict={user_batch: [984], item_batch: [1085]})
    print("pred_batch : ", pred_batch)
    pred_batch = clip(pred_batch)
    print("clip(pred_batch) : ", pred_batch)