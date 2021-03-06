import tensorflow as tf


def inference_svd(user_batch, item_batch, user_num, item_num, dim=5, device="/cpu:0"):
    with tf.variable_scope("scop_traning") as scop:
        bias_global = tf.get_variable("bias_global", shape=[])
        w_bias_user = tf.get_variable("embd_bias_user", shape=[user_num])
        w_bias_item = tf.get_variable("embd_bias_item", shape=[item_num])
        w_user = tf.get_variable("embd_user", shape=[user_num, dim],
                                 initializer=tf.truncated_normal_initializer(stddev=0.02))
        w_item = tf.get_variable("embd_item", shape=[item_num, dim],
                                 initializer=tf.truncated_normal_initializer(stddev=0.02))
        with tf.device("/cpu:0"):
            bias_user = tf.nn.embedding_lookup(w_bias_user, user_batch, name="bias_user")
            bias_item = tf.nn.embedding_lookup(w_bias_item, item_batch, name="bias_item")

            embd_user = tf.nn.embedding_lookup(w_user, user_batch, name="embedding_user")
            embd_item = tf.nn.embedding_lookup(w_item, item_batch, name="embedding_item")
        with tf.device(device):
            infer = tf.reduce_sum(tf.mul(embd_user, embd_item), 1)
            infer = tf.add(infer, bias_global)
            infer = tf.add(infer, bias_user)
            infer = tf.add(infer, bias_item, name="svd_inference")
            regularizer = tf.add(tf.nn.l2_loss(embd_user), tf.nn.l2_loss(embd_item), name="svd_regularizer")
        tf.get_variable_scope().reuse_variables()
    return infer, regularizer


def optimiaztion(infer, regularizer, rate_batch, learning_rate=0.1, reg=0.1, device="/cpu:0"):
    with tf.device(device):
        cost_l2 = tf.nn.l2_loss(tf.sub(infer, rate_batch))
        panelty = tf.constant(reg, dtype=tf.float32, shape=[], name="l2")
        cost = tf.add(cost_l2, tf.mul(regularizer, panelty))
        train_op = tf.train.FtrlOptimizer(learning_rate).minimize(cost)
    return cost, train_op
