import os
from pymongo import MongoClient, errors
from datetime import datetime
from pprint import pprint
import PySimpleGUI as sg


class Mongo:
    def __init__(self, host, port):
        self.client = None
        self.dbs = None
        self.db = None
        self.collections = None
        self.collection = None

    def connect_client(self, host, port):
        try:
            self.client = MongoClient(host, int(port))
            self.dbs = self.client.list_database_names()
            return True
        except errors.ConnectionFailure:
            print("Failed to connect to server")
            return False

    def select_db(self, db_name):
        self.db = self.client[db_name]

    def get_collections(self):
        self.collections = self.db.list_collection_names()
        return self.collections

    def select_collection(self, collection_name):
        self.collection = self.db[collection_name]

    def add_one(self):
        post = {
            'title': 'あいうえお',
            'content': 'かきくけこ',
            'created_at': datetime.now()
        }
        return self.db.test.insert_one(post)

    def get_item(self):
        for data in self.db.test.find():
            pprint(data)


class Option:
    def __init__(self):
        self.export_path = __file__
        self.host = 'localhost'
        self.port = '27017'


class MainDisplay:
    def __init__(self):
        self.option = Option()
        self.mongo = Mongo(self.option.host, self.option.port)

        sg.theme('DarkBlue12')
        # self.layout = [
        #     [sg.Button(button_text='Option', key='-OPTION-', )],
        #     [sg.Text('Database List')],
        #     [sg.Listbox(values=(), size=(30, 5), key='-DATABASELIST-')],
        #     [sg.Button(button_text='Select Database', key='-DATABASE-')],
        #     [sg.Text('_' * 30)],
        #     [sg.Text('Collections')],
        #     [sg.Listbox(values=(), size=(30, 20), key='-COLLECTIONLIST-')],
        # ]
        self.layout = [
            [sg.Button(button_text='Option', key='-OPTION-', )],
            [sg.Text('Database List'), sg.Text('Collections')],
            [sg.Listbox(values=(), size=(30, 5), key='-DATABASELIST-'),
             sg.Text('⇒'),
             sg.Listbox(values=(), size=(30, 5), key='-COLLECTIONLIST-')],
            [sg.Button(button_text='Select Database', key='-DATABASE-'),
             sg.Button(button_text='Select Collection', key='-COLLECTION-')],
            [sg.HorizontalSeparator()],
        ]
        self.window = sg.Window(title='MongoToCsv', layout=self.layout, finalize=True)

        if self.mongo.connect_client(self.option.host, self.option.port):
            self.window['-DATABASELIST-'].update(values=self.mongo.dbs)

    def call_option_display(self):
        option_display = OptionDisplay(self.option, self.mongo)
        client_updated = option_display.main()
        if client_updated:
            self.window['-DATABASELIST-'].update(values=self.mongo.dbs)
        del option_display

    def main(self):
        while True:
            event, values = self.window.read()
            print(event, values)
            if event in (None, 'Exit'):
                break
            if event == '-OPTION-':
                self.call_option_display()
            if event == '-DATABASE-':
                if len(values['-DATABASELIST-']) <= 0:
                    continue
                self.mongo.select_db(values['-DATABASELIST-'][0])
                self.window['-COLLECTIONLIST-'].update(values=self.mongo.get_collections())
            if event == '-COLLECTION-':
                if len(values['-COLLECTIONLIST-']) <= 0:
                    continue
                self.mongo.select_collection(values['-COLLECTIONLIST-'][0])
        self.window.close()


class OptionDisplay:
    def __init__(self, option, mongo):
        self.option = option
        self.mongo = mongo

        sg.theme('DarkBlue11')
        tab1_layout = [
            [sg.Text('host', size=(5, 1)), sg.Input(option.host, size=(15, 1), key='host')],
            [sg.Text('port', size=(5, 1)), sg.Input(option.port, size=(15, 1), key='post')],
            [sg.Submit(button_text='Connect MongoDB'),
             sg.Text(key='Connect MongoDB Result', size=(15, 1))]
        ]
        tab2_layout = [
            [sg.Text('export', size=(5, 1)), sg.InputText(), sg.FolderBrowse()]
        ]
        self.layout = [
            [sg.TabGroup([[sg.Tab('Connect', tab1_layout), sg.Tab('Export', tab2_layout)]])],
            [sg.Exit()]
        ]
        self.window = sg.Window(title='Option', layout=self.layout)

    def main(self):
        client_updated = False
        while True:
            event, values = self.window.read()
            print(event, values)
            if event in (None, 'Exit'):
                break
            if event == 'Connect MongoDB':
                if self.mongo.connect_client(values['host'], values['post']):
                    self.window['Connect MongoDB Result'].update('Success!', text_color=("#0000ff"))
                    client_updated = True
                else:
                    self.window['Connect MongoDB Result'].update('Error!', text_color=('#ff0000'))
        self.window.close()
        return client_updated

# # sg.theme('Dark Blue 3')
# sg.theme('GreenTan')
#
# tab1_layout = [
#     [sg.Button(button_text='Option')],
#     [sg.Text('host', size=(5, 1)), sg.Input('localhost', size=(15, 1), key='host')],
#     [sg.Text('port', size=(5, 1)), sg.Input('27017', size=(15, 1), key='post')],
#     [sg.Submit(button_text='Connect MongoDB'),
#      sg.Text(key='Connect MongoDB Result', size=(15, 1))],
#     [sg.Text('_' * 30)],
#     [sg.Text('Database List')],
#     [sg.Listbox(values=(), size=(30, 5), key='dbs')],
#     [sg.Button(button_text='Select Database')]
# ]
#
# tab2_layout = [
#     [sg.Text('Collections')],
#     [sg.Listbox(values=(), size=(30, 20), key='collections')],
# ]
#
# layout = [
#     [sg.TabGroup([[sg.Tab('Connect', tab1_layout), sg.Tab('Collections', tab2_layout)]])]
# ]
#
# window = sg.Window('Mongo to Csv', layout)
# mongo = Mongo()
#
# while True:
#     event, values = window.read()
#     print(event, values)
#     if event in (None, 'Exit'):
#         break
#     if event == 'Option':
#         sg.popup(option_layout)
#     if event == 'Connect MongoDB':
#         mongo.set_mongo_client(values['host'], values['post'])
#         window['Connect MongoDB Result'].update('Success!', text_color=("#0000ff"))
#         # window['Connect MongoDB Result'].update('Error!', text_color=('#ff0000'))
#         window['dbs'].update(values=mongo.dbs)
#     if event == 'Select Database':
#         mongo.select_db(values['dbs'][0])
#         window['collections'].update(values=mongo.get_collections())
#
#
#
# window.close()


if __name__ == '__main__':
    main_display = MainDisplay()
    main_display.main()


