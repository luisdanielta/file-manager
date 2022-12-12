from core import Base, time, os
from core.components import Button, Container, CheckButton, Table, AppMenu, MenuButton, Text
from view.config import Config
from view.plugins import Plugins


class App(Base):

    def __init__(self):
        super().__init__()
        self.title("File Manager")
        self.resizable(False, False)

        # menu
        self.menu = AppMenu(self, {
            'Config': Config,
            'Plugins': Plugins,
            'About': self.send_about,
            'Exit': self.destroy
        })

        # btn select folder
        self.sf_btn = Button(self, 'Select Folder', {
            'row': 0, 'column': 0, 'sticky': 'nsew',
            'padx': 5, 'pady': 5
        }, command=self.handle_sf_btn)

        # btn select file
        self.stf_btn = Container(self, 'Select of types file', {  # container type file
            'row': 2, 'column': 0, 'sticky': 'nsew',
            'padx': 5, 'pady': 5
        })

        # btn´s select types - position
        self.p_btn = self.get_info('position')['buttons']
        for btn in self.p_btn.keys():
            row = self.p_btn[btn][0]
            column = self.p_btn[btn][1]
            grid = {
                'row': row, 'column': column, 'sticky': 'nsew',
                'padx': 3, 'pady': 3
            }

            globals()[btn] = Button(self.stf_btn, btn, grid=grid,
                                    state='disabled',
                                    command=lambda btn=btn: self.handle_stf_btn(btn)) if self.OP_BTNS else MenuButton(
                self.stf_btn, btn, grid=grid, options=self.BUTTONS[btn],
                state='disabled', command=lambda btn=self.BUTTONS[btn]: self.handle_stf_btn(btn))

        # container btn check
        self.ct_btn_check = Container(self, 'Tools', {
            'row': 3, 'column': 0, 'sticky': 'nsew',
            'padx': 5, 'pady': 5
        })

        # btn check subfolders
        self.subf_btn = CheckButton(self.ct_btn_check, 'Include subfolders', {
            'row': 2, 'column': 0, 'sticky': 'nsew',
            'padx': 5, 'pady': 5
        }, variable=self.STATE,
            command=lambda msg='This option can take a long time, depending on the number of files and size': self.warning_msg(
                active=self.subf_btn.get_state(), msg=msg
        ))

        # btn check copy
        self.copy_btn = CheckButton(self.ct_btn_check, 'Copy files', {
            'row': 2, 'column': 1, 'sticky': 'nsew',
            'padx': 5, 'pady': 5
        }, variable=self.STATE)

        # btn check move
        self.move_btn = CheckButton(self.ct_btn_check, 'Move files', {
            'row': 2, 'column': 2, 'sticky': 'nsew',
            'padx': 5, 'pady': 5
        }, variable=self.STATE)

        # table routes recents
        self.table = Table(self, ('Route', 'Date'), {
            'row': 4, 'column': 0, 'sticky': 'nsew',
            'padx': 5, 'pady': 5
        }, [190, 60], height=5)

        # container buttons table
        self.ct_btn = Container(self, 'Actions', {
            'row': 5, 'column': 0, 'sticky': 'nsew',
            'padx': 5, 'pady': 5
        })

        self.ct_btn.columnconfigure(0, weight=1)
        self.ct_btn.columnconfigure(1, weight=1)

        # btn select route
        self.sr_btn = Button(self.ct_btn, 'Select Route', {
            'row': 0, 'column': 0, 'sticky': 'nsew',
            'padx': 5, 'pady': 5
        })

        # btn delete route
        self.dr_btn = Button(self.ct_btn, 'Delete Route', {
            'row': 0, 'column': 1, 'sticky': 'nsew',
            'padx': 10, 'pady': 5
        })

    # handle events

    def handle_sf_btn(self):
        self.open_folder()
        if self.PATH:
            self.txt_path = Text(self, self.PATH, {
                'row': 1, 'column': 0, 'sticky': 'nsew',
                'padx': 5, 'pady': 5
            }, anchor='center')
            for btn in self.p_btn.keys():
                globals()[btn].config(state='normal')

    def handle_stf_btn(self, type_btn):
        # get copy - move - subfolders
        t_init = time.time()
        copy = self.copy_btn.get_state()
        move = self.move_btn.get_state()
        subf = self.subf_btn.get_state()

        # messagebox, copy - move one select
        if copy and move:
            self.error_msg(msg='Select only one option (copy or move)')
            return

        if not copy and not move:
            self.error_msg(msg='Select one option (copy or move)')
            return

        types = self.get_info('files')
        files = os.listdir(self.PATH)
        try:
            # add extension .upper()
            ext = types[type_btn]
            for i in range(len(ext)):
                ext.append(ext[i].upper())

        except KeyError:
            ext = [type_btn, type_btn.upper()]
            type_btn = type_btn.split('.')[1]

        if not os.path.exists(f'{self.PATH}/{type_btn}'):  # if folder not exists
            os.mkdir(f'{self.PATH}/{type_btn}')

        if subf == 1:
            s_folders = self.find_subf()
            for subfolder in s_folders:
                files = os.listdir(subfolder)
                for file in files:
                    if move:
                        self.move_file(file, subfolder, type_btn, ext)
                    elif copy:
                        self.copy_file(file, subfolder, type_btn, ext)

        for file in files:
            if file.endswith(tuple(ext)):
                if move:
                    self.move_file(file, self.PATH, type_btn, ext)
                elif copy:
                    self.copy_file(file, self.PATH, type_btn, ext)

        t_end = time.time()
        t = round(t_end - t_init, 2)
        # messagebox, process completed
        self.info_msg(msg=f'Process completed in {t} seconds.')


if __name__ == "__main__":
    app = App()
    app.mainloop()
