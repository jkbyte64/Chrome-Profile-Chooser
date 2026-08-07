#!/usr/bin/env python3

from gui import Root
from gc_profile import get_profiles_from_json_config


def main():
    profile_info = get_profiles_from_json_config()
    root = Root()
    root.fill_profile_selector(profile_info)
    root.start()


if __name__ == "__main__":
    main()
