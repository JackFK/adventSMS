import argparse

from advent.adventcontroller import AdventController

parser = argparse.ArgumentParser(description='Process SMS Advent.')


def _bootstrap():
    return AdventController()


def incomming(args):
    if not args.path:
        parser.error('path needed!')
    ac = _bootstrap()
    sms = ac.smsfromfile(args.path)
    if sms:
        return ac.incomming(sms)
    return -1


def send(args):
    if not args.message:
        parser.error('message needed!')
    ac = _bootstrap()
    return ac.manualsend(args.message)


def status(args):
    ac = _bootstrap()
    ac.status('console')
    return 0


def sendstatus(args):
    ac = _bootstrap()
    ac.status('sms')
    return 0


def job(args):
    ac = _bootstrap()
    return ac.job()


def debug(args):
    ac = _bootstrap()
    ac.debug()
    return 0

def createdb(args):
    ac = AdventController()
    ac.createdatabase()
    return 0



parser.add_argument('--incomming', dest='function', action='store_const',
                    const=incomming,
                    help='process SMS file')

parser.add_argument('--send', dest='function', action='store_const',
                    const=send,
                    help='send SMS')

parser.add_argument('--status', dest='function', action='store_const',
                    const=status,
                    help='print status')

parser.add_argument('--sendstatus', dest='function', action='store_const',
                    const=sendstatus,
                    help='send status')

parser.add_argument('--job', dest='function', action='store_const',
                    const=job,
                    help='execute jobs in que')

parser.add_argument('--db', dest='function', action='store_const',
                    const=createdb,
                    help='creates Database')

parser.add_argument('--debug', dest='function', action='store_const',
                    const=debug,
                    help='debugging')

parser.add_argument('--path', dest='path', help='path to SMS file')
parser.add_argument('--message', dest='message', help='message to send')

args = parser.parse_args()

result = args.function(args)

exit(result)
