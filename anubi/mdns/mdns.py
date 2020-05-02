import socket
import threading
import queue
import random
import errno
import logging
import time
import select
import os
from .dnspacket import DnsPacket
from .dnsqrecord import DnsQRecord
from .dnsenums import OpCode, RCode, DnsType

logger = logging.getLogger(__name__)

class QueueRecord():
    def __init__(self, query, answers, additionals, unicast_address):
        self.query = query
        self.answers = answers
        self.additionals = additionals
        self.unicast_address = unicast_address

class DnsReplySender(threading.Thread):
    def __init__(self, sock, multicast_address):
        super().__init__(name='DnsReplySender')
        self.__reply_queue = queue.Queue(-1) #infinite queue
        self.__reply_queue_lock = threading.Semaphore(0)
        self.__sock = sock
        self.__multicast_address = multicast_address

    def run(self):
        try:
            while True:
                #get item from queue
                self.__reply_queue_lock.acquire()
                data = self.__reply_queue.get_nowait()
                if data is None:
                    logger.info('Exiting message sender thread')
                    #stop the thread
                    return
                received_from_multicast = data.unicast_address[1] == self.__multicast_address[1]
                prefer_unicast = any(map(lambda q: q.prefer_unicast, data.query.question_records))
                if prefer_unicast or (not received_from_multicast):
                    #send unicast message
                    unicast_reply = DnsPacket(False)
                    unicast_reply.id = data.query.id
                    unicast_reply.question_records.extend(data.query.question_records)
                    unicast_reply.answer_records.extend(data.answers)
                    unicast_reply.additional_records.extend(data.additionals)
                    logger.info('Unicast: sending %s to %s', unicast_reply, data.unicast_address)
                    self.__sock.sendto(unicast_reply.encode(), data.unicast_address)
                if (not prefer_unicast) or received_from_multicast:
                    #send multicast message
                    multicast_reply = DnsPacket(False)
                    multicast_reply.answer_records.extend(data.answers)
                    multicast_reply.additional_records.extend(data.additionals)
                    delay = random.randint(20, 120) / 1000.0
                    #multicast reply must be delayed by a random ammount of ms to avoid collisions
                    logger.info('Multicast: sending %s', multicast_reply)
                    time.sleep(delay)
                    self.__sock.sendto(multicast_reply.encode(), self.__multicast_address)
        except Exception as ex:
            logger.error('Exiting message sender thread with error {0}'.format(ex))
            return

    def send(self, query, answers, additionals, unicast_address):
        record = QueueRecord(query, answers, additionals, unicast_address)
        self.__reply_queue.put(record)
        self.__reply_queue_lock.release()

    def stop(self):
        #token to stop the thread
        self.__reply_queue.put(None)
        #notify that new data are available
        self.__reply_queue_lock.release()
        logger.info('Stopping message sender thread')


class mDNS(threading.Thread):
    __MDNS_ADDRESS = ('224.0.0.251', 5353)
    __MAX_PACKET_SIZE = 9000 - 20 - 8#Max packet - IPv4 header - UDP header

    def __init__(self):
        '''
        Implements the multicast DNS logic.
        Once started it spawn a new thread that reply to mDNS queries when there is at least one answer
        to the query question in the internal record database.
        '''
        super().__init__(name='mDNS responder')
        #record database
        self.__records_db = []
        #open the socket
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #set socket options
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if hasattr(socket, 'SO_REUSEPORT'):
            self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.__sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
        self.__sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, True)
        #register to multicast group
        mGroup = socket.inet_aton(self.__MDNS_ADDRESS[0]) + socket.INADDR_ANY.to_bytes(4, byteorder='big')
        self.__sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mGroup)
        #bind the socket to the correct port
        self.__sock.bind(('', self.__MDNS_ADDRESS[1]))
        #create pipes used for stopping thread
        self.__read_pipe, self.__write_pipe = os.pipe()
        #reply sender
        self.__reply_sender = DnsReplySender(self.__sock, self.__MDNS_ADDRESS)

    def run(self):
        self.__reply_sender.start()
        while True:
            try:
                ready_read, _, _ = select.select([self.__sock, self.__read_pipe], [], [])
                if (self.__sock in ready_read):
                    data, addr = self.__sock.recvfrom(4096)
                    logger.debug('Received request %s', data.hex())
                    try:
                        query = DnsPacket.decode(data)
                    except:
                        logger.warning('Fail to decode received data')
                        continue
                    #check if we have some record that ask questions
                    answers = []
                    additional = []
                    #process only query with OP CODE: QUERY and R CODE: NOERROR
                    if query.OpCode == OpCode.QUERY and query.RCODE == RCode.NOERROR:
                        for question in query.question_records:
                            answers += list(filter(lambda r: r.answer_to(question), self.__records_db))
                            for additional_question in self.__get_additional_questions(question):
                                additional += list(filter(lambda r: r.answer_to(additional_question), self.__records_db))
                        if len(answers) != 0:
                            if self.__reply_sender.is_alive():
                                #we have some answers, prepare the packet to send back
                                self.__reply_sender.send(query, answers, additional, addr)
                            else:
                                logger.error('Exiting mDNS thread because reply sender thread stop working')
                                return
                else:
                    logger.info('Exiting mDNS thread')
                    self.__sock.close()
                    os.close(self.__read_pipe)
                    return
            except Exception as ex:
                logger.error('Exiting mDNS thread with error {0}'.format(ex))
                #error occurred, exit
                self.__sock.close()
                return
    def start(self):
        '''
        Start the mDSN instance. Once started the instance reply to mDNS queries if the internal database
        contains at least one record that reply to query questions.
        This method cannot be called on a stopped instance.
        '''
        super().start()
    def stop(self):
        '''
        Stop a running instance of mDNS that do not reply to queries anymore.
        Once stopped an mDNS instance cannot be started again.
        '''
        logger.info('Stopping mDNS thread')
        self.__reply_sender.stop()
        self.__reply_sender.join()
        w = os.fdopen(self.__write_pipe, 'w')
        w.write('\0')
        w.close()
    def add_record(self, record):
        '''
        :param record: The record that has to be added to the internal database.
        :type record: :class:`DnsRRecord`       
        :return: True if the record has been added, False otherwise.

        Add the given record to the internal class database.
        This method can be called any time, even after the instance has been started by the 
        :func:`start` method.
        '''
        #check if the record already exists
        if record in self.__records_db:
            logging.warning('Record {0} already present in record database'.format(record))
            return False
        else:
            self.__records_db.append(record)
            logger.info('Add {0} record to record database'.format(record))
            return True
    @staticmethod
    def __get_additional_questions(question):
        if question.record_type == DnsType.A:
            return [DnsQRecord(question.name, DnsType.AAAA, question.record_class)]
        elif question.record_type == DnsType.AAAA:
            return [DnsQRecord(question.name, DnsType.A, question.record_class)]
        else:
            return []