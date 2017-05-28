import csv
from demographics import not_tas
import matplotlib.pyplot as plt
import numpy as np
from functools import reduce
import scipy.stats as stats

questions = [
    "id",
    "1. I have a positive impression of agent programming in AFABL.",
    "2. I found it easier to write the agents using AFABL’s\n programming constructs compared to bare Scala.",
    "3. I believe that AFABL facilitated more reusable and\nmaintainable code for agents compared to bare Scala.",
    "4. If given the choice, I would choose AFABL over Scala\n for agent programming projects.",
    "5. I found it easier to use AFABL compared to Scala for Task 1.",
    "6. What was it about AFABL that made Task 1 easier or harder?",
    "7. I found it easier to use AFABL compared to Scala for Task 2.",
    "8. What was it about AFABL that made Task 2 easier or harder?"
]

plot_files = [
    "",
    "afabl-impression.png",
    "afabl-easier-overall.png",
    "afabl-better-maintenance.png",
    "afabl-choice.png",
    "afabl-easier-task1.png",
    "",
    "afabl-easier-task2.png",
    ""
]

likert_qs = [1,2,3,4,5,7]
free_resonse_qs = [6,8]

def count(x, xs):
    return reduce(lambda a, b: a + 1 if b == x else a, [0] + xs)

def create_hists(ntas):
    for i in likert_qs:
        data = [row[i] for row in ntas]
        categories = ['1', '2', '3', '4', '5']
        bars = [count(d, data) for d in categories]
        fig = plt.figure()
        plt.bar([0.5, 1.5, 2.5, 3.5, 4.5], bars, tick_label=categories)
        plt.title(questions[i])
        plt.ylabel("Number of respondents")
        plt.xlabel("Strongly disagree 1 - 5  Strongly Agree")
        fig.savefig(plot_files[i])

def details(i, ntas):
    if i in likert_qs:
        return ("\\\\\\begin{center}\n" +
                f"\includegraphics[height=2.25in]{{{plot_files[i]}}}\n"
                + "\\end{center}\n")
    return ("\\begin{itemize}\n" +
            reduce(lambda line1, line2: line1 + line2,
                   [f"\item {response}\n"
                    for response in
                    [row[i] for row in ntas]]) +
            "\\end{itemize}\n")

def qreport(ntas):
    for i in range(len(questions)):
        if i == 0: continue
        question, es = questions[i], details(i, ntas)
        yield question, es


def report(ntas):
    return ("\\begin{enumerate}\n" +
            reduce(lambda line1, line2: line1 + line2,
                   [f"\item {question}\n " +
                    extras
                    for question, extras in qreport(ntas)]) +
            "\\end{enumerate}\n")

def cronback_alphas(ntas):
    constructs = {
        "Satisfaction with Scala": [1, 3],
        "Satisfaction with AFABL": [2, 4],
        "Preference for AFABL": [5, 7]
    }
    cas = {}
    for construct, questions in constructs.items():
        answers = [[row[question] for row in ntas] for question in questions]
        print(answers)
        construct_answers = reduce(lambda x, y: x + y, answers)
        print(construct_answers)
        k = len(questions)
        s2_t = stats.tvar(construct_answers)
        s2_i = [stats.tvar(qas) for qas in answers]
        ca = (k / (k + 1)) * (1 - ((s2_t - sum(s2_i)) / s2_t))
        cas[construct] = ca
    return cas

if __name__=="__main__":
    data = list(csv.reader(open("reflection.csv")))
    ntas = [row for row in data if row[0] in not_tas]
    create_hists(ntas)
    print(report(ntas))
    print(cronback_alphas(ntas))
