

sudo usb_modeswitch -v 0x12d1 -p 0x1521 -M 55534243123456780000000000000011060000000000000000000000000000

ubuntu@beagle:/opt/advent$ lsusb
Bus 001 Device 003: ID 12d1:1464 Huawei Technologies Co., Ltd. 
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub

Berechtigungen!




            #
            # /etc/smsd.conf
            #
            # Description: Main configuration file for the smsd
            #
            
            devices = GSM1
            outgoing = /var/spool/sms/outgoing
            checked = /var/spool/sms/checked
            incoming = /var/spool/sms/incoming
            logfile = /var/log/smstools/smsd.log
            infofile = /var/run/smstools/smsd.working
            pidfile = /var/run/smstools/smsd.pid
            outgoing = /var/spool/sms/outgoing
            checked = /var/spool/sms/checked
            failed = /var/spool/sms/failed
            incoming = /var/spool/sms/incoming
            sent = /var/spool/sms/sent
            stats = /var/log/smstools/smsd_stats
            #loglevel = 7
            
            receive_before_send = no
            
            autosplit = 3
            
            eventhandler = /opt/advent/handler.sh
            
            
            
               
            [GSM1]
            pre_init = no
            #init = ATZ
            init = ATE0
            #init2 = ATE0
            device = /dev/ttyUSB0
            incoming = yes
            baudrate = 19200
            rtscts = no
            memory_start = 0