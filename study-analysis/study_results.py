#!/usr/bin/env python

from functools import reduce
import csv
import scipy.stats as stats
import statsmodels.stats.power as power
import sys
from demographics import *



def get_data(file):
    lines = [line[1:] for line in csv.reader(file)]
    return lines[1:]

def results(metric, data, include=lambda participant: True):
    afabl1 = [float(row[1]) for row in data if include(row[0])]
    afabl2 = [float(row[2]) for row in data if include(row[0])]
    scala1 = [float(row[3]) for row in data if include(row[0])]
    scala2 = [float(row[4]) for row in data if include(row[0])]

    task1_ttest = stats.ttest_ind(a = scala1, b = afabl1, equal_var=False)
    task2_ttest = stats.ttest_ind(a = scala2, b = afabl2, equal_var=False)

    afabl1_mean, afabl1_std = stats.trim_mean(afabl1, 0.0), stats.tstd(afabl1)
    afabl2_mean,afabl2_std = stats.trim_mean(afabl2, 0.0), stats.tstd(afabl2)
    scala1_mean, scala1_std = stats.trim_mean(scala1, 0.0), stats.tstd(scala1)
    scala2_mean,scala2_std = stats.trim_mean(scala2, 0.0), stats.tstd(scala2)

    std1 = stats.gmean([stats.tstd(afabl1), stats.tstd(scala1)])
    es1 = abs(afabl1_mean - scala1_mean) / std1 #stats.tstd(afabl1 + scala1)
    pwr1 = power.tt_ind_solve_power(effect_size=es1,
                                    nobs1=len(afabl1),
                                    alpha=0.05,
                                    power=None,
                                    ratio=len(afabl1)/len(scala1))

    std2 = stats.gmean([stats.tstd(afabl2), stats.tstd(scala2)])
    es2 = abs(afabl2_mean - scala2_mean) / std2 #stats.tstd(afabl2 + scala2)
    pwr2 = power.tt_ind_solve_power(effect_size=es2,
                                    nobs1=len(afabl2),
                                    alpha=0.05,
                                    power=None,
                                    ratio=len(afabl2)/len(scala2))

    return (metric, scala1_mean, afabl1_mean, task1_ttest.pvalue, pwr1),\
        (metric, scala2_mean, afabl2_mean, task2_ttest.pvalue, pwr2)

def summary_table(task, metrics):
    """metrics is a
    list[(metric: str, scala_mean: float, afabl_mean: float, pvalue: float, pwr: float)]
    """
    return ("\\begin{tabular}{|l|r|r|r|r|}\\hline\n" +
            f"{task} & Scala Mean & AFABL Mean & p-value & Power \\\\\\hline\n" +
            reduce(lambda line1, line2: line1 + line2,
                   [f"{metric} & {scala_mean:.2f} & {afabl_mean:.2f} & {pvalue:.2f} & {pwr:.2f}\\\\\n"
                    for
                    metric, scala_mean, afabl_mean, pvalue, pwr
                    in metrics]) +
            "\\hline\n" +
            "\\end{tabular}\n")

def compare(data, column, group1, group2):
    """data: list[list[str]] -- 2x2 array of data from csv data file,
    column: int -- the column containing data item on which to compare groups
    group1: str -> bool -- predicate functions on first column (id) determining
                           which rows are included in group1
    group2: str -> bool -- predicate functions on first column (id) determining
                           which rows are included in group2
    """
    g1 = [float(row[column]) for row in data if group1(row[0])]
    g2 = [float(row[column]) for row in data if group2(row[0])]

    g1_mean, g1_std = stats.trim_mean(g1, 0.0), stats.tstd(g1)
    g2_mean, g2_std = stats.trim_mean(g2, 0.0), stats.tstd(g2)

    ttest = stats.ttest_ind(a = g1, b = g2, equal_var=False)
    g1_frac, g2_frac = len(g1) / len(g1 + g2), len(g1) / len(g1 + g2)
    pooled_std = (g1_frac * g1_std) + (g2_frac * g2_std)
    es = abs(g1_mean - g2_mean) / pooled_std
    pwr = power.tt_ind_solve_power(effect_size=es,
                                    nobs1=len(g1),
                                    alpha=0.05,
                                    power=None,
                                    ratio=len(g1)/len(g2))

    return [g1_mean, g2_mean, ttest.pvalue, pwr]

def comparison_table(task, group1, group2, metrics):
    """metrics is a
    list[(metric: str, mean1: float, mean1: float, pvalue: float, pwr: float)]
    """
    return ("\\begin{tabular}{|l|r|r|r|r|}\\hline\n" +
            f"{task} & {group1} Mean & {group2} Mean & p-value & Power\\\\\\hline\n" +
            reduce(lambda line1, line2: line1 + line2,
                   [f"{metric} & {scala_mean:.2f} & {afabl_mean:.2f} & {pvalue:.2f} & {pwr:.2f}\\\\\n"
                    for
                    metric, scala_mean, afabl_mean, pvalue, pwr
                    in metrics]) +
            "\\hline\n" +
            "\\end{tabular}\n")

def compare_all_metrics(column, group1, group2):
    """column is column in csv data file,
    group1 is predicate for group1 measurement,
    group1 is predicate for group1 measurement
    """
    return [["Time in Seconds"] + compare(time_data, column, group1, group2),
            ["Lines of Code"] + compare(loc_data, column, group1, group2),
            ["Complexity"] + compare(comp_data, column, group1, group2),
            ["Performance"] + compare(perf_data, column, group1, group2)]

if __name__=='__main__':
    # [1:] to discard header row
    time_data = list(csv.reader(open('times.csv')))[1:]
    loc_data = list(csv.reader(open('loc.csv')))[1:]
    comp_data = list(csv.reader(open('complexity.csv')))[1:]
    perf_data = list(csv.reader(open('performance.csv')))[1:]

    task1_time, task2_time = results("Time in seconds", time_data)
    task1_loc, task2_loc = results("Lines of code", loc_data)
    task1_comp, task2_comp = results("Complexity", comp_data)
    task1_perf, task2_perf = results("Performance", perf_data)

    task1_results = [task1_time, task1_loc, task1_comp, task1_perf]
    task2_results = [task2_time, task2_loc, task2_comp, task2_perf]

    print("Task 1 Overall Results")
    print(summary_table("Task 1", task1_results))
    print()
    print("Task 2 Overall Results")
    print(summary_table("Task 2", task2_results))

    print("TAs vs. Non-TAs")
    print(comparison_table("Afabl Task 1", "TA", "Non-TA",
                           compare_all_metrics(1, lambda p: p in tas,
                                               lambda p: p in not_tas)))

    print()
    print(comparison_table("Afabl Task 2", "TA", "Non-TA",
                           compare_all_metrics(2, lambda p: p in tas,
                                               lambda p: p in not_tas)))

    print()
    print(comparison_table("Scala Task 1", "TA", "Non-TA",
                           compare_all_metrics(3, lambda p: p in tas,
                                               lambda p: p in not_tas)))

    print()
    print(comparison_table("Scala Task 2", "TA", "Non-TA",
                           compare_all_metrics(2, lambda p: p in tas,
                                               lambda p: p in not_tas)))

    print("Code Novices vs. Code Proficient")
    print(comparison_table("Afabl Task 1", "Coding Novice", "Experienced Coder",
                           compare_all_metrics(1, lambda p: p in code_novices,
                                               lambda p: p in code_proficient)))

    print()
    print(comparison_table("Afabl Task 2", "Coding Novice", "Experienced Coder",
                           compare_all_metrics(2, lambda p: p in code_novices,
                                               lambda p: p in code_proficient)))

    print()
    print(comparison_table("Scala Task 1", "Coding Novice", "Experienced Coder",
                           compare_all_metrics(3, lambda p: p in code_novices,
                                               lambda p: p in code_proficient)))
    print()
    print(comparison_table("Scala Task 2", "Coding Novice", "Experienced Coder",
                           compare_all_metrics(2, lambda p: p in code_novices,
                                               lambda p: p in code_proficient)))

    print("Agent Novices vs. Agent Proficient")
    print(comparison_table("Afabl Task 1", "Agent Novice", "Some Agent Exp",
                           compare_all_metrics(1, lambda p: p in agent_novices,
                                               lambda p: p in agent_proficient)))

    print()
    print(comparison_table("Afabl Task 2", "Agent Novice", "Some Agent Exp",
                           compare_all_metrics(2, lambda p: p in agent_novices,
                                               lambda p: p in agent_proficient)))

    print()
    print(comparison_table("Scala Task 1", "Agent Novice", "Some Agent Exp",
                           compare_all_metrics(3, lambda p: p in agent_novices,
                                               lambda p: p in agent_proficient)))

    print()
    print(comparison_table("Scala Task 2", "Agent Novice", "Some Agent Exp",
                           compare_all_metrics(2, lambda p: p in agent_novices,
                                               lambda p: p in agent_proficient)))
