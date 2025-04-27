import pandas as pd
import api.common.data_type.file as aocdtfo
import api.analytics.evaluation as aocae
import api.analytics.descriptive.correlation.measure as aocadcm
import api.analytics.descriptive.correlation.contingency_table_correction as aocadcc


def get_alpha_list():
    return [0.000001, 0.000002, 0.000005, 0.00001, 0.00002, 0.00005, 0.0001, 0.0002, 0.0005, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5]


def get_basic_correlation_degree_dict(contingency_table_dict):
    n = contingency_table_dict['n11'] + contingency_table_dict['n10'] + contingency_table_dict['n01'] + contingency_table_dict['n00']
    tcp = contingency_table_dict['n11']/n
    ecp = (contingency_table_dict['n11'] + contingency_table_dict['n10'])/n*(contingency_table_dict['n11'] + contingency_table_dict['n01'])/n
    correlation_degree_dict = {}
    correlation_degree_dict['BCPNN'] = aocadcm.get_bcpnn(tcp, ecp, n)
    correlation_degree_dict['AV_OR'] = aocadcm.get_added_value(contingency_table_dict)
    correlation_degree_dict['LV_OR'] = aocadcm.get_probability_difference(tcp, ecp)
    correlation_degree_dict['OR_OR'] = aocadcm.get_odds_ratio(contingency_table_dict)
    correlation_degree_dict['PR_OR'] = aocadcm.get_probability_ratio(tcp, ecp)
    correlation_degree_dict['RR_OR'] = aocadcm.get_relative_risk(contingency_table_dict)
    return correlation_degree_dict


def get_cc_correlation_degree_dict(contingency_table_dict, cc=0.5):
    contingency_table_dict = aocadcc.get_cc_contingency_table_dict(contingency_table_dict, cc)
    basic_correlation_degree_dict = get_basic_correlation_degree_dict(contingency_table_dict)
    correlation_degree_dict = {}
    for key in basic_correlation_degree_dict:
        correlation_degree_dict[key+'_CC'] = basic_correlation_degree_dict[key]
    return correlation_degree_dict


def get_alpha_correlation_degree_dict(contingency_table_dict, alpha):
    n = contingency_table_dict['n11'] + contingency_table_dict['n10'] + contingency_table_dict['n01'] + contingency_table_dict['n00']
    tcp = contingency_table_dict['n11']/n
    ecp = (contingency_table_dict['n11'] + contingency_table_dict['n10'])/n*(contingency_table_dict['n11'] + contingency_table_dict['n01'])/n
    correlation_degree_dict = {}
    correlation_degree_dict['AV_LB' + str(alpha)] = aocadcm.get_added_value_confidence_interval(contingency_table_dict, alpha)[0]
    correlation_degree_dict['LV_LB' + str(alpha)] = aocadcm.get_probability_difference_confidence_interval(tcp, ecp, n, alpha)[0]
    correlation_degree_dict['OR_LB' + str(alpha)] = aocadcm.get_odds_ratio_confidence_interval(contingency_table_dict, alpha)[0]
    correlation_degree_dict['PR_LB' + str(alpha)] = aocadcm.get_probability_ratio_confidence_interval(tcp, ecp, n, alpha)[0]
    correlation_degree_dict['RR_LB' + str(alpha)] = aocadcm.get_relative_risk_confidence_interval(contingency_table_dict, alpha)[0]
    corrected_contingency_table_dict = aocadcc.get_corrected_contingency_table_dict(contingency_table_dict, alpha)
    tcp = corrected_contingency_table_dict['n11']/n
    ecp = (corrected_contingency_table_dict['n11'] + corrected_contingency_table_dict['n10'])/n*(corrected_contingency_table_dict['n11'] + corrected_contingency_table_dict['n01'])/n
    correlation_degree_dict['AV_ECC'+str(alpha)] = aocadcm.get_added_value(corrected_contingency_table_dict)
    correlation_degree_dict['LV_ECC'+str(alpha)] = aocadcm.get_probability_difference(tcp, ecp)
    correlation_degree_dict['OR_ECC'+str(alpha)] = aocadcm.get_odds_ratio(corrected_contingency_table_dict)
    correlation_degree_dict['PR_ECC'+str(alpha)] = aocadcm.get_probability_ratio(tcp, ecp)
    correlation_degree_dict['RR_ECC'+str(alpha)] = aocadcm.get_relative_risk(corrected_contingency_table_dict)
    return correlation_degree_dict


def calculate_correlation():
    raw_df = pd.read_csv(real_data_folder + 'data.csv')
    alpha_list = get_alpha_list()
    matrix = []
    for i in raw_df.index:
        correlation_degree_dict = {}
        contingency_table_dict = {'n11': raw_df.loc[i, 'n11'], 'n10': raw_df.loc[i, 'n10'], 'n01': raw_df.loc[i, 'n01'], 'n00': raw_df.loc[i, 'n00']}
        correlation_degree_dict.update(get_basic_correlation_degree_dict(contingency_table_dict))
        correlation_degree_dict.update(get_cc_correlation_degree_dict(contingency_table_dict))
        for alpha in alpha_list:
            correlation_degree_dict.update(get_alpha_correlation_degree_dict(contingency_table_dict, alpha))
        matrix.append(correlation_degree_dict)
    correlation_df = pd.DataFrame(matrix)
    result_df = pd.concat([raw_df, correlation_df], axis=1)
    aocdtfo.save_pickle_data(result_df, real_data_folder + 'result.pk', True)


def evaluate():
    result_df = aocdtfo.load_pickle_data(real_data_folder + 'result.pk')
    attribute_name_list = list(result_df.columns)
    result_dict = {}
    for attribute_name in attribute_name_list[8:]:
        result_df = result_df.sort_values(by=attribute_name, ascending=False)
        relevance_score_list = list(result_df[attribute_name_list[7]])
        result_dict[attribute_name] = aocae.get_ranking_quality_score(relevance_score_list)
    aocdtfo.save_dict_as_json_file(result_dict, real_data_folder + 'rsq.json')


real_data_folder = 'data/real/AKI/'
calculate_correlation()
evaluate()
