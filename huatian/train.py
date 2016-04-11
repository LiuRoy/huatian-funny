# -*- coding=utf8 -*-
"""
    构建决策树
"""
from __future__ import division
from math import log
import operator
import matplotlib.pyplot as plt
from extension import mongo_collection, SALARY, EDUCATION, SATISFY

decision_node = dict(boxstyle="sawtooth", fc="0.8")
leaf_node = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")


def load_data():
    """从mongo导入数据"""
    data = []
    for user in mongo_collection.find({"appearance": {"$exists": True},
                                       "satisfy": {"$exists": True}}):
        data.append([user.get('appearance', 0),
                     user.get('age', u'0'),
                     user.get('height', u'0'),
                     SALARY.get(user.get('salary', u'0'), u'--'),
                     EDUCATION.get(user.get('education', u'0'), u'--'),
                     SATISFY[user['satisfy']]])
    labels = [u'颜值', u'年龄', u'身高', u'工资', u'学历']
    return data, labels


def majority_count(class_list):
    class_count = {}
    for vote in class_list:
        class_count[vote] = class_count.get(vote, 0) + 1
    sorted_class_count = sorted(class_count.iteritems(),
                                key=operator.itemgetter(1), reverse=True)
    return sorted_class_count[0][0]


def calc_shannon_ent(data_set):
    num_entries = len(data_set)
    label_counts = {}
    for feat_vec in data_set:
        current_label = feat_vec[-1]
        label_counts[current_label] = label_counts.get(current_label, 0) + 1
    shannon_ent = 0.0
    for key in label_counts:
        prob = float(label_counts[key]) / num_entries
        shannon_ent -= prob * log(prob, 2)
    return shannon_ent


def split_data_set(data_set, axis, value):
    ret_data_set = []
    for feat_vec in data_set:
        if feat_vec[axis] == value:
            reduced_feat_vec = feat_vec[:axis]
            reduced_feat_vec.extend(feat_vec[axis+1:])
            ret_data_set.append(reduced_feat_vec)
    return ret_data_set


def choose_best_feature_to_split(data_set):
    num_features = len(data_set[0]) - 1
    base_entropy = calc_shannon_ent(data_set)
    best_info_gain, best_feature = 0.0, -1
    for i in range(num_features):
        feat_fist = [example[i] for example in data_set]
        unique_vals = set(feat_fist)
        new_entropy = 0.0
        for value in unique_vals:
            sub_data_set = split_data_set(data_set, i, value)
            prob = len(sub_data_set) / len(data_set)
            new_entropy += prob * calc_shannon_ent(sub_data_set)
        info_gain = base_entropy - new_entropy
        if info_gain > best_info_gain:
            best_info_gain = info_gain
            best_feature = i
    return best_feature


def create_tree(data_set, labels):
    """生成决策树"""
    class_list = [example[-1] for example in data_set]
    if class_list.count(class_list[0]) == len(class_list): 
        return class_list[0]
    if len(data_set[0]) == 1:
        return majority_count(class_list)
    best_feat = choose_best_feature_to_split(data_set)
    best_feat_label = labels[best_feat]
    my_tree = {best_feat_label:{}}
    del(labels[best_feat])
    feat_values = [example[best_feat] for example in data_set]
    unique_vals = set(feat_values)
    for value in unique_vals:
        sub_labels = labels[:]
        my_tree[best_feat_label][value] = \
            create_tree(split_data_set(data_set, best_feat, value), sub_labels)
    return my_tree


def get_num_leafs(my_tree):
    num_leafs = 0
    first_str = my_tree.keys()[0]
    second_dict = my_tree[first_str]
    for _, val in second_dict.iteritems():
        if isinstance(val, dict):
            num_leafs += get_num_leafs(val)
        else:
            num_leafs += 1
    return num_leafs


def get_tree_depth(my_tree):
    max_depth = 0
    first_str = my_tree.keys()[0]
    second_dict = my_tree[first_str]
    for _, val in second_dict.iteritems():
        if isinstance(val, dict):
            this_depth = 1 + get_tree_depth(val)
        else:
            this_depth = 1
        if this_depth > max_depth:
            max_depth = this_depth
    return max_depth


def plot_node(node_txt, center_pt, parent_pt, node_type):
    create_plot.ax1.annotate(
        node_txt, xy=parent_pt,  xycoords='axes fraction',
        xytext=center_pt, textcoords='axes fraction',
        va="center", ha="center", bbox=node_type, arrowprops=arrow_args)


def plot_mid_text(cntr_pt, parent_pt, txt_string):
    x_mid = (parent_pt[0]-cntr_pt[0])/2.0 + cntr_pt[0]
    y_mid = (parent_pt[1]-cntr_pt[1])/2.0 + cntr_pt[1]
    create_plot.ax1.text(x_mid, y_mid, txt_string, va="center",
                         ha="center", rotation=30)


def plot_tree(my_tree, parent_pt, node_txt):
    num_leafs = get_num_leafs(my_tree)
    first_str = my_tree.keys()[0]
    cntr_pt = (plot_tree.xOff + (2.0 + num_leafs) / 2.0 / plot_tree.totalW, plot_tree.yOff)
    plot_mid_text(cntr_pt, parent_pt, node_txt)
    plot_node(first_str, cntr_pt, parent_pt, decision_node)
    second_dict = my_tree[first_str]
    plot_tree.yOff = plot_tree.yOff - 1.0 / plot_tree.totalD

    for key, val in second_dict.iteritems():
        if isinstance(val, dict):
            plot_tree(val, cntr_pt, unicode(key))
        else:
            plot_tree.xOff = plot_tree.xOff + 1.0 / plot_tree.totalW
            plot_node(unicode(val), (plot_tree.xOff, plot_tree.yOff), cntr_pt, leaf_node)
            plot_mid_text((plot_tree.xOff, plot_tree.yOff), cntr_pt, unicode(key))

    plot_tree.yOff = plot_tree.yOff + 1.0 / plot_tree.totalD


def create_plot(in_tree):
    """"生成图像"""
    fig = plt.figure(1, figsize=(25, 10), facecolor='white')
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    create_plot.ax1 = plt.subplot(111, frameon=False, **axprops)
    plot_tree.totalW = float(get_num_leafs(in_tree))
    plot_tree.totalD = float(get_tree_depth(in_tree))
    plot_tree.xOff = -0.5 / plot_tree.totalW
    plot_tree.yOff = 1.0
    plot_tree(in_tree, (0.5, 1.0), '')
    plt.show()


def compress_tree(my_tree):
    """压缩决策树"""
    first_str = my_tree.keys()[0]
    inner_dict = my_tree[first_str]

    copy_dict = {}
    for key, val in inner_dict.items():
        if not isinstance(val, dict):
            if val not in copy_dict:
                copy_dict[val] = [unicode(key)]
            else:
                copy_dict[val].append(unicode(key))

    copy_dict = {u','.join(val): unicode(key) for key, val in copy_dict.items()}
    for key, val in inner_dict.items():
        if isinstance(val, dict):
            compress_tree(val)
        else:
            inner_dict.pop(key)

    inner_dict.update(copy_dict)


if __name__ == '__main__':
    data_set, labels = load_data()
    result = create_tree(data_set, labels)
    compress_tree(result)
    create_plot(result)
