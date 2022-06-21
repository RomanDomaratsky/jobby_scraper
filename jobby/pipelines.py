# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class JobbyPipeline:
    def __init__(self):
        self.con = sqlite3.connect('jobs.sqlite')
        self.cur = self.con.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS jobs(
                                        title TEXT,
                                        link TEXT,
                                        organization TEXT,
                                        city TEXT,
                                        region TEXT,
                                        country TEXT,
                                        posted_date TEXT,
                                        description TEXT
                                        )""")

    def process_item(self, item, spider):
        self.cur.execute("""INSERT OR IGNORE INTO jobs VALUES (?,?,?,?,?,?,?,?)""",
                                  (item['title'], item['link'], item['organization'], item['city'],
                                   item['region'], item['country'], item['posted_date'], item['description']))

        self.cur.execute("""DELETE FROM jobs
                                    WHERE rowid NOT IN (
                                    SELECT MIN(rowid) 
                                    FROM jobs
                                    GROUP BY link
                                    )""")

        self.con.commit()
        return item
