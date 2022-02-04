import io
import sys
import glob
from enum import Enum, auto

class BibParserState(Enum):
    SEEK_AT_SIGN    = auto()
    READ_ENTRY_TYPE = auto()
    READ_IDENTIFIER = auto()
    SEEK_KEY_OR_END = auto()
    READ_KEY        = auto()
    READ_VALUE      = auto()

def is_allowed_in_identifier(ch):
    try:
        # see https://tex.stackexchange.com/questions/408530/what-characters-are-allowed-to-use-as-delimiters-for-bibtex-keys
        if ch.isalnum() or '"-:!=;?'.index(ch) >= 0:
            return True
    except:
        return False

class Bibliography:
    def __init__(self):
        self.bib = None
        self.bibfile = None
        self.bibfilename = None
        self.hasbibfile = False
        self.bibfileok = False
        self.bibfileerrors = None
        
        for file in glob.glob("*.bib"):
            self.bibfilename = file
            self.hasbibfile = True
            break

        if self.hasbibfile:
            self.bibfile = io.open(self.bibfilename, "r", encoding="utf8")
            bib, errors = self.parsebibfile(self.bibfile.read())

            if len(errors) == 0:
                self.bib = bib
                self.bibfileok = True
            else:
                self.bibfileerrors = errors
        else:
            self.bibfileerrors = ['no bib file has been loaded - any file ending with .bib will be loaded from the same folder as the .tex files if it exists']

    def cite(self, obj):
        index, content = self.rendercitation(self.parsearg(obj, 0))
        display = index

        if len(obj.opts) > 0:
            optname = self.parseopt(obj, 0)
            display += f', {optname}'

        return f'<span class="bubblelabel">[{display}]</span><span class="bubblecontent">[{index}]: {content}</span>'

    def bibliography(self, obj):
        if not self.bibfileok:
            return f'<span style="color: red;">\\bibliography error. {self.displaybibfileerrors()}</span>'

        output = '<ol class="bibliography">'

        for key in self.bib:
            index, content = self.rendercitation(key)
            output += f'<li>{content}</li>'

        output += '</ol>'

        return output

    def displaybibfileerrors(self):
        errors = ''
        for error in self.bibfileerrors:
            errors += f'<li>{error}</li>'
        return f'The following went wrong: <ol>{errors}</ol>'

    def validatebibentry(self, key):
        error = None
        requiredfields = ['title', 'author']

        if self.hasbibfile:
            if self.bibfileok:
                if key in self.bib:
                    entry = self.bib[key]
                    valid = True
                    missingfields = []
                    for field in requiredfields:
                        if not field in entry.keys():
                            valid = False
                            missingfields.append(field)
                    if valid:
                        return True, None
                    else:
                        missingstr = ', '.join(missingfields)
                        error = f'bib file entry "{key}" is missing the following required fields: {missingstr}'
                else:
                    error = f'no such entry "{key}" in bib file'
            else:
                error = f'something went wrong when reading the .bib file. {self.displaybibfileerrors()}'
        else:
            error = self.displaybibfileerrors()

        return False, error

    def rendercitation(self, key):
        ok, error = self.validatebibentry(key)

        if not ok:
            return 'error', f'citation failed: {error}'

        entry = self.bib[key]
        index = entry['id']
        content = entry['author'] + '. <i>' + entry['title'] + '</i>'

        return index, content

    def parsebibfile(self, contents):
        """
        Grammar:

        <entry>
        <entry>
        ...
        <entry>

        where <entry> is of the form

        @<type>{<identifier>,
          <key>={<value>},
          <key>={<value>},
          ...,
          <key>={<value>}
        }
        """
        counter = 1
        errors = []
        bib = {}
        ptr = 0
        state = BibParserState.SEEK_AT_SIGN
        buf = ''
        entry = None
        identifier = None
        ignorewhitespace = True
        key = ''
        value = ''
        foundstartbracket = False

        while True:
            ch = None
            
            try:
                ch = contents[ptr]
            except:
                if state != BibParserState.SEEK_AT_SIGN:
                    errors.append(f'File ended before parsing was finished! Perhaps you forgot a }}?')
                break

            if ignorewhitespace:
                if ch.isspace():
                    ptr += 1
                    continue

            if state == BibParserState.SEEK_AT_SIGN:
                if ch == '@':
                    state = BibParserState.READ_ENTRY_TYPE
                    buf = ''
                    entry = {}
                    entry['id'] = str(counter)
                    counter += 1
                else:
                    errors.append(f'Expected "@" while looking for a new entry, found "{ch}"')
                    break
                ptr += 1

            elif state == BibParserState.READ_ENTRY_TYPE:
                if ch.isalpha():
                    buf += ch
                else:
                    if ch == '{':
                        entry['type'] = buf
                        buf = ''
                        ignorewhitespace = True
                        state = BibParserState.READ_IDENTIFIER
                    else:
                        errors.append(f'Expected "{{"" after reading entry type, found "{ch}"')
                        break
                ptr += 1

            elif state == BibParserState.READ_IDENTIFIER:
                if is_allowed_in_identifier(ch):
                    buf += ch
                else:
                    if ch == ',':
                        identifier = buf
                        ignorewhitespace = True
                        state = BibParserState.SEEK_KEY_OR_END
                    else:
                        errors.append(f'Expected "," after reading entry identifier, found "{ch}". That character is not allowed in the identifier of a reference')
                        break
                ptr += 1

            elif state == BibParserState.SEEK_KEY_OR_END:
                if ch == '}':
                    ignorewhitespace = True
                    state = BibParserState.SEEK_AT_SIGN
                    ptr += 1
                else:
                    if ch.isalpha():
                        state = BibParserState.READ_KEY
                        key = ''
                    elif ch == ',':
                        ptr += 1
                    else:
                        errors.append(f'Unexpected character "{ch}" while looking for key name')
                        break

            elif state == BibParserState.READ_KEY:
                if ch.isalpha():
                    key += ch
                    ptr += 1
                elif ch == '=':
                    ptr += 1
                    value = ''
                    foundstartbracket = False
                    state = BibParserState.READ_VALUE
                else:
                    errors.append(f'Unexpected character "{ch}" while reading key name, expected an alphabetic character, or a "="')
                    break

            elif state == BibParserState.READ_VALUE:
                if not foundstartbracket:
                    if ch == '{':
                        foundstartbracket = True
                        ignorewhitespace = False
                        ptr += 1
                    else:
                        errors.append(f'Unexpected character "{ch}" while looking for {{')
                        break
                else:
                    if ch == '{':
                        errors.append(f'Did not expect to see "{{" while reading a value, perhaps you forgot to terminate with a "}}"')
                        break
                    elif ch != '}':
                        value += ch
                    else:
                        entry[key] = value
                        bib[identifier] = entry
                        ignorewhitespace = True
                        state = BibParserState.SEEK_KEY_OR_END
                    ptr += 1

        if state == BibParserState.SEEK_KEY_OR_END:
            errors.append(f'Did not find }} to terminate book entry')

        return bib, errors