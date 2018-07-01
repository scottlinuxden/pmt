
# $Id$
#
# COPYRIGHT:
#   Copyright (C) 1999 LinuXden, All Rights Reserved
#   Copright Statement at http://www.linuxden.com/copyrighted_apps.html
#
# AUTHOR: 
#   R. Scott Davis
#
# CONTACT:
#   R. Scott Davis
#   E-mail: scott.davis@linuxden.com
#

import time

def YY_Year_to_YYYY(year):
	"""
	Converts a two digit year to a four digit year
	This will only work for years 1999-2098
	"""
	if year == '99':
		return `int(year) + 1900`
	else:
		return `int(year) + 2000`
	
def timeDelta(time1, time2):
	"""
	Calculates the difference in seconds between two times,
	time2 - time1
	where each time is specified like the following:
	YYYYMMDDHHNNSS
	YYYY is four digit year
	MM is two digit month
	DD is two digit day
	HH is two digit hour
	NN is minutes
	SS is seconds
	"""
	time1_secs = time.mktime((int(time1[:4]), int(time1[4:6]), int(time1[6:8]), int(time1[8:10]), int(time1[10:12]), int(time1[12:14]), 0, 0, 0))
	time2_secs = time.mktime((int(time2[:4]), int(time2[4:6]), int(time2[6:8]), int(time2[8:10]), int(time2[10:12]), int(time2[12:14]), 0, 0, 0))
	return time2_secs - time1_secs

def dateTimeToTime(date_time):
	"""
	Converts a date time string in the format YYYYMMDDHHMISS
	to seconds since the epoch on a UNIX machine which is
	January 1, 1970
	"""
	return time.mktime((int(date_time[:4]), int(date_time[4:6]), int(date_time[6:8]), int(date_time[8:10]), int(date_time[10:12]), int(date_time[12:14]), 0, 0, 0))

def YYMMDD_DateToTime(date):
	"""
	Converts a date time string in the format YYMMDD
	to seconds since the epoch on a UNIX machine which is
	January 1, 1970, It is implied that hours, minutes, seconds is 0
	and that if year <> 99 then the 21st century else 20th century
	"""
	return time.mktime((int(YY_Year_to_YYYY(date[:2])), int(date[2:4]), int(date[4:6]), 0, 0, 0, 0, 0, 0))

def timeTo_YYMMDD(date_time):
	"""
	Returns the YYMMDD of the date specified by date_time
	"""
	return time.strftime('%y%m%d', time.localtime(date_time))  

def YYMMDD_DateToJulianDay(date):
	"""
	Returns the julian day of the date specified by date. Date is in the format of
	YYMMDD
	"""
	date_time = time.mktime((int(YY_Year_to_YYYY(date[:2])), int(date[2:4]), int(date[4:6]), 0, 0, 0, 0, 0, 0))

	return time.strftime('%j', time.localtime(date_time))

def YYMMDD_DateToDayOfWeek(date):
	"""
	Returns the day of the week specified by date.  Date is in the format of YYMMDD  
	"""
	date_time = time.mktime((int(YY_Year_to_YYYY(date[:2])), int(date[2:4]), int(date[4:6]), 0, 0, 0, 0, 0, 0))

	return time.strftime('%w', time.localtime(date_time))

def YYMMDD_Split(date):
	"""
	Returns a tuple containing (2 digit year, month, day)
	"""
	return (date[:2], date[2:4], date[4:])

def YYMMDD_SplitYYYYMMDD(date):
	"""
	Returns a tuple containing (4 digit year, month, day)
	"""
	return (YY_Year_to_YYYY(date[:2]), date[2:4], date[4:])

def dayBefore_YYMMDD(date):
	"""
	Returns the date in the form of YYMMDD of the day before the
	date specified by date
	"""
	date_time = YYMMDD_DateToTime(date)
	date_time = date_time - 86400
	return timeTo_YYMMDD(date_time)

def dayAfter_YYMMDD(date):
	"""
	Returns the date in the form of YYMMDD of the day before the
	date specified by date
	"""
	date_time = YYMMDD_DateToTime(date)
	date_time = date_time + 86400
	return timeTo_YYMMDD(date_time)

def current_time_MM_DD_YYYY():
	"""
	Returns the current date in the format MM-DD-YYYY
	"""
	return time.strftime('%m-%d-%Y', time.localtime(time.time()))  

