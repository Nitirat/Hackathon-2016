from pyramid.view import (
    view_config,
    view_defaults
    )
import json
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


@view_defaults(route_name='hello')
class TutorialViews(object):
    def __init__(self, request):
        self.request = request
        self.view_name = 'TutorialViews'

    # Retrieving /howdy/first/last the first time
    @view_config(renderer='hello.pt')
    def hello(self):
        return {'page_title': 'Hello View'}

    # Posting to /howdy/first/last via the "Edit" submit button
    @view_config(request_method='POST', renderer='edit.pt')
    def rate(self):
        user = int(self.request.params['user'])
        movie = self.request.params['movie']
        with open('movies.json') as data_file:
            dataMovie = json.load(data_file)
        movieNum = dataMovie[movie]
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
            pred_batch = sess.run(infer, feed_dict={user_batch: [user], item_batch: [movieNum]})
            pred_batch = clip(pred_batch)
            print("4 => ", pred_batch)
        return {'page_title': 'Edit View', 'movieName': movie, 'pred': pred_batch[0]}
