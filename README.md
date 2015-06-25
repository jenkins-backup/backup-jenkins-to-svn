##每日自动备份JENKINS_HOME至版本控制系统SVN

**Jenkins**是一个可扩展的开源的持续集成工具，也是当下最流行的持续集成工具。

###Jenkins主要功能###
- 易于安装(Easy installation)
- 易于配置(Easy configuration)
- 变更集支持(Change set support)
- 永久链接(Permanent links)
- RSS/Email/IM集成(RSS/E-mail/IM Integration)
- 事后标签(After-the-fact tagging)
- JUnit/TestNG测试报告(JUnit/TestNG test reporting)
- 分布式构建(Distributed builds)
- 文件指纹打印(File fingerprinting)
- 插件支持(Plugin Support)

其中插件支持使得Jenkins可定制、可扩展。

###JENKINS_HOME目录结构###
Jenkins的相关文件都存放在文件系统中，而JENKINS_HOME主要用来存放这些文件的，如系统配置文件、插件、每个job的配置文件等。

JENKINS_HOME目录结构如下：
<pre>
 +- config.xml     (jenkins root configuration)
 +- *.xml          (other site-wide configuration files)
 +- userContent    (files in this directory will be served under your http://server/userContent/)
 +- fingerprints   (stores fingerprint records)
 +- plugins        (stores plugins)
 +- jobs
     +- [JOBNAME]      (sub directory for each job)
         +- config.xml     (job configuration file)
         +- latest         (symbolic link to the last successful build)
         +- builds
             +- [BUILD_ID]     (for each build)
                 +- build.xml      (build result summary)
                 +- log            (log file)
                 +- changelog.xml  (change log)
+- workspace      (working directory for the version control system)
</pre>

无论是Jenkins的升级、迁移还是备份、恢复都需要对JENKINS_HOME的操作，而备份Jenkins只需备份JENKINS_HOME即可。

在JENKINS_HOME中，有些目录是无需备份的，如：workspace。

因为workspace是版本控制系统的工作目录，这个目录下的相关文件都来自版本控制系统，都可以从版本控制系统获取。

###Jenkins备份插件###
Jenkins是可扩展的，有上千个插件可供选择，在备份这方面有两个插件可供选择：thinBackup plugin和backup plugin。

thinBackup plugin可以自动备份全局的和job的指定配置文件（不包括archive和workspace）。

backup plugin可以备份JENKINS_HOME，可以选择是否备份workspace、builds history、maven atifacts archives、fingerprints等。

thinBackup plugin和backup plugin不同：

1. bakup plugin只能手动触发备份，thinBackup plugin可以定期自动备份。
2. bakup plugin可以备份JENKINS_HOME，可以选择哪些内容是否需要备份（如workspace、builds history等）， thinBackup plugin只备份最重要的信息（全局的和job的指定配置文件）。

上面两个备份插件总体来说满足一般的需求了。

通常持续集成服务器资源专用，Jenkins安装在专门的服务器上（如：虚拟机）。
但是如果虚拟机挂了，短时间内难以恢复，自然也无法从备份恢复了（上面两个插件都是本机备份）。

所以为了应对这种情况的发生，应该把JENKINS_HOME备份到其他地方。

###将JENKINS_HOME备份到版本控制系统###
笔者选择将JENKINS_HOME备份到版本控制系统：

1. 版本控制系统选择的是SVN
2. 每晚自动备份JENKINS_HOME至SVN
3. 此外，通过SVN和可以对比两个revision之间的差异，查看变更，便于追溯

备份前的初始化步骤如下：

1. 在SVN版本库上新建一个目录如JENKINS_HOME_BAK
2. 将JENKINS_HOME_BAK检出(checkout)到Jenkins服务器上的某个位置，如E:/JENKINS_HOME_BAK

具体的备份步骤如下：

1. 拷贝JENKINS_HOME到JENKINS_HOME_BAK
2. 将JENKINS_HOME_BAK中未纳入版本控制的文件或目录纳入到版本控制（svn add操作）
3. 遍历JENKINS_HOME_BAK，如果其中的文件或目录不在JENKINS_HOME中，对其执行svn delete操作
4. 最后提交到SVN版本库（svn ci操作）

上述步骤，如果第2步是手动，理论上是难以实现的，所以如果是手动备份，可以不执行第5步操作
而这些流程化的步骤，如果手动操作，异常繁琐、重复，懒人通常懒的做重复性的事，所以应该将其自动化。

关于自动化备份脚本，主要是实现上面的4个步骤：

1. 对于第1步，使用Ant脚本实现
	* Ant脚本不仅仅用于构建，还可以用于构建之外
	* Ant的语法很灵活，有很多task可供选择
	* 拷贝操作使用了Ant copy task，可以使用fileset的excludes来排除无需拷贝的文件或目录（如workspace），很方便
	* Ant copy task可以增量copy

2. 对于第2步、第3步和第4步，使用Python+svn client comands实现
	* 选择Python是因为最近在不断学习Python
	* 选择svn client commands而不是pysvn是因为没有在windows上安装好pysvn，于是用svn client commands代替

此外，自动化备份，可以在Jenkins上创建一个job专门用来定时备份JENKINS_HOME

具体的实现脚本见：

- oscgit:<a href="http://git.oschina.net/donhui/JENKINS_HOME_BAKCUP" target="_blank">donhui/JENKINS_HOME_BAKCUP</a>
- github:<a href="https://github.com/donhui/JENKINS_HOME_BACKUP" target="_blank">donhui/JENKINS_HOME_BAKCUP</a>

补充说明，上述所使用到的工具及环境：

	* Jenkins 1.592
	* Python 2.7.8
	* svn client commands（Windows下安装TortoiseSVN时需要手动选择安装）
	* Ant 1.8.1
	* 在windows环境和linux环境都验证测试过
	* 在svn client 1.7和1.7以上环境都验证测试过



###参考###
- <a href="https://wiki.jenkins-ci.org/display/JENKINS/Meet+Jenkins" target="_blank">https://wiki.jenkins-ci.org/display/JENKINS/Meet+Jenkins</a>
- <a href="https://wiki.jenkins-ci.org/display/JENKINS/Administering+Jenkins" target="_blank">https://wiki.jenkins-ci.org/display/JENKINS/Administering+Jenkins</a>
- <a href="https://wiki.jenkins-ci.org/display/JENKINS/thinBackup" target="_blank">https://wiki.jenkins-ci.org/display/JENKINS/thinBackup</a>
- <a href="https://wiki.jenkins-ci.org/display/JENKINS/Backup+Plugin" target="_blank">https://wiki.jenkins-ci.org/display/JENKINS/Backup+Plugin</a>
- <a href="http://blog.csdn.net/spare_h/article/details/6677435" target="_blank">http://blog.csdn.net/spare_h/article/details/6677435</a>
- <a href="http://www.cnblogs.com/zz0412/p/jenkins_jj_08.html" target="_blank">http://www.cnblogs.com/zz0412/p/jenkins_jj_08.html</a>



























