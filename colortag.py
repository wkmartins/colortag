import re
import sys

ansi_codes = {
    # bg = background
    # l = light

    # colors
    "black": "30",
    "red": "31",
    "green": "32",
    "yellow": "33",
    "blue": "34",
    "magenta": "35",
    "cyan": "36",
    "lgray": "37",
    "gray": "90",
    "lred": "91",
    "lgreen": "92",
    "lyellow": "93",
    "lblue": "94",
    "lmagenta": "95",
    "lcyan": "96",
    "white": "97",
    # colorsbg
    "blackbg": "40",
    "redbg": "41",
    "greenbg": "42",
    "yellowbg": "43",
    "bluebg": "44",
    "magentabg": "45",
    "cyanbg": "46",
    "lgraybg": "47",
    "graybg": "100",
    "lredbg": "101",
    "lgreenbg": "102",
    "lyellowbg": "103",
    "lbluebg": "104",
    "lmagentabg": "105",
    "lcyanbg": "106",
    "whitebg": "107",
    # styles
    "bold": "1",
    "dark": "2",
    "line": "4",
    "blink": "5",
    "reverse": "7",
    "hidden": "8"
}


class ColorTag(str):
    def __new__(cls, string, tags):
        instance = super().__new__(cls, string)
        if not isinstance(string, str):
            raise TypeError(f"Expected str type, received '{type(string)}'")
        if not isinstance(tags, dict):
            raise TypeError(f"Expected dict type, received '{type(tags)}'")
        for tag in tags.values():
            for attr in tag:
                if attr not in ansi_codes:
                    raise ValueError(f"Invalid attribute: '{attr}'")
        # Convert string to ansi
        # 'hello' with tag 'blue' goes to
        # \x1b[34mhello\x1b[0;39;49m
        ansi = string
        reset = "\x1b[0;39;49m"
        for (start, end), tag in reversed(tags.items()):
            codes = [ansi_codes[attr] for attr in tag]
            codes = ";".join(codes)
            codes = f"\x1b[{codes}m"
            ansi = ansi[:end] + reset + ansi[end:]
            ansi = ansi[:start] + codes + ansi[start:]

        instance._string = string
        instance._tags = tags
        instance._ansi = ansi
        return instance

    @property
    def string(self):
        return self._string

    @property
    def tags(self):
        return self._tags

    @property
    def ansi(self):
        return self._ansi

    def __getitem__(self, key):
        if isinstance(key, int):
            keytag = []
            # Check if the char in position 'key' have a tag
            # if it does, assign 'keytag' to it
            for (start, end), tag in self.tags.items():
                if key in range(start, end):
                    keytag = tag
                    break
            return ColorTag(self.string[key], {(0, 1): keytag})
        elif isinstance(key, slice):
            sliced_str = ""
            sliced_tags = {}
            kstart, kstop, kstep = key.start, key.stop, key.step
            # Define default values
            if kstart is None:
                kstart = 0
            if kstop is None:
                kstop = len(self)
            if kstep is None:
                kstep = 1
            for i in range(kstart, kstop, kstep):
                sliced_str += self[i]
                # Check if the index is on a tag
                for (start, end), tag in self.tags.items():
                    if i in range(start, end):
                        if not sliced_tags:  # If it's empty
                            last_tag = None
                        else:
                            # Get the last position-tag pair
                            last_pos, last_tag = list(sliced_tags.items())[-1]
                        if last_tag == tag:
                            # Increment the last tag 'end' position
                            # so it stack the tags instead of creating
                            # a new one for each character
                            sliced_tags.pop(last_pos)
                            last_start, last_end = last_pos
                            sliced_tags[last_start, last_end + 1] = tag
                        else:
                            # Create other tag
                            lenght = len(sliced_str)
                            sliced_tags[lenght - 1, lenght] = tag
                    last_tag = tag
            return ColorTag(sliced_str, sliced_tags)

    def __str__(self) -> str:
        return self.ansi

    def __repr__(self) -> str:
        return self.ansi

    def __add__(self, other):
        # Initializate new tags with the 'self' tags
        new_tags = self.tags
        if isinstance(other, ColorTag):
            new_str = self.string + other.string
            # Increment the tags from 'other' to fix positions
            for (start, end), tag in other.tags.items():
                new_tags[(start + len(self), end + len(self))] = tag
        elif isinstance(other, str):
            # String type has no tags so just use the tags from 'self'
            new_str = self.string + other
        else:
            raise TypeError(f"Invalid type for concatenation: '{type(other)}'")
        return ColorTag(new_str, new_tags)

    def upper(self):
        string = super().upper()
        return ColorTag(string, self.tags)

    def lower(self):
        string = super().lower()
        return ColorTag(string, self.tags)

    def capitalize(self):
        string = super().capitalize()
        return ColorTag(string, self.tags)

    def casefold(self):
        string = super().casefold()
        return ColorTag(string, self.tags)

    def title(self):
        string = super().title()
        return ColorTag(string, self.tags)

    def join(self, iterable):
        joined = c("")
        for i, value in enumerate(iterable):
            if i > 0:
                joined += self
            joined += str(value)
        return joined

    def center(self, width, char=" "):
        if width <= len(self):
            return ColorTag(self.string, self.tags)
        space = width - len(self)
        left = space // 2
        right = space - left
        centered_str = (char * left) + self.string + (char * right)
        tags = {}
        for (start, end), tag in self.tags.items():
            tags[start + left, end + left] = tag
        return ColorTag(centered_str, tags)

    def replace(self, old, new, count):
        raise NotImplementedError("Replace not yet implemented for ColorTag")


def c(string):
    """Convert string to ColorTag object"""
    pattern = r"<(.+?):([a-z; ]+)>"
    tags = {}
    for matchA in re.finditer(pattern, string):
        start, end = matchA.span(1)
        for matchB in re.finditer(pattern, string):
            if matchB.group(0) == matchA.group(0):
                word_start = re.match(pattern, matchA.group(0)).start(1)
                chars_before_word = matchA.group(0)[:word_start]
                start -= len(chars_before_word)
                end -= len(chars_before_word)
                break
            else:
                len_to_remove = len(matchB.group(0)) - len(matchB.group(1))
                start -= len_to_remove
                end -= len_to_remove
        match_tags = matchA.group(2).strip().split(";")
        tags[(start, end)] = match_tags

    matches = list(re.finditer(pattern, string))
    for match in reversed(matches):
        start, end = match.span(0)
        string = string[:start] + match.group(1) + string[end:]
    return ColorTag(string, tags)


def cprint(*strings, sep=" ", end="\n", file=sys.stdout, flush=False):
    strings = tuple([c(string) for string in strings])
    print(*strings, sep=sep, end=end, file=file, flush=flush)
