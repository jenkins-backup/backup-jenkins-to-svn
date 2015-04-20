# -*- coding: utf-8 -*-
import os
import svncli
import logging


'''
    每日自动备份JENKINS_HOME到SVN：
    1、调用ant命令copy from JENKINS_HOME_PATH to JENKINS_HOME_BAK_PATH
    2、批量将JENKINS_HOME_BAK_PATH中不在版本控制下的目录或文件添加到版本控制
    3、遍历JENKINS_HOME_BAK_PATH，如果其中的文件或目录不在JENKINS_HOME中，对其执行svn delete操作
    4、将JENKINS_HOME_BAK_PATH提交到SVN
    使用到的svn相关命令有：status、add、delete、ci
'''


def main():
    # 从jenkins_config.properties中读取JENKINS_HOME_PATH、JENKINS_HOME_BAK_PATH
    global JENKINS_HOME_BAK_PATH
    global JENKINS_HOME_PATH
    jenkins_config = "jenkins_config.properties"
    with open(jenkins_config, "r") as f:
        for line in f.readlines():
            tmp = line.split("=", 1)
            if "JENKINS_HOME_PATH" == tmp[0].strip():
                JENKINS_HOME_PATH = tmp[1].strip()
            elif "JENKINS_HOME_BAK_PATH" == tmp[0].strip():
                JENKINS_HOME_BAK_PATH = tmp[1].strip()
            else:
                pass

    # 1、调用ant命令copy JENKINS_HOME_PATH to JENKINS_HOME_BAK_PATH
    os.system("ant -f backup.xml")

    # svn_status_file用来存储svn status命令的输出结果
    svn_status_file = "svn_status.txt"

    # 2、批量将JENKINS_HOME_BAK_PATH中不在版本控制下的目录或文件添加到版本控制
    # 2.1执行svn status命令，将输出结果定向到svn_status.txt中
    svncli.status(JENKINS_HOME_BAK_PATH, svn_status_file)

    # 2.2读取并解析svn_status.txt，将不在版本控制下的目录或文件添加到版本控制，未在版本控制下的文件或目录所在的行会以“?”开头
    with open(svn_status_file, "r") as f:
        for line in f.readlines():
            if line.startswith("?"):
                # 去掉字符串前面的"?"和空格
                line = line.replace("?", "").strip()
                # 将不在版本控制下的目录或文件添加到版本控制
                svncli.add(line)

    # 3、遍历JENKINS_HOME_BAK_PATH，如果其中的文件或目录不在JENKINS_HOME中，对其执行svn delete操作
    for dirpath, dirs, files in os.walk(JENKINS_HOME_BAK_PATH):
        # 3.1、遍历JENKINS_HOME_BAK_PATH，如果其中的文件不在JENKINS_HOME中，对其执行svn delete操作
        for f in files:
            # JENKINS_HOME_BAK_PATH下的文件
            bakfile = os.path.join(dirpath, f)
            # 与JENKINS_HOME_BAK_PATH下的文件相对应的JENKINS_HOME_PATH下的文件
            orginfile = os.path.join(dirpath.replace(JENKINS_HOME_BAK_PATH, JENKINS_HOME_PATH), f)
            if bakfile.startswith(JENKINS_HOME_BAK_PATH + ".svn"):
                # 忽略.svn目录及其下的目录或文件
                pass
            else:
                if not os.path.exists(orginfile):
                    # 对不在JENKINS_HOME_PATH下的文件执行svn delete操作
                    logging.debug(orginfile + " is not exists.")
                    svncli.delete_from_wc(bakfile)
        # 3.2、遍历JENKINS_HOME_BAK_PATH，如果其中的目录不在JENKINS_HOME中，对其执行svn delete操作
        for bak_dir in dirs:
            # JENKINS_HOME_BAK_PATH下的目录
            bakdir = os.path.join(dirpath, bak_dir)
            # 与JENKINS_HOME_BAK_PATH下的目录相对应的JENKINS_HOME_PATH下的目录
            orgindir = os.path.join(dirpath.replace(JENKINS_HOME_BAK_PATH, JENKINS_HOME_PATH), bak_dir)
            if bakdir.startswith(JENKINS_HOME_BAK_PATH + ".svn"):
                # 忽略.svn目录及其下的目录或文件
                pass
            else:
                if not os.path.exists(orgindir):
                    # 对不在JENKINS_HOME_PATH下的目录执行svn delete操作
                    svncli.delete_from_wc(bakdir)

    # 4、将JENKINS_HOME_BAK_PATH提交到SVN
    log_message = "daily backup JENKINS_JOME"
    svncli.commit(JENKINS_HOME_BAK_PATH, log_message)

if __name__ == "__main__":
    main()
