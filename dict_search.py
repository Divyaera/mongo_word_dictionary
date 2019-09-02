def check_install(package_names):
    for package_name in package_names:
        try:
            __import__(package_name)
        except ImportError:
            import pip
            if hasattr(pip, "main"):
                pip.main(['install', package_name])
            else:
                from pip._internal import main as pkj
                pkj(['install', package_name])
check_install(['pymongo'])
import pymongo
import re
import sys
import os
if sys.version_info[0] < 3:
    print("Must be using Python 3")
    exit()
class FileTypeNotSupportedExeption(Exception):
    """raised when unsupported file type is passed"""
    pass
class TableInvalidError(Exception):
    """raised when table structure is not present or None"""
    pass
class uniqueWordDB():
    def __init__(self):
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mycol = None
        self.my_unique_words = set()

    def create_table(self):
        mydb = self.myclient["mydatabase"]
        self.mycol = mydb["customers"]
        self.mycol.delete_many({})

    def fill_table(self, file_name):
        try:
            if file_name.split('.')[-1].lower() != 'txt':
                raise FileTypeNotSupportedExeption
        except FileTypeNotSupportedExeption:
            print("Input .txt files only")
            return False
        with open (file_name, 'r+') as f:
            words = f.readlines()
            f.close()
        index = 0
        my_list = []
        for line in words:
            line = re.sub(r'[^\w\s]', r'', line)
            for word in line.split():
                index += 1
                if word.lower() not in self.my_unique_words:
                    self.my_unique_words.add(word.lower())
                    my_list.append({"_id": index, "name": word.lower()})
        try:
            if not self.mycol:
                raise TableInvalidError
            x = self.mycol.insert_many(my_list)
        except TableInvalidError:
            print("Table structure invalid or None")
            return False
        return True

    def search_table(self, word):
        search_result = self.mycol.find({"name": word.lower()})
        search_result = [result for result in search_result]
        if search_result:
            return True
        else:
            return False

if __name__ == "__main__":
    if len(sys.argv) == 3:
        file_name = sys.argv[1]
        word = sys.argv[2]
    else:
        print ("Error: usage - python dict_search.py <file_name> <word_to_be_searched>")
        exit()
    try:
        with open(file_name, 'r+') as f:
            file_size = os.path.getsize(file_name) / 1024 / 1024
            if file_size > 200:
                print("Enter file size less that 200 MB, current is {}".format(file_size))
                exit()
            f.close()
    except IOError:
        print ("File name does not exists - ", file_name)
        exit()
    db = uniqueWordDB()
    db.create_table()
    db_populated = db.fill_table(file_name)
    if db_populated:
        print(db.search_table(word))