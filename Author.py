class Author:
    journal=" "
    volume=0
    number=0
    pages=0
    year=0
    publisher=""


    def __init__(self,author_name,author_surname):
        self.author_name=author_name
        self.author_surname=author_surname
    def get_author_name(self):
        return self.author_name

    def get_author_journal(self):
        return self.journal

    def get_author_volume(self):
        return self.journal

    def get_author_number(self):
        return self.number

    def get_author_pages(self):
        return self.pages

    def get_author_year(self):
        return self.year

    def get_author_publisher(self):
        return self.publisher

    def get_author_surname(self):
        return self.author_surname
