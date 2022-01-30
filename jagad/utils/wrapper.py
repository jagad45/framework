import textwrap

def wrap_string(s: str, width: int =40, indent: int =32, indentAll: bool =False, followingHeader=None):
    # This function copy from 'Empire Framework'
    # See https://github.com/EmpireProject/Empire/blob/master/lib/common/messages.py
    output = ""

    if len(s) > width:
        text = textwrap.dedent(s).strip()
        lines = textwrap.wrap(text, width)
        if indentAll:
            output = " " * indent + lines[0]
            if followingHeader:
                output += " " * followingHeader
        else:
            output = lines[0]
            if followingHeader:
                output += " " + followingHeader
        index = 0
        while index < len(lines):
            output += "\n" + " " * indent + (lines[index]).strip()
            index += 1
        return output
    else:
        return s.strip()