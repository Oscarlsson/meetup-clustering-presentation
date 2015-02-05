# -*- coding: utf-8 -*-

# Scrapy settings for lyricsspider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'lyricsspider'

SPIDER_MODULES = ['lyricsspider.spiders']
NEWSPIDER_MODULE = 'lyricsspider.spiders'

ITEM_PIPELINES = {
    'lyricsspider.pipelines.outputter': 1,
}
