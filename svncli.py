#!Python.exe
# -*- coding: utf-8 -*-

import sys
import os
import logging

# 设置日志级别为DEBUG
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# merge function
def merge(src, dst):
    merge_command = 'svn merge -r 1:HEAD "%s" "%s"' % (src, dst)
    logging.debug(merge_command)
    os.system(merge_command)
    return


# copy function
def copy(src, dst):
    copy_command = 'svn copy "%s" "%s"' % (src, dst)
    logging.debug(copy_command)
    os.system(copy_command)
    return


# update function
# wc_dir:the dir of working copy
def update(wc_dir):
    update_command = 'svn up "%s"' % wc_dir
    logging.debug(update_command)
    os.system(update_command)
    return


# commit function
# wc_dir:the dir of working copy
def commit(wc_dir, log_message):
    commit_command = 'svn ci -m "%s" "%s"' % (log_message, wc_dir)
    logging.debug(commit_command)
    os.system(commit_command)
    return


# add function
def add(path):
    add_command = 'svn add "%s"' % path
    logging.debug(add_command)
    os.system(add_command)
    return


# status function
# wc_dir:the dir of working copy
# output_file: to store the output of svn st command
def status(wc_dir, output_file):
    status_command = 'svn st "%s" > "%s"' % (wc_dir, output_file)
    logging.debug(status_command)
    os.system(status_command)
    return


# delete_from_wc function : delete from path (woking copy)
def delete_from_wc(path):
    delete_command = 'svn delete "%s"' % path
    logging.debug(delete_command)
    os.system(delete_command)
    return


# delete_from_repo function : delete from url (repository)
def delete_from_repo(url, log_message):
    delete_command = 'svn delete -m "%s" "%s"' % (log_message, url)
    logging.debug(delete_command)
    os.system(delete_command)
    return