#!/usr/bin/python
# -*- coding: utf-8 -*-

import wykop
import argparse
import ConfigParser
import sys, os
import textwrap
from StringIO import StringIO
from ConfigParser import SafeConfigParser

def usage():
    return \
    """mikro.py [-h] [--appkey APPKEY --secret SECRET --login LOGIN --accountkey ACCOUNTKEY ] |
                     [--config CONFIG [--section SECTION]]
                message"""

def epilog():
    return textwrap.dedent("""\
mikro.py to prosty program napisany w języku Python,
służący do wysyłania wiadomości tekstowych na mikrobloga
serwisu Wykop.pl.

Przykłady użycia:

  mikro.py "Lubie placki #oswiadczenie"

Takie proste wywołanie jest możliwe tylko wtedy jeżeli zostanie
wczesniej zdefiniowany plik konfiguracyjny (domyślnie: ~/.mikro),
zawierający uzupełnione dane:

  [wykop]
      appkey=
      secret=
      login=
      accountkey=

Możliwe jest też dostarczenie całej niezbednej konfiguracji
bezpośrednio za pomocą dodatkowych argumentów:

  mikro.py --appkey oKcgE22J3iH --secret LcK6SCU --accountkey SCUyHpfuTo2n52gCtG0 --login noisy "Lubie placki #oswiadczenie"

A także wskazanie innej niż domyślnej lokalizacji pliku
onfiguracyjnego:

  mikro.py --config /tmp/mikro_test.conf --section nazwa_sekcji

Może także użyć kombinacji obydu metod. W takim przypadku
najpierw odczytywane są wartości ze wskazanego (lub domyślnego)
pliku, które to następnie mogą być nadpisane poprzez podane
argumenty:

  mikro.py --config ~/.wykop.ini --login noisy --accountkey SCUyHpfuTo2n52gCtG0 "Lubie placki #oswiadczenie"
  mikro.py --login noisy2 --accountkey PhWAG1U9HARrCav4Aj5F "Lubie placki #oswiadczenie"

FAQ:

> Skąd wziąć appkey, secret i accountkey?

  Należy je sobie samodzielnie wygenerować korzystając ze
  strony dla programistów w serwisie wykop:

  http://www.wykop.pl/dla-programistow/api/

  Następnie należy wejść do [Uzyskaj dostęp do API] i wypełnić
  pole "nazwa aplikacji" (dowolną wartością), a także zaznaczyć
  następujące pola:

  [✓] - Logowanie - umożliwia zalogowanie się na konto użytkownika
  [✓] - Mikroblog - rozpoczynanie i uczestniczenie w dyskusjach na mikroblogu

  [✓] - Oświadczam, że zapoznałem się z Regulaminem WykopAPI

  UWAGA: Nie należy zaznaczać opcji "Sesja Użytkownika"!

  Po zatwierdzeniu zgłoszenia, należy przejść na stronę:
  http://www.wykop.pl/dla-programistow/twoje-aplikacje/

  i przy odpowiedniej pozycji kliknąć [Połącz aplikacje].


Źródła projektu dostępne są pod adresem:
http://github.com/noisy/mikro.py/
""")

def main():

    home = os.path.expanduser("~")
    scriptname=os.path.splitext(os.path.basename(__file__))[0]
    config_file_path = home+"/."+scriptname

    parser = argparse.ArgumentParser(usage=usage(), epilog=epilog(), formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--appkey', help='Klucz aplikacji')
    parser.add_argument('--secret', help='Sekretny klucz aplikacji')
    parser.add_argument('--login', help='Login użytkownika w serwisie wykop.pl')
    parser.add_argument('--accountkey', help='Klucz uzytkownika')
    parser.add_argument('--config', default=config_file_path, help='Plik cfg/ini zawierający powyższą konfiguracje\n(domyslnie: %s)' % config_file_path)
    parser.add_argument('--section', default="wykop", help='Sekcja w pliku cfg/ini zawierająca konfiguracje\n(domyslnie: wykop)')
    parser.add_argument('message', help='Wiadomosc do wyslania na mikroblog')

    args = parser.parse_args()


    required_config = ['appkey', 'secret', 'login', 'accountkey']

    if os.path.isfile(args.config):
        config = SafeConfigParser()
        data = StringIO('\n'.join(line.strip() for line in open(args.config)))
        config.readfp(data)
        for x in required_config:
            if getattr(args, x) == None:
                try:
                    setattr(args, x, config.get(args.section, x))
                except ConfigParser.NoOptionError:
                    print "Paramentr %s nie został ustawiony" % x
                    exit()

    elif not all(getattr(args, x) != None for x in required_config):
        print u"Plik konfiguracyjny (%s) nie istnieje, a dostarczone parametry niezapewniają wystarczającej konfiguracji" % args.config
        print "sprawdz: %s --help" % sys.argv[0]
        exit()


    api = wykop.WykopAPI(args.appkey, args.secret)
    api.authenticate(args.login, args.accountkey)

    api.add_entry(args.message)

if __name__ == '__main__':
    main()
