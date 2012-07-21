#!/usr/bin/env python
# encoding: utf-8
"""
main.py

Created by Julia Winn on 2012-07-02.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import pymongo


def main():
    
    # connect to database
    connection = pymongo.Connection()
    items = connection.craigslist.items
    
    # drop all of yesterdays items
    items.drop()
    
    # get new items
    os.system("scrapy crawl boston")
    
    # now render the website
    os.system("python /home/jwinn12/craigpad/app.py")

if __name__ == '__main__':
	main()

