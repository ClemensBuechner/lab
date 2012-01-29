#! /usr/bin/env python

import os
import platform

from downward.experiment import DownwardExperiment
from downward.checkouts import Translator, Preprocessor, Planner
from downward.reports.absolute import AbsoluteReport
from downward.reports.suite import SuiteReport
from lab.environments import LocalEnvironment, GkiGridEnvironment
from lab.steps import Step
from lab import tools


EXPNAME = 'js-' + os.path.splitext(os.path.basename(__file__))[0]
if platform.node() == 'habakuk':
    EXPPATH = os.path.join('/home/downward/jendrik/experiments/', EXPNAME)
    REPO = '/home/downward/jendrik/downward'
    SUITE = 'IPC11_OPT'
    ENV = GkiGridEnvironment()
else:
    EXPPATH = os.path.join(tools.DEFAULT_EXP_DIR, EXPNAME)
    REPO = '/home/jendrik/projects/Downward/downward'
    SUITE = 'gripper:prob01.pddl'
    ENV = LocalEnvironment()

ATTRIBUTES = ['coverage', 'cost', 'total_time', 'single_solver']

exp = DownwardExperiment(path=EXPPATH, env=ENV, repo=REPO)

# Add report steps
abs_domain_report_file = os.path.join(exp.eval_dir, '%s-abs-d.html' % EXPNAME)
abs_problem_report_file = os.path.join(exp.eval_dir, '%s-abs-p.html' % EXPNAME)
exp.add_step(Step('report-abs-d', AbsoluteReport('domain', attributes=ATTRIBUTES),
                                                 exp.eval_dir, abs_domain_report_file))
exp.add_step(Step('report-abs-p', AbsoluteReport('problem', attributes=ATTRIBUTES),
                                                 exp.eval_dir, abs_problem_report_file))

# Copy the results
exp.add_step(Step.publish_reports(abs_domain_report_file, abs_problem_report_file))

# Compress the experiment directory
exp.add_step(Step.zip_exp_dir(exp))

# Remove the experiment directory
exp.add_step(Step.remove_exp_dir(exp))


def get_exp(suite, configs):
    exp.add_suite(suite)
    for nick, config in configs:
        exp.add_config(nick, config)
    return exp