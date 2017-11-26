import logging
import time
from datetime import date

from advent.Model.basemodel import db
from advent.Model.sms import SMS
from advent.Model.subscriber import Subscriber
from advent.Model.thought import Thought


class KEYWORDS:
    SUBSCRIBE = ['advent']
    UNSUBSCRIBE = ['abmelden']
    REQUESTSTATUS = ['status']

class NUMBERS:
    ADMIN = '491621050910'

class TEXTS:
    SUBSCRIBED = 'Hallo, schön, dass Du Dich für unseren Adventskalender entscheiden hast. Wir wünschen Dir eine schöne Adventszeit, L.G. Jugend St. Konrad/Lauenburg'
    UNSUBSCRIBED = 'Hallo, wir haben Dich vom Adventskalender abgemeldet. Wir wünschen Dir eine schöne Adventszeit, L.G. Jugend St. Konrad/Lauenburg'
    DOUBLESUB = 'Hallo, wir haben Dich bereits auf der Liste, Du erhältst jeden Tag im Advent eine SMS. Wir wünschen eine schöne Adventszeit, L.G. Jugend St. Konrad/Lauenburg'
    NOTLISTED = 'Hallo, wir können Dich nicht auf der Liste finden, eine Abmeldung war nicht möglich. Wir wünschen Dir eine schöne Adventszeit, L.G. Jugend St. Konrad/Lauenburg'
    STATUS = 'Status des Adventskalenders: {0}, Uptime: {1}, Subscribers: {2}'


class AdventController(object):
    def __init__(self):
        logging.basicConfig(filename='advent.log', level=logging.INFO)
        self.outgoingPath = '/var/spool/sms/outgoing'
        db.connect()
        self.createdatabase()  # TODO: remove this

    def createdatabase(self):
        db.create_tables([Thought, SMS, Subscriber], safe=True)

    def smsfromfile(self, file):
        with open(file, 'r') as file:
            return SMS.fromstring(file.read())

    def incomming(self, sms):
        answer =None
        if sms.checkforkeywords(KEYWORDS.SUBSCRIBE):
            sub = Subscriber.subscribe(sms.msgfrom, sms.msg)
            if sub:
                logging.info('{0} has subscribed'.format(sms.msgfrom))
                answer = SMS.create(sms.msgfrom, TEXTS.SUBSCRIBED, True)
            else:
                logging.warn('{0} tried to subscribe, but was already subscribed!'.format(sms.msgfrom))
                answer = SMS.create(sms.msgfrom, TEXTS.DOUBLESUB, True)

        elif sms.checkforkeywords(KEYWORDS.UNSUBSCRIBE):
            try:
                sub = Subscriber.get(Subscriber.number == sms.msgfrom, Subscriber.active == True)
                sub.unsubscribe(sms.msgfrom, sms.msg)
                logging.info('{0} has unsubscribed'.format(sms.msgfrom))
                answer = SMS.create(sms.msgfrom, TEXTS.UNSUBSCRIBED, True)
            except Subscriber.DoesNotExist:
                logging.warn('{0} tried to unsubscribe, but was not found!'.format(sms.msgfrom))
                answer = SMS.create(sms.msgfrom, TEXTS.NOTLISTED, True)

        elif sms.checkforkeywords(KEYWORDS.REQUESTSTATUS):
            answer = SMS.create(sms.msgfrom, TEXTS.STATUS, True)

        if answer:
            self.send(answer)
        return 0

    def send(self, sms):
        with open(self.outgoingPath + '/{}.sms'.format(sms.get_id()), 'w') as file:
            file.write(sms.tostring())

    def manualsend(self, msg, number='', force=False):
        sq = Subscriber.select().where(Subscriber.active == True)
        if number:
            if force or sq.where(Subscriber.number == number).exists():
                sms = SMS.create(number, msg, True)
                self.send(sms)
                logging.info('Sending SMS "{0}" to {1}'.format(sms.msg, sms.msgto))
            else:
                logging.warn('{0} was not subscribed, use force if you really want so!'.format(number))
        else:
            for sms in list(map(lambda num: SMS.create(num, msg, True), Subscriber.getallnumbers())):
                self.send(sms)
            logging.info('Sending SMS "{0}" to all subscribers'.format(msg))

    def job(self, month=0, day=0):

        logging.info('Job started!')
        start = time.time()

        if not (month and day):
            today = date.today()
            month = today.month
            day = today.day

        try:
            thougth = Thought.oftheday(day, month)
        except Thought.DoesNotExist:
            thougth = None
            logging.warn('No thought of the day found! Done!')

        if thougth:
            print(thougth.msg)

            for sms in list(map(lambda num: SMS.create(num, thougth.msg, True), Subscriber.getallnumbers())):
                self.send(sms)
            logging.info('Sending SMS "{0}" to all subscribers'.format(thougth.msg))

            thougth.is_published = True
            thougth.save()

        elapsed = time.time()

        logging.info('Job ended! ({0} seconds)'.format(elapsed - start))

    def status(self, dest):
        if dest == 'sms':
            self._statustosms()
        else:
            self._statustoconsole()

    def _statustoconsole(self):
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])

        print('--------------------------------')
        print('  ADVENTSKALENDER ')
        print('  status: OK                    ')
        print('  uptime: ' + self.pretty_time_delta(uptime_seconds))
        print('  subscribers: ' + str(Subscriber.count()))
        print('--------------------------------')

    def _statustosms(self):

        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])

        answer = SMS.create(NUMBERS.ADMIN, TEXTS.STATUS.format('OK', self.pretty_time_delta(uptime_seconds),Subscriber.count()), True)
        self.send(answer)

    def debug(self):
        today = date.today()
        month = today.month
        day = today.day

        Thought.create('mymessage!', day, month)

    @staticmethod
    def pretty_time_delta(seconds):
        seconds = int(seconds)
        days, seconds = divmod(seconds, 86400)
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)
        if days > 0:
            return '%dt %dh %dm %ds' % (days, hours, minutes, seconds)
        elif hours > 0:
            return '%dh %dm %ds' % (hours, minutes, seconds)
        elif minutes > 0:
            return '%dm %ds' % (minutes, seconds)
        else:
            return '%ds' % (seconds)