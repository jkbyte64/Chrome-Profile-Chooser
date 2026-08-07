import pathlib
import tkinter as tk
import subprocess as sp

from tkinter import ttk
from gui_utils import ToolTip
from gc_profile import Profile
from PIL import Image, ImageTk
from typing import Optional, Dict, Any


class Root:
    @property
    def ProfileName(self) -> str:
        return self._profile_name.get()

    @ProfileName.setter
    def ProfileName(self, value: str):
        self._profile_name.set(value)

    @property
    def DisplayName(self) -> str:
        return self._display_name.get()

    @DisplayName.setter
    def DisplayName(self, value: str):
        self._display_name.set(value)

    @property
    def UserName(self) -> str:
        return self._user_name.get()

    @UserName.setter
    def UserName(self, value: str):
        self._user_name.set(value)

    @property
    def EmailAddr(self) -> str:
        return self._email_addr.get()

    @EmailAddr.setter
    def EmailAddr(self, value: str):
        self._email_addr.set(value)

    @property
    def IsGoogleAccount(self) -> str:
        return self._is_google_account.get()
    
    @IsGoogleAccount.setter
    def IsGoogleAccount(self, value: str):
        self._is_google_account.set(value)

    def __init__(self):
        self.__sel_profile_default_text = "(Select a profile...)"
        self.__no_sel_profile_default_text = "(No profile selected)"
        self.__current_profile: Optional[Profile] = None
        self.__profile_map: Dict[str, Optional[str]] = {
            self.__sel_profile_default_text: None
        }
        self.__profiles: Dict[str, Profile] = {}

        self.__profile_pic_dims = (128, 128)
        self.__current_shown_profile_pic: Optional[ImageTk.PhotoImage] = None

        self.__bgcolor = "#d9d9d9"
        self.__fgcolor = "#000000"
        self.__tabfg1 = "black"
        self.__tabfg2 = "white"
        self.__bgmode = "light"
        self.__tabbg1 = "#d9d9d9"
        self.__tabbg2 = "gray40"

        self.__win_title = "Google Chrome Profile Selector"
        self.__configure(600, 450)

        # For getters and setters
        self._profile_name = tk.StringVar()
        self._display_name = tk.StringVar()
        self._user_name = tk.StringVar()
        self._email_addr = tk.StringVar()
        self._is_google_account = tk.StringVar()
        self.ProfileName = "---"
        self.DisplayName = self.__no_sel_profile_default_text
        self.UserName = "---"
        self.EmailAddr = "---"
        self.IsGoogleAccount = "---"

        self.__elems: Dict[str, Any] = {}
        self.__add_elements()

    def __get_window_dimensions_for_center(self, width, height):
        # Maximize the window temporarily, to get usable width and height
        self.__win.withdraw()
        self.__win.state("zoomed")
        self.__win.update()
        usable_width = self.__win.winfo_width()
        usable_height = self.__win.winfo_height()
        self.__win.state("normal")
        self.__win.update()
        self.__win.deiconify()

        center_x = int((usable_width - width) / 2)
        center_y = int((usable_height - height) / 2)
        return f"{width}x{height}+{center_x}+{center_y}"

    def __configure(self, width, height):
        self.__win = tk.Tk(baseName=self.__win_title)
        root = self.__win

        root.title(self.__win_title)
        root.geometry(self.__get_window_dimensions_for_center(width, height))
        root.minsize(width, height)
        root.maxsize(width, height)
        root.resizable(False, False)
        root.configure(
            background="#d9d9d9",
            highlightbackground="#d9d9d9",
            highlightcolor="#000000"
        )

    def __add_elements(self):
        root = self.__win

        self.__elems["FrmProfileSel"] = tk.LabelFrame(root)
        FrmProfileSel = self.__elems["FrmProfileSel"]
        FrmProfileSel.place(relx=0.017, rely=0.022, relheight=0.167, relwidth=0.967)
        FrmProfileSel.configure(
            relief="groove",
            font="-family {Segoe UI} -size 10",
            foreground="#000000",
            text=" Profile Selector ",
            background="#d9d9d9",
            highlightbackground="#d9d9d9",
            highlightcolor="#000000",
        )

        self.__elems["ProfileSelector"] = ttk.Combobox(FrmProfileSel)
        ProfileSelector = self.__elems["ProfileSelector"]
        ProfileSelector.place(relx=0.017, rely=0.333, relheight=0.467, relwidth=0.7, bordermode="ignore")
        ProfileSelector.configure(
            background="#d9d9d9",
            foreground="#000000",
            font="-family {Segoe UI} -size 10",
            state="readonly"
        )

        self.__elems["ProfileSelectorTooltip"] = ToolTip(ProfileSelector, "Selects a profile from the list.")

        self.__elems["BtnClearSel"] = tk.Button(FrmProfileSel)
        BtnClearSel = self.__elems["BtnClearSel"]
        BtnClearSel.place(relx=0.741, rely=0.333, height=36, width=137, bordermode="ignore")
        BtnClearSel.configure(
            activebackground="#d9d9d9",
            activeforeground="black",
            background="#d9d9d9",
            compound='left',
            disabledforeground="#a3a3a3",
            font="-family {Segoe UI} -size 10",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="#000000",
            text="Clear selection",
            underline=0,
            command=lambda: self.__clear_selected_profile(manual=True)
        )
        
        self.__elems["BtnClearSelTooltip"] = ToolTip(BtnClearSel, "Clears the selected profile.")

        self.__elems["BtnStart"] = tk.Button(root)
        BtnStart = self.__elems["BtnStart"]
        BtnStart.place(relx=0.745, rely=0.9, height=36, width=140)
        BtnStart.configure(
            activebackground="#d9d9d9",
            background="#d9d9d9",
            activeforeground="black",
            compound='left',
            disabledforeground="#a3a3a3",
            font="-family {Segoe UI} -size 10",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="#000000",
            text="Start",
            underline=0,
            state="disabled",
            command=lambda: self.__start_chrome()
        )

        self.__elems["BtnStartTooltip"] = ToolTip(BtnStart, "Starts Google Chrome with the selected profile.")

        self.__elems["FrmChosenProfile"] = tk.Frame(root)
        FrmChosenProfile = self.__elems["FrmChosenProfile"]
        FrmChosenProfile.place(relx=0.017, rely=0.222, relheight=0.656, relwidth=0.967)
        FrmChosenProfile.configure(
            relief="groove",
            borderwidth="2",
            background="#d9d9d9",
            highlightbackground="#d9d9d9",
            highlightcolor="#000000"
        )

        self.__elems["EtyUserName"] = tk.Entry(FrmChosenProfile)
        EtyUserName = self.__elems["EtyUserName"]
        EtyUserName.place(relx=0.328, rely=0.441, height=25, relwidth=0.645)
        EtyUserName.configure(
            background="#d9d9d9",
            disabledforeground="#a3a3a3",
            exportselection=False,
            font="-family {Segoe UI} -size 11",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="#000000",
            insertbackground="#000000",
            readonlybackground="#d9d9d9",
            relief="flat",
            selectbackground="#d9d9d9",
            selectforeground="black",
            state='readonly',
            textvariable=self._user_name
        )

        self.__elems["EtyEmail"] = tk.Entry(FrmChosenProfile)
        EtyEmail = self.__elems["EtyEmail"]
        EtyEmail.place(relx=0.328, rely=0.644, height=25, relwidth=0.645)
        EtyEmail.configure(
            background="#d9d9d9",
            disabledforeground="#a3a3a3",
            exportselection=False,
            font="-family {Segoe UI} -size 11",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="#000000",
            insertbackground="#000000",
            readonlybackground="#d9d9d9",
            relief="flat",
            selectbackground="#d9d9d9",
            selectforeground="black",
            state='readonly',
            textvariable=self._email_addr
        )

        self.__elems["EtyProfileName"] = tk.Entry(FrmChosenProfile)
        EtyProfileName = self.__elems["EtyProfileName"]
        EtyProfileName.place(relx=0.328, rely=0.847, height=25, relwidth=0.645)
        EtyProfileName.configure(
            background="#d9d9d9",
            disabledforeground="#a3a3a3",
            exportselection=False,
            font="-family {Segoe UI} -size 11",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="#000000",
            insertbackground="#000000",
            readonlybackground="#d9d9d9",
            relief="flat",
            selectbackground="#d9d9d9",
            selectforeground="black",
            state='readonly',
            textvariable=self._profile_name
        )

        self.__elems["ProfilePic"] = tk.Canvas(FrmChosenProfile)
        ProfilePic = self.__elems["ProfilePic"]
        ProfilePic.place(
            relx=0.034, rely=0.068,
            width=self.__profile_pic_dims[0], height=self.__profile_pic_dims[1]
        )
        ProfilePic.configure(
            background="#d9d9d9",
            borderwidth="2",
            highlightbackground="#d9d9d9",
            highlightcolor="#000000",
            insertbackground="#000000",
            relief="ridge",
            selectbackground="#d9d9d9",
            selectforeground="black"
        ) 

        self.__elems["LblIsGA"] = tk.Label(FrmChosenProfile)
        LblIsGA = self.__elems["LblIsGA"]
        LblIsGA.place(relx=0.328, rely=0.237, height=21, width=155)
        LblIsGA.configure(
            activebackground="#d9d9d9",
            activeforeground="black",
            anchor="w",
            background="#d9d9d9",
            compound="left",
            disabledforeground="#a3a3a3",
            font="-family {Segoe UI} -size 11 -weight bold",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="#000000",
            justify="right",
            text="Is Google Account?"
        )

        self.__elems["LblUserName"] = tk.Label(FrmChosenProfile)
        LblUserName = self.__elems["LblUserName"]
        LblUserName.place(relx=0.328, rely=0.339, height=21, width=155)
        LblUserName.configure(
            activebackground="#d9d9d9",
            activeforeground="black",
            anchor="w",
            background="#d9d9d9",
            compound="left",
            disabledforeground="#a3a3a3",
            font="-family {Segoe UI} -size 11 -weight bold",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="#000000",
            justify="right",
            text="User name:"
        )

        self.__elems["LblEmail"] = tk.Label(FrmChosenProfile)
        LblEmail = self.__elems["LblEmail"]
        LblEmail.place(relx=0.328, rely=0.542, height=21, width=155)
        LblEmail.configure(
            activebackground="#d9d9d9",
            activeforeground="black",
            anchor="w",
            background="#d9d9d9",
            compound="left",
            disabledforeground="#a3a3a3",
            font="-family {Segoe UI} -size 11 -weight bold",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="#000000",
            justify="right",
            text="E-mail:"
        )

        self.__elems["LblProfileName"] = tk.Label(FrmChosenProfile)
        LblProfileName = self.__elems["LblProfileName"]
        LblProfileName.place(relx=0.328, rely=0.746, height=21, width=155)
        LblProfileName.configure(
            activebackground="#d9d9d9",
            activeforeground="black",
            anchor="w",
            background="#d9d9d9",
            compound="left",
            disabledforeground="#a3a3a3",
            font="-family {Segoe UI} -size 11 -weight bold",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="#000000",
            justify="right",
            text="Profile name:"
        )

        self.__elems["LblDisplayName"] = tk.Label(FrmChosenProfile)
        LblDisplayName = self.__elems["LblDisplayName"]
        LblDisplayName.place(relx=0.328, rely=0.068, height=41, width=374)
        LblDisplayName.configure(
            activebackground="#d9d9d9",
            activeforeground="black",
            anchor="w",
            background="#d9d9d9",
            compound="left",
            disabledforeground="#a3a3a3",
            font="-family {Segoe UI} -size 16 -weight bold",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="#000000",
            textvariable=self._display_name
        )

        self.__elems["EtyIsGA"] = tk.Entry(FrmChosenProfile)
        EtyIsGA = self.__elems["EtyIsGA"]
        EtyIsGA.place(relx=0.586, rely=0.237, height=25, relwidth=0.386)
        EtyIsGA.configure(
            background="#d9d9d9",
            disabledforeground="#a3a3a3",
            exportselection=False,
            font="-family {Segoe UI} -size 11",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="#000000",
            insertbackground="#000000",
            readonlybackground="#d9d9d9",
            relief="flat",
            selectbackground="#d9d9d9",
            selectforeground="black",
            state="readonly",
            textvariable=self._is_google_account
        )

        self.__elems["BtnExit"] = tk.Button(root)
        BtnExit = self.__elems["BtnExit"]
        BtnExit.place(relx=0.017, rely=0.9, height=36, width=140)
        BtnExit.configure(
            activebackground="#d9d9d9",
            activeforeground="black",
            background="#d9d9d9",
            command=root.destroy,
            compound="left",
            disabledforeground="#a3a3a3",
            font="-family {Segoe UI} -size 10",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="#000000",
            text="Exit",
            underline=0
        )

        self.__elems["BtnExitTooltip"] = ToolTip(BtnExit, "Exits the program.")

    def __clear_selected_profile(self, manual=False):
        if manual:
            self.__current_profile = None
            ProfileSelector: ttk.Combobox = self.__elems["ProfileSelector"]
            ProfileSelector.current(0)
            BtnClearSel: tk.Button = self.__elems["BtnClearSel"]
            BtnClearSel.focus()

        self.__disable_start_button()

        ProfilePic: tk.Canvas = self.__elems["ProfilePic"]
        ProfilePic.delete()
        self.__current_shown_profile_pic = None
        
        LblDisplayName: tk.Label = self.__elems["LblDisplayName"]
        LblDisplayName.configure(text=self.__no_sel_profile_default_text)
        self.DisplayName = self.__no_sel_profile_default_text
        self.IsGoogleAccount = "---"
        self.UserName = "---"
        self.EmailAddr = "---"
        self.ProfileName = "---"

    def __disable_start_button(self):
        BtnStart: tk.Button = self.__elems["BtnStart"]
        BtnStart.configure(state="disabled")

    def __enable_start_button(self):
        BtnStart: tk.Button = self.__elems["BtnStart"]
        BtnStart.configure(state="normal")

    def __set_selected_profile(self, event: tk.Event[ttk.Combobox]):
        cbox: ttk.Combobox = self.__elems["ProfileSelector"]
        sel_profile_name = self.__profile_map[cbox.get()]
        if not sel_profile_name or not sel_profile_name.strip():
            self.__current_profile = None
        else:
            self.__current_profile = self.__profiles[sel_profile_name]
        self.__show_selected_profile()

    def __show_selected_profile(self):
        profile = self.__current_profile
        if not profile:
            self.__clear_selected_profile()
            return
        else:
            self.__enable_start_button()

        ProfilePic: tk.Canvas = self.__elems["ProfilePic"]
        if profile.is_google_account:
            resized_pic = None
            if profile.ga_pic:
                resized_pic = profile.ga_pic.resize(self.__profile_pic_dims, Image.Resampling.LANCZOS)
            elif profile.itl_avatar:
                resized_pic = profile.itl_avatar.resize(self.__profile_pic_dims, Image.Resampling.LANCZOS)
            else:
                ProfilePic.delete("ProfilePic")
                self.__current_shown_profile_pic = None
                return

            if resized_pic:
                self.__current_shown_profile_pic = ImageTk.PhotoImage(resized_pic)
                ProfilePic.create_image(0, 0, anchor="nw", image=self.__current_shown_profile_pic, tags="ProfilePic")
        elif profile.avatar_icon.strip() and profile.itl_avatar:
            resized_pic = profile.itl_avatar.resize(self.__profile_pic_dims, Image.Resampling.LANCZOS)
            self.__current_shown_profile_pic = ImageTk.PhotoImage(resized_pic)
            ProfilePic.create_image(0, 0, anchor="nw", image=self.__current_shown_profile_pic, tags="ProfilePic")
        else:
            ProfilePic.delete("ProfilePic")
            self.__current_shown_profile_pic = None

        self.ProfileName = profile.name
        self.DisplayName = profile.display_name
        if profile.is_google_account:
            self.IsGoogleAccount = "Yes"
            self.UserName = profile.ga_name
            self.EmailAddr = profile.ga_username
        else:
            self.IsGoogleAccount = "No"
            self.UserName = profile.display_name
            self.EmailAddr = "N/A"

    def __start_chrome(self):
        if self.__current_profile:
            chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
            chrome_fp = pathlib.Path(chrome_path).resolve()
            cmd = [
                str(chrome_fp), f"--profile-directory={self.__current_profile.name}",
                "--start-maximized"
            ]
            sp.Popen(cmd)
            self.__win.destroy()

    def fill_profile_selector(self, profiles: Dict[str, Profile]):
        self.__profiles = profiles
        for k in self.__profiles.keys():
            self.__profile_map[self.__profiles[k].display_name] = k
        
        cbox: ttk.Combobox = self.__elems["ProfileSelector"]
        cbox.delete(0, "end")
        cbox.configure(
            values=list(self.__profile_map.keys()),
        )
        cbox.current(0)
        cbox.bind("<<ComboboxSelected>>", self.__set_selected_profile)

    def start(self):
        self.__win.mainloop()
