from __future__ import absolute_import
from ctr.algorithm import ffm
from ctr.common import utility
import sys

if __name__ == "__main__":
    feature_map_file = "feature_map_v3.json"
    train_data_file = "app_train_features_v3.csv"
    test_data_file = "app_test_features_v3.csv"
    if len(sys.argv) > 1:
        eta, _lambda, k, iter = sys.argv[1:5]
        eta, _lambda, k, iter = float(eta), float(_lambda), int(k), int(iter)
        feature_map = utility.HashFeatureMap.load(feature_map_file)
    else:
        eta, _lambda, k, iter = 0.03, 0.00002, 4, 15
    if len(sys.argv) > 5 and sys.argv[5] == "dummy":
        print "Use dummy features"
        feature_map_file = "feature_map_v3_dummy.json"
        train_data_file = "app_train_features_v3_dummy.csv"
        test_data_file = "app_test_features_v3_dummy.csv"
        feature_map = utility.DummyFeatureMap.load(feature_map_file)
    train_fs = utility.FeatureStream(feature_map, utility.get_date_file_path(train_data_file))
    #model_file = "app_model_ffm_4_id_{0}_{1}.json".format(eta, _lambda)
    print "training......"
    alg = ffm.FFM(train_fs.feature_count(), train_fs.field_count(), k)
    pre_logloss = 0
    for i in xrange(iter):
        train_fs.reset()
        print "iter {0}......".format(i)
        #alg.load_model(utility.get_date_file_path(model_file))
        log_loss = alg.train(train_fs, _lambda, eta, report_interval=-1)
        #alg.dump_model(utility.get_date_file_path(model_file))
        print "testing......"
        test_fs = utility.FeatureStream(feature_map, utility.get_date_file_path(test_data_file))
        alg.test(test_fs, report_interval=-1)
        if pre_logloss > 0 and abs(float(log_loss - pre_logloss)) / pre_logloss < 0.001:
            break