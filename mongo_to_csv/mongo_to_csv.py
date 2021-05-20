import os
import pymongo
from datetime import datetime, timedelta
from pprint import pprint
import PySimpleGUI as sg


class Mongo:
    def __init__(self):
        self.client = None
        self.dbs = None
        self.collections = None

        self.selected_db = None
        self.selected_collection = None

    def connect_client(self, host, port, username, password):
        try:
            self.client = pymongo.MongoClient(host, int(port), username=username, password=password)
            self.dbs = self.client.list_database_names()
            return True
        # TODO; pymongo.errors.OperationFailure等、他のエラー時の処理
        except pymongo.errors.ConnectionFailure:
            print("Failed to connect to server")
            return False

    def select_db(self, db_name):
        self.selected_db = self.client[db_name]

    def get_collections(self):
        self.collections = self.selected_db.list_collection_names()
        return self.collections

    def select_collection(self, collection_name):
        self.selected_collection = self.selected_db[collection_name]

    def add_one(self):
        post = {
            'title': 'あいうえお',
            'content': 'かきくけこ',
            'created_at': datetime.now()
        }
        return self.selected_db.test.insert_one(post)

    def get_item(self):
        data = []
        for d in self.selected_collection.find():
            data.append(d)
        return data

    def find(self, filter_={}):
        data = []
        for d in self.selected_collection.find(filter=filter_):
            data.append(d)
        return data

    def find_recent(self, datetime_key, filter_={}):
        data = []
        for d in self.selected_collection.find(filter=filter_).sort(datetime_key, pymongo.DESCENDING).limit(100):
            data.append(d)
        return data

    def get_fields(self):
        fields = []
        # TODO 'datetime'でソートしているが、そのドキュメントの時間keyを判定してからソートする
        for d in self.selected_collection.find().sort('datetime', pymongo.DESCENDING).limit(1000):
            [fields.append(k) for k in d.keys()]
        fields = list(set(fields))
        try:
            fields.remove('_id')
        except ValueError:
            pass
        return fields

    def get_values(self, field):
        values = []
        # TODO 'datetime'でソートしているが、そのドキュメントの時間keyを判定してからソートする
        for d in self.selected_collection.find().sort('datetime', pymongo.DESCENDING).limit(1000):
            values.append(d[field])
        values = list(set(values))
        return values


class Option:
    def __init__(self):
        self.export_path = __file__
        self.host = 'localhost'
        self.port = '27017'
        self.username = ''
        self.password = ''


class MainDisplay:
    def __init__(self):
        self.option = Option()
        self.mongo = Mongo()

        sg.theme('DarkBlue12')

        self.field_conditions_tab1 = [
            [sg.InputText('', size=(20, 1), key='-FIELD1-'), sg.Text(':'),
             sg.InputText('', size=(20, 1), key='-VALUE1-')],
            [sg.InputText('', size=(20, 1), key='-FIELD2-'), sg.Text(':'),
             sg.InputText('', size=(20, 1), key='-VALUE2-')],
            [sg.InputText('', size=(20, 1), key='-FIELD3-'), sg.Text(':'),
             sg.InputText('', size=(20, 1), key='-VALUE3-')],
        ]

        self.field_conditions_tab2 = [
            [sg.Combo(values=(), size=(20, 5), key='-FIELDS1-'), sg.Text(':'),
             sg.Combo(values=(), size=(20, 5), key='-VALUES1-')],
        ]

        self.field_conditions = [
            [sg.TabGroup([[sg.Tab('tab1', self.field_conditions_tab1),
                           sg.Tab('tab2', self.field_conditions_tab2)]], key='-CONDITIONTAB-')]
        ]

        self.condition_layout = [
            [self.field_conditions],
            [sg.Combo(values=(), size=(15, 5), key='-DATETIME-'),
             sg.Input(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'), size=(20, 1), key='-CALENDAR-'),
             sg.CalendarButton('calendar'),
             sg.Input('1', size=(2, 1), key='-AGONUM-'),
             sg.InputCombo(('sec', 'min', 'hour', 'day'), default_value='min', key='-AGOUNIT-'),
             sg.Text('ago data find.')],
        ]

        self.layout = [
            [sg.Text('', size=(55, 1)), sg.Button(button_text='Option', key='-OPTION-', )],
            [sg.Text('Database List', size=(30, 1)), sg.Text('Collections')],
            [sg.Listbox(values=(), size=(30, 5), key='-DATABASELIST-'),
             sg.Text('⇒'),
             sg.Listbox(values=(), size=(30, 5), key='-COLLECTIONLIST-')],
            [sg.Button(button_text='Select Database', key='-DATABASE-'),
             sg.Text('', size=(18, 1)),
             sg.Button(button_text='Select Collection', key='-COLLECTION-')],
            [sg.HorizontalSeparator()],
            [sg.Text('Setting find Conditions.')],
            [self.condition_layout],
            [sg.Button('Find', key='-FIND-'), sg.Button('Find Recent', key='-RECENT-')],
            [sg.Multiline(default_text='', size=(70, 20), key='-DATA-')]
        ]
        self.window = sg.Window(title='MongoToCsv', layout=self.layout, finalize=True)

        # TODO: 起動時DB接続は停止中、ConnectionFailureの場合メッセージが出るのに時間がかかるため起動が遅くなる
        # if self.mongo.connect_client(self.option.host, self.option.port, self.option.username, self.option.password):
        #     self.window['-DATABASELIST-'].update(values=self.mongo.dbs)

    def call_option_display(self):
        option_display = OptionDisplay(self.option, self.mongo)
        client_updated = option_display.main()
        if client_updated:
            self.window['-DATABASELIST-'].update(values=self.mongo.dbs)
        del option_display

    def get_field_condition(self, filter_, values, tab_name):
        if tab_name == 'tab1':
            for i in range(1, 4):
                if values['-FIELD' + str(i) + '-'] != '' and values['-VALUE' + str(i) + '-'] != '':
                    filter_[values['-FIELD' + str(i) + '-']] = values['-VALUE' + str(i) + '-']
        elif tab_name == 'tab2':
            if values['-FIELDS1-'] != '' and values['-VALUES1-'] != '':
                filter_[values['-FIELDS1-']] = values['-VALUES1-']

    def get_datetime_condition(self, filter_, values):
        # 時間差分を算出
        if values['-AGOUNIT-'] == 'sec':
            delta = timedelta(seconds=int(values['-AGONUM-']))
        elif values['-AGOUNIT-'] == 'min':
            delta = timedelta(minutes=int(values['-AGONUM-']))
        elif values['-AGOUNIT-'] == 'hour':
            delta = timedelta(hours=int(values['-AGONUM-']))
        elif values['-AGOUNIT-'] == 'day':
            delta = timedelta(days=int(values['-AGONUM-']))
        # 開始時間、終了時間を設定
        end_time = datetime.strptime(values['-CALENDAR-'].split('.')[0], '%Y-%m-%d %H:%M:%S')
        start_time = end_time - delta
        filter_[values['-DATETIME-']] = {'$gte': start_time, '$lt': end_time}

    def set_fields(self):
        fields = self.mongo.get_fields()
        self.window['-FIELDS1-'].update(values=fields)
        self.window['-DATETIME-'].update(values=fields)

    def set_values(self, field):
        values = self.mongo.get_values(field)
        self.window['-VALUES1-'].update(values=values)

    def main(self):
        fields1 = ''

        while True:
            event, values = self.window.read(timeout=1000, timeout_key='-TIMEOUT-')
            # print(event, values)
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
                self.set_fields()
            if event == '-FIND-':
                if len(values['-COLLECTIONLIST-']) <= 0 or self.mongo.selected_collection is None:
                    continue
                filter_ = {}
                self.get_field_condition(filter_, values, values['-CONDITIONTAB-'])
                self.get_datetime_condition(filter_, values)
                data = self.mongo.find(filter_)
                self.window['-DATA-'].update(value=data)
            if event == '-RECENT-':
                if len(values['-COLLECTIONLIST-']) <= 0 or self.mongo.selected_collection is None:
                    continue
                filter_ = {}
                self.get_field_condition(filter_, values, values['-CONDITIONTAB-'])
                data = self.mongo.find_recent(datetime_key=values['-DATETIME-'], filter_=filter_)
                self.window['-DATA-'].update(value=data)
            if event == '-TIMEOUT-':
                if values['-FIELDS1-'] != '' and values['-FIELDS1-'] != fields1:
                    self.set_values(values['-FIELDS1-'])
                    fields1 = values['-FIELDS1-']

        self.window.close()


class OptionDisplay:
    def __init__(self, option, mongo):
        self.option = option
        self.mongo = mongo

        sg.theme('DarkBlue11')
        tab1_layout = [
            [sg.Text('host', size=(5, 1)), sg.Input(option.host, size=(15, 1), key='host'), sg.Text('', size=(3, 1)),
             sg.Text('username', size=(7, 1)), sg.Input(option.username, size=(15, 1), key='username')],
            [sg.Text('port', size=(5, 1)), sg.Input(option.port, size=(15, 1), key='port'), sg.Text('', size=(3, 1)),
             sg.Text('password', size=(7, 1)),
             sg.Input(option.password, size=(15, 1), password_char= '*', key='password')],
            [sg.Submit(button_text='Connect MongoDB'),
             sg.Text(key='Connect MongoDB Result', size=(15, 1))]
        ]
        tab2_layout = [
            [sg.Text('export', size=(5, 1)),
             sg.InputText(os.path.dirname(self.option.export_path), key='-EXPORTPATH-'),
             sg.FolderBrowse()]
        ]
        self.layout = [
            [sg.TabGroup([[sg.Tab('Connect', tab1_layout), sg.Tab('Export', tab2_layout)]])],
            [sg.Text('', size=(45, 1)), sg.OK(key='-SAVEOPTION-'), sg.Exit()]
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
                if self.mongo.connect_client(values['host'], values['port'], values['username'], values['password']):
                    self.window['Connect MongoDB Result'].update('Success!', text_color=("#0000ff"))
                    client_updated = True
                else:
                    self.window['Connect MongoDB Result'].update('Error!', text_color=('#ff0000'))
            if event == '-SAVEOPTION-':
                self.option.host = values['host']
                self.option.port = values['port']
                self.option.username = values['username']
                self.option.password = values['password']
                self.option.export_path = values['-EXPORTPATH-']
                break
        self.window.close()
        return client_updated


if __name__ == '__main__':
    main_display = MainDisplay()
    main_display.main()


