# from pysqlite2 import dbapi2 as sqlite
import sqlite3
import logging
from scrapy.shell import inspect_response

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(process)d - %(name)s - %(levelname)s - %(lineno)d -  %(message)s'
    )
logger = logging.getLogger('scrapme.pipelines.SQLiteInsertPipeline')

class SQLiteInsertPipeline(object):

    def __init__(self):

        # semua config sebaiknya di file pipeline
        # karena selain config, ada database structure yang harus disesuaikan untuk setiap kasus
        # memang agak berbeda untuk database unstructure yang confignya hanya alamat

        self.connection = sqlite3.connect('data/quotes_simple.db')
        self.cursor = self.connection.cursor()

        try:
            logger.debug("start init CREATE TABLE IF NOT EXISTS quotes_simple")
            ddl = "\
                CREATE TABLE IF NOT EXISTS quotes_simple (\
                    id INTEGER PRIMARY KEY, \
                    author_bio TEXT, \
                    author_birthday DATE, \
                    author_bornlocation TEXT, \
                    author_name VARCHAR(50), \
                    quote_content TEXT \
                    )\
                "
            self.cursor.execute(ddl)
            logger.debug("CREATE TABLE IF NOT EXISTS quotes_simple")

        except sqlite3.Error as e:
            logger.error(e)

    def process_item(self, item, spider):

        try:
            logger.debug("Duplicate Check Start")

            dml = "\
                SELECT * \
                FROM quotes_simple \
                WHERE quote_content=?\
                "
            criteria = (item['quote_content'],)
            self.cursor.execute(dml, criteria)

            logger.debug("Duplicate Check Finish")

        except sqlite3.Error as e:
            logger.error(e)
        
        result = self.cursor.fetchone()
        # result adalah hasil fetch database, bukan item
        # logger.debug("Duplicate Check Result : %s" % str(result[5]))

        # for debugging
        # inspect_response(response, self)

        if result:
            logger.debug("Item already in database: %s" % item)
        else:
            try:

                logger.debug("Store item")
                # logger.debug("Store item : %s" % item)

                sql = "\
                    INSERT INTO quotes_simple \
                    (author_bio, author_birthday, author_bornlocation, author_name, quote_content) VALUES \
                    (?,?,?,?,?)\
                    "

                data = (
                    item["author_bio"],
                    item["author_birthday"],
                    item["author_bornlocation"],
                    item["author_name"],
                    item["quote_content"]
                    )
                
                self.cursor.execute(sql,data)
                self.connection.commit()

                # logger.debug("Item stored : %s" % item)
                logger.debug("Item stored")

            except sqlite3.Error as e:
                logger.error(e)

        return item