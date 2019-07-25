# -*- coding: utf-8 -*-
# @Time    : 2019-07-25 09:30
# @Author  : Yuyoo
# @Email   : sunyuyaoseu@163.com
# @File    : build_tree.py

from utils import Voc


def _remove_duplicate(input):
    return list(set(input))


def build_stage_one_edges(res, graph_voc):
    """
    :param res:
    :param graph_voc:
    :return: edge_idx [[1,2,3],[0,1,0]]
    """
    edge_idx = []
    for sample in res:
        sample_idx = list(map(lambda x: graph_voc.word2idx[x], sample))
        for i in range(len(sample_idx) - 1):
            # only direct children -> ancestor
            edge_idx.append((sample_idx[i+1], sample_idx[i]))
            #
            # # self-loop except leaf node
            # if i != 0:
            #     edge_idx.append((sample_idx[i], sample_idx[i]))

    edge_idx = _remove_duplicate(edge_idx)
    row = list(map(lambda x: x[0], edge_idx))
    col = list(map(lambda x: x[1], edge_idx))
    return [row, col]


def build_stage_two_edges(res, graph_voc):
    """
    :param res:
    :param graph_voc:
    :return: edge_idx [[1,2,3],[0,1,0]]
    """
    edge_idx = []
    for sample in res:
        sample_idx = list(map(lambda x: graph_voc.word2idx[x], sample))
        # only ancestors -> leaf node
        edge_idx.extend([(sample_idx[0], sample_idx[i])
                         for i in range(1, len(sample_idx))])

    edge_idx = _remove_duplicate(edge_idx)
    row = list(map(lambda x: x[0], edge_idx))
    col = list(map(lambda x: x[1], edge_idx))
    return [row, col]


def build_cominbed_edges(res, graph_voc):
    """
    :param res:
    :param graph_voc:
    :return: edge_idx [[1,2,3],[0,1,0]]
    """
    edge_idx = []
    for sample in res:
        sample_idx = list(map(lambda x: graph_voc.word2idx[x], sample))
        for i in range(len(sample_idx) - 1):
            # ancestor <- direct children
            edge_idx.append((sample_idx[i+1], sample_idx[i]))

            # ancestors -> leaf node
            edge_idx.extend([(sample_idx[0], sample_idx[i])
                             for i in range(1, len(sample_idx))])
            #
            #
            # # self-loop except leaf node
            # if i != 0:
            #     edge_idx.append((sample_idx[i], sample_idx[i]))

    edge_idx = _remove_duplicate(edge_idx)
    row = list(map(lambda x: x[0], edge_idx))
    col = list(map(lambda x: x[1], edge_idx))
    return [row, col]


def expand_level2():
    level2 = ['A00-A09', 'A15-A19', 'A20-A28', 'A30-A49', 'A50-A64',
              'A65-A69', 'A70-A74', 'A75-A79', 'A80-A89', 'A90-A99',
              'B00-B09', 'B10', 'B15-B19', 'B20-B24', 'B25-B34', 'B35-B49',
              'B50-B64', 'B65-B83', 'B85-B89', 'B90-B94', 'B95-B97',
              'B99', 'C00-C14', 'C15-C26', 'C30-C39', 'C40-C41',
              'C43-C44', 'C45-C49', 'C50', 'C51-C58', 'C60-C63',
              'C64-C68', 'C69-C72', 'C73-C75', 'C76-C80', 'C7A', 'C7B',
              'C81-C96', 'D00-D09', 'D10-D36', 'D37-D48', 'D3A', 'D49',
              'D50-D53', 'D55-D59', 'D60-D64', 'D65-D69', 'D70-D77', 'D78',
              'D80-D89', 'E00-E07', 'E08-E14', 'E15-E16', 'E20-E35', 'E36',
              'E40-E46', 'E50-E64', 'E65-E68', 'E70-E90', 'F00-F09',
              'F10-F19', 'F20-F29', 'F30-F39', 'F40-F48', 'F50-F59',
              'F60-F69', 'F70-F79', 'F80-F89', 'F90-F98', 'F99',
              'G00-G09', 'G10-G14', 'G20-G26', 'G30-G32', 'G35-G37',
              'G40-G47', 'G50-G59', 'G60-G65', 'G70-G73', 'G80-G83',
              'G89-G99', 'H00-H06', 'H10-H13', 'H15-H22', 'H25-H28',
              'H30-H36', 'H40-H42', 'H43-H45', 'H46-H48', 'H49-H52',
              'H53-H54', 'H55-H59', 'H60-H62', 'H65-H75', 'H80-H83',
              'H90-H95', 'I00-I02', 'I05-I09', 'I10-I15', 'I20-I25',
              'I26-I28', 'I30-I52', 'I60-I69', 'I70-I79', 'I80-I89',
              'I95-I99', 'J00-J06', 'J09-J18', 'J20-J22', 'J30-J39',
              'J40-J47', 'J60-J70', 'J80-J84', 'J85-J86', 'J90-J94',
              'J95-J99', 'K00-K14', 'K20-K31', 'K35-K38', 'K40-K46',
              'K50-K52', 'K55-K64', 'K65-K68', 'K70-K77', 'K80-K87',
              'K90-K95', 'L00-L08', 'L10-L14', 'L20-L30', 'L40-L45',
              'L49-L54', 'L55-L59', 'L60-L75', 'L76', 'L80-L99', 'M00-M25', 'M26-M27',
              'M30-M36', 'M40-M54', 'M60-M79', 'M80-M94', 'M95-M99',
              'N00-N08', 'N10-N16', 'N17-N19', 'N20-N23', 'N25-N29',
              'N30-N39', 'N40-N53', 'N60-N65', 'N70-N77', 'N80-N98',
              'N99', 'O00-O08', 'O09', 'O10-O16', 'O20-O29', 'O30-O48',
              'O60-O77', 'O80-O84', 'O85-O92', 'O94-O99', 'O9A', 'P00-P04',
              'P05-P08', 'P09', 'P10-P15', 'P19-P29', 'P35-P39', 'P50-P61',
              'P70-P74', 'P75-P78', 'P80-P83', 'P84', 'P90-P96', 'Q00-Q07',
              'Q10-Q18', 'Q20-Q28', 'Q30-Q34', 'Q35-Q37', 'Q38-Q45',
              'Q50-Q56', 'Q60-Q64', 'Q65-Q79', 'Q80-Q89', 'Q90-Q99',
              'R00-R09', 'R10-R19', 'R20-R23', 'R25-R29', 'R30-R39',
              'R40-R46', 'R47-R49', 'R50-R69', 'R70-R79', 'R80-R82',
              'R83-R89', 'R90-R94', 'R95-R99', 'S00-S09', 'S10-S19',
              'S20-S29', 'S30-S39', 'S40-S49', 'S50-S59', 'S60-S69',
              'S70-S79', 'S80-S89', 'S90-S99', 'T00-T07', 'T08-T14',
              'T15-T19', 'T20-T32', 'T33-T35', 'T36-T50', 'T51-T65',
              'T66-T78', 'T79', 'T80-T88', 'T90-T98', 'V00-X59',
              'X60-X84', 'X85-Y09', 'Y10-Y34', 'Y35-Y38', 'Y40-Y84',
              'Y85-Y89', 'Y90-Y99', 'Z00-Z13', 'Z14-Z15', 'Z16', 'Z17', 'Z18', 'Z20-Z29', 'Z30-Z39',
              'Z40-Z54', 'Z55-Z65', 'Z66', 'Z67', 'Z68', 'Z69-Z76', 'Z77-Z99', 'U00-U49',
              'U80-U89']

    level2_dict = {}
    for codes in level2:
        tokens = codes.split('-')
        if len(tokens) == 1:
            level2_dict[codes] = codes
        elif tokens[0][0] == tokens[1][0]:
            for j in range(int(tokens[0][1:]), int(tokens[1][1:]) + 1):
                level2_dict[tokens[0][0] + '%02d' % j] = codes
        elif tokens[0][0] != tokens[1][0]:
            # "V01-X59"
            start_ch = tokens[0][0]
            end_ch = tokens[1][0]
            for k in range(ord(end_ch) - ord(start_ch) + 1):
                # 当前字符
                ch = chr(ord(start_ch) + k)
                if ch == end_ch:
                    for j in range(0, int(tokens[1][1:]) + 1):
                        level2_dict[ch + '%02d' % j] = codes
                elif ch == start_ch:
                    for j in range(int(tokens[0][1:]), 100):
                        level2_dict[ch + '%02d' % j] = codes
                else:
                    for j in range(0, 100):
                        level2_dict[ch + '%02d' % j] = codes
    level2_sup = {'M1A': 'M00-M25', 'C4A': 'C43-C44'}
    level2_dict.update(level2_sup)
    return level2_dict


def build_icd10_tree(unique_codes):
    res = []
    graph_voc = Voc()

    root_node = 'icd10_root'
    level3_dict = expand_level2()
    for code in unique_codes:
        level1 = code
        level2 = level1[:3]
        level3 = level3_dict[level2]
        level4 = root_node

        sample = [level1, level2, level3, level4]

        graph_voc.add_sentence(sample)
        res.append(sample)

    return res, graph_voc


def build_atc_tree(unique_codes):
    res = []
    graph_voc = Voc()

    root_node = 'atc_root'
    for code in unique_codes:
        sample = [code] + [code[:i] for i in [4, 3, 1]] + [root_node]

        graph_voc.add_sentence(sample)
        res.append(sample)

    return res, graph_voc