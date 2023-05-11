#!/usr/bin/python

# pitiful file, but neats and logs
from sys import version as python_version

# 2 modify
__curr_ver__ = '1.30 06 Jan 2021'.split()

# 2 update
__old_vers__ = [ '1.25 10 Aug 2020', '1.24 20 Feb 2020', '1.23 02 Oct 2019',
                 '1.21 20 Mar 2019', '1.2 27 Jan 2019', '1.12 20 Dic 2018',
                 '1.11 20 Jul 2018', '1.1 07 May 2018','1.0 13 Apr 2018']

# 2 rarely modify
__copyright__ = ( 'Copyright ' + u'\u00a9' + ' 2018-' + __curr_ver__[-1] + ','
                + '\nHernan Chavez Thielemann')

__url__ = 'https://github.com/hernanchavezthielemann/GRO2LAM'

__version__ = ' GRO2LAM version {} ({} {} {})'.format( *__curr_ver__)

__python_version__ = float( python_version[ 0:3])