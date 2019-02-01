import direct
from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
from direct.showbase.MessengerGlobal import messenger
from direct.p3d.PackageInstaller import PackageInstaller
from direct.task.TaskManagerGlobal import taskMgr
import sys
import time
import os
import subprocess
import __builtin__


class WebLauncherBase(DirectObject):
    notify = directNotify.newCategory('WebLauncherBase')
    PandaErrorCodeKey = 'PANDA_ERROR_CODE'
    NewInstallationKey = 'IS_NEW_INSTALLATION'
    LastLoginKey = 'LAST_LOGIN'
    UserLoggedInKey = 'USER_LOGGED_IN'
    PaidUserLoggedInKey = 'PAID_USER_LOGGED_IN'
    ReferrerKey = 'REFERRER_CODE'
    PeriodTimeRemainingKey = 'PERIOD_TIME_REMAINING'
    PeriodNameKey = 'PERIOD_NAME'
    SwidKey = 'SWID'
    DISLTokenKey = 'DISLTOKEN'
    ProxyServerKey = 'PROXY_SERVER'
    ProxyDirectHostsKey = 'PROXY_DIRECT_HOSTS'
    logPrefix = ''

    class PhaseData:

        def __init__(self, phase):
            self.phase = phase
            self.percent = 0
            self.complete = False
            self.postProcessCallbacks = []

        def markComplete(self):
            self._PhaseData__nextCallback(None, 'default')

        def _PhaseData__nextCallback(self, currentCallback, currentTaskChain):
            if currentCallback:
                currentCallback()

            if self.postProcessCallbacks:
                (callback, taskChain) = self.postProcessCallbacks[0]
                del self.postProcessCallbacks[0]
                if taskChain != currentTaskChain:
                    print 'switching to %s' % taskChain
                    taskMgr.add(
                        self._PhaseData__nextCallback,
                        'phaseCallback-%s' %
                        self.phase,
                        taskChain=taskChain,
                        extraArgs=[
                            callback,
                            taskChain])
                    return None

            self.complete = True
            messenger.send(
                'phaseComplete-%s' %
                self.phase, taskChain='default')

    def __init__(self, appRunner):
        self.appRunner = appRunner
        __builtin__.launcher = self
        appRunner.exceptionHandler = self.exceptionHandler
        gameInfoStr = appRunner.getToken('gameInfo')
        if gameInfoStr:
            self.gameInfo = appRunner.evalScript(
                gameInfoStr, needsResponse=True)
        else:

            class DummyGameInfo:
                pass

            self.gameInfo = DummyGameInfo()
        self.phasesByPackageName = {}
        self.phaseData = {}
        self.allPhasesComplete = False
        for (phase, packageName) in self.LauncherPhases:
            self.phasesByPackageName[packageName] = phase
            self.phaseData[phase] = self.PhaseData(phase)
            self.acceptOnce('phaseComplete-%s' %
                            phase, self._WebLauncherBase__gotPhaseComplete)

        self.packageInstaller = None
        self.started = False
        self.setPandaErrorCode(0)
        self.setServerVersion('dev')
        self.WIN32 = os.name == 'nt'
        if self.WIN32:
            if sys.getwindowsversion()[3] == 2:
                pass
            self.VISTA = sys.getwindowsversion()[0] == 6
        else:
            self.VISTA = 0
        self.launcherFileDbHash = HashVal()
        self.serverDbFileHash = HashVal()
        self.testServerFlag = self.getTestServerFlag()
        self.notify.info('isTestServer: %s' % self.testServerFlag)
        print '\n\nStarting %s...' % self.GameName
        print 'Current time: ' + time.asctime(time.localtime(time.time())) + ' ' + time.tzname[0]
        print 'sys.argv = ', sys.argv
        print 'tokens = ', appRunner.tokens
        print 'gameInfo = ', self.gameInfo
        cwd = os.getcwd()
        os.chdir(appRunner.logDirectory.toOsSpecific())
        self.notify.info('chdir: %s' % appRunner.logDirectory.toOsSpecific())
        hwprofile = 'hwprofile.log'
        command = None
        if sys.platform == 'darwin':
            command = '/usr/sbin/system_profiler >%s' % hwprofile
            shell = True
        elif sys.platform == 'linux':
            command = '(cat /proc/cpuinfo; cat /proc/meminfo; /sbin/ifconfig -a) >%s' % hwprofile
            shell = True
        else:
            command = 'dxdiag /t %s' % hwprofile
            shell = False
        self.notify.info(command)

        try:
            self.hwpipe = subprocess.Popen(command, shell=shell)
        except OSError:
            self.notify.warning('Could not run hwpipe command')
            self.hwpipe = None

        os.chdir(cwd)
        if self.hwpipe:
            self.notify.info('hwpipe pid: %s' % self.hwpipe.pid)
            taskMgr.add(self._WebLauncherBase__checkHwpipe, 'checkHwpipe')

    def _WebLauncherBase__gotPhaseComplete(self):
        if self.allPhasesComplete:
            return None

        for phaseData in self.phaseData.values():
            if not phaseData.complete:
                return None
                continue

        self.allPhasesComplete = True
        print 'launcherAllPhasesComplete'
        messenger.send('launcherAllPhasesComplete', taskChain='default')

    def _WebLauncherBase__checkHwpipe(self, task):
        if self.hwpipe.poll() is None:
            return task.cont

        self.notify.info('hwpipe finished: %s' % self.hwpipe.returncode)
        return task.done

    def isDummy(self):
        return False

    def setRegistry(self, key, value):
        self.notify.info('DEPRECATED setRegistry: %s = %s' % (key, value))

    def getRegistry(self, key):
        self.notify.info('DEPRECATED getRegistry: %s' % key)

    def getValue(self, key, default=None):
        return getattr(self.gameInfo, key, default)

    def setValue(self, key, value):
        setattr(self.gameInfo, key, value)

    def getVerifyFiles(self):
        return config.GetInt('launcher-verify', 0)

    def getTestServerFlag(self):
        return self.getValue('IS_TEST_SERVER', 0)

    def getGameServer(self):
        return self.getValue('GAME_SERVER', '')

    def getPhaseComplete(self, phase):
        return self.phaseData[phase].complete

    def getPercentPhaseComplete(self, phase):
        return self.phaseData[phase].percent

    def addPhasePostProcess(self, phase, func, taskChain='default'):
        if self.getPhaseComplete(phase):
            func()
            return None

        self.phaseData[phase].postProcessCallbacks.append((func, taskChain))

    def getBlue(self):
        pass

    def getPlayToken(self):
        pass

    def getDISLToken(self):
        DISLToken = self.getValue(self.DISLTokenKey)
        if DISLToken == 'NO DISLTOKEN':
            DISLToken = None

        return DISLToken

    def startDownload(self):
        self.packageInstaller = WebLauncherInstaller(self)
        for (phase, packageName) in self.LauncherPhases:
            self.packageInstaller.addPackage(packageName)

        self.packageInstaller.donePackages()

    def isTestServer(self):
        return self.testServerFlag

    def recordPeriodTimeRemaining(self, secondsRemaining):
        self.setValue(self.PeriodTimeRemainingKey, int(secondsRemaining))

    def recordPeriodName(self, periodName):
        self.setValue(self.PeriodNameKey, periodName)

    def recordSwid(self, swid):
        self.setValue(self.SwidKey, swid)

    def getGoUserName(self):
        return self.goUserName

    def setGoUserName(self, userName):
        self.goUserName = userName

    def setPandaWindowOpen(self):
        pass

    def setPandaErrorCode(self, code):
        self.pandaErrorCode = code
        self.gameInfo.pandaErrorCode = code

    def getPandaErrorCode(self):
        return self.pandaErrorCode

    def setDisconnectDetailsNormal(self):
        self.disconnectCode = 0
        self.disconnectMsg = 'normal'
        self.gameInfo.disconnectCode = self.disconnectCode
        self.gameInfo.disconnectMsg = self.disconnectMsg

    def setDisconnectDetails(self, newCode, newMsg):
        if newCode is None:
            newCode = 0

        self.disconnectCode = newCode
        self.disconnectMsg = newMsg
        self.gameInfo.disconnectCode = self.disconnectCode
        self.gameInfo.disconnectMsg = self.disconnectMsg
        self.notify.warning(
            'disconnected with code: %s - %s' %
            (self.gameInfo.disconnectCode,
             self.gameInfo.disconnectMsg))

    def setServerVersion(self, version):
        self.ServerVersion = version
        self.gameInfo.ServerVersion = version

    def getServerVersion(self):
        return self.ServerVersion

    def getIsNewInstallation(self):
        result = self.getValue(self.NewInstallationKey, 1)
        result = base.config.GetBool('new-installation', result)
        return result

    def setIsNotNewInstallation(self):
        self.setValue(self.NewInstallationKey, 0)

    def getLastLogin(self):
        return self.getValue(self.LastLoginKey, '')

    def setLastLogin(self, login):
        self.setValue(self.LastLoginKey, login)

    def setUserLoggedIn(self):
        self.setValue(self.UserLoggedInKey, '1')

    def setPaidUserLoggedIn(self):
        self.setValue(self.PaidUserLoggedInKey, '1')

    def getReferrerCode(self):
        return self.getValue(self.ReferrerKey, None)

    def exceptionHandler(self):
        self.setPandaErrorCode(12)
        self.notify.warning('Handling Python exception.')
        if hasattr(__builtin__, 'base') and getattr(base, 'cr', None):
            if base.cr.timeManager:
                OTPGlobals = OTPGlobals
                import otp.otpbase
                base.cr.timeManager.setDisconnectReason(
                    OTPGlobals.DisconnectPythonError)
                base.cr.timeManager.setExceptionInfo()

            base.cr.sendDisconnect()

        if hasattr(__builtin__, 'base'):
            base.destroy()

        self.notify.info('Exception exit.\n')
        import traceback as traceback
        traceback.print_exc()
        sys.exit()

    def isDownloadComplete(self):
        return self.allPhasesComplete


class WebLauncherInstaller(PackageInstaller):

    def __init__(self, launcher):
        PackageInstaller.__init__(self, launcher.appRunner)
        self.launcher = launcher
        self.lastProgress = None

    def packageProgress(self, package, progress):
        PackageInstaller.packageProgress(self, package, progress)
        percent = int(progress * 100.0 + 0.5)
        phase = self.launcher.phasesByPackageName[package.packageName]
        self.launcher.phaseData[phase].percent = percent
        if (phase, percent) != self.lastProgress:
            messenger.send('launcherPercentPhaseComplete', [
                phase,
                percent,
                None,
                None])
            self.lastProgress = (phase, percent)

    def packageFinished(self, package, success):
        PackageInstaller.packageFinished(self, package, success)
        if not success:
            print 'Failed to download %s' % package.packageName
            return None

        phase = self.launcher.phasesByPackageName[package.packageName]
        self.launcher.phaseData[phase].markComplete()

    def downloadFinished(self, success):
        PackageInstaller.downloadFinished(self, success)
        if not success:
            print 'Failed to download all packages.'
