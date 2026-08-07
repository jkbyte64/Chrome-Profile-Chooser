import re
import os
import json
import pathlib
import requests

from util import err_and_exit

from PIL import Image
from io import BytesIO
from typing import Optional, Dict, Annotated
from pydantic import BaseModel, ConfigDict, Field
from pydantic.json_schema import SkipJsonSchema


def get_profiles_from_json_config() -> Dict[str, Profile]:
    path_chunks = [
        os.environ.get("LOCALAPPDATA"), "Google", "Chrome", "User Data", "Local State"
    ]
    fp = pathlib.Path(os.path.join(*path_chunks)).resolve()
    if not fp.exists() or not fp.is_file():
        err_and_exit(f"The Local State file \"{str(fp)}\" is not a file or doesn't exist!")

    result = {}

    with fp.open("r", encoding="utf-8") as fhand:
        json_info = json.load(fhand)["profile"]
        for pfname in json_info["profiles_order"]:
            result[pfname] = Profile.from_json(pfname, json_info["info_cache"][pfname])

    return result


class Profile(BaseModel):
    __path_chunks = [
        os.environ.get("LOCALAPPDATA"), "Google", "Chrome", "User Data"
    ]

    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str = ""
    dp: Optional[pathlib.Path] = None
    display_name: str = ""
    shortcut_name: str = ""
    avatar_icon: str = ""
    is_google_account: bool = False
    ga_name: str = ""
    ga_username: str = ""
    ga_pic_url: str = ""
    ga_pic: Annotated[Optional[Image.Image], SkipJsonSchema, Field(exclude=True)] = None
    itl_avatar: Annotated[Optional[Image.Image], SkipJsonSchema, Field(exclude=True)] = None

    def __str__(self):
        return self.model_dump_json(indent=2)

    def __download_ga_pic_from_url(self):
        response = requests.get(self.ga_pic_url)
        self.ga_pic = Image.open(BytesIO(response.content))

    def __get_itl_avatar(self):
        match = re.search(r".*\/IDR\_PROFILE\_AVATAR\_([0-9]+)", self.avatar_icon)
        if not self.avatar_icon.strip() or not match:
            self.itl_avatar = None
            return

        dp = pathlib.Path( pathlib.Path(__file__).resolve().parent / "itl-avatars" ).resolve()
        if not dp.exists() and not dp.is_dir():
            self.itl_avatar = None
            return

        fp = pathlib.Path(dp / f"{int(match.group(1)):02d}.png")
        if not fp.exists() and not fp.is_file():
            self.itl_avatar = None
            return

        self.itl_avatar = Image.open(fp)

    @classmethod
    def from_json(cls, pfname, jo):
        result = cls()

        result.name = pfname
        result.dp = pathlib.Path(os.path.join(*result.__path_chunks)) / result.name
        result.display_name = jo["name"]
        result.shortcut_name = jo["shortcut_name"]
        result.avatar_icon = jo["avatar_icon"]
        result.__get_itl_avatar()

        if "last_downloaded_gaia_picture_url_with_size" in jo:
            result.is_google_account = True
            result.ga_name = jo["gaia_name"]
            result.ga_username = jo["user_name"]
            result.ga_pic_url = jo["last_downloaded_gaia_picture_url_with_size"]
            result.__download_ga_pic_from_url()
        else:
            result.is_google_account = False
            result.ga_name = ""
            result.ga_username = ""
            result.ga_pic_url = ""
            result.ga_pic = None

        return result
