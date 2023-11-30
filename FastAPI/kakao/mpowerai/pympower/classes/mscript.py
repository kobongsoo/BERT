import os
import signal

class MStopEvent:
    _signaled = False

    @staticmethod
    def _sigintHandler(signum, frame):
        MStopEvent._signaled = True

    @staticmethod
    def setup():
        signal.signal(signal.SIGINT, MStopEvent._sigintHandler)
        if 'nt' != os.name:
            signal.signal(signal.SIGTERM, MStopEvent._sigintHandler)

    @staticmethod
    def isSetup() -> bool:
        if 'nt' == os.name:
            return MStopEvent._sigintHandler == signal.getsignal(signal.SIGINT)
        else:
            return (
                (MStopEvent._sigintHandler == signal.getsignal(signal.SIGINT))
                and (MStopEvent._sigintHandler == signal.getsignal(signal.SIGTERM))
            )

    @staticmethod
    def isSignaled() -> bool:
        return MStopEvent._signaled

    @staticmethod
    def setSignaled():
        MStopEvent._signaled = True

    @staticmethod
    def clearSignaled():
        MStopEvent._signaled = False

    @staticmethod
    def sendSignal(pid:int):
        os.kill(pid, signal.SIGINT)


##############################################################################
# __all__ 구성
##############################################################################

__all__ =  [
    MStopEvent.__name__,
]
