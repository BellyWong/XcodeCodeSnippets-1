#!/usr/bin/python
#
# lscs.py
#
# Lists Xcode 4 Code Snippets.
#
# Example:
# ./lscs.py
#
# Copyright 2012 Kirby Turner
#
# Version 1.0
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
import sys
import getopt

def show(filename, dict):
    title = dict['IDECodeSnippetTitle']
    if 'IDECodeSnippetSummary' in dict:
        summary = dict['IDECodeSnippetSummary']
    else:
        summary = ''
    shortcut = dict['IDECodeSnippetCompletionPrefix']
    print 'File: ' + filename
    print 'Title: ' + title
    print 'Shortcut: ' + shortcut
    print summary
    print '====='

def showAsMarkdown(filename, dict):
    title = dict['IDECodeSnippetTitle']
    if 'IDECodeSnippetSummary' in dict:
        summary = dict['IDECodeSnippetSummary']
    else:
        summary = ''
    shortcut = dict['IDECodeSnippetCompletionPrefix']
    snippet = dict['IDECodeSnippetContents']
    scope = dict['IDECodeSnippetCompletionScopes']

    print '## ' + title
    print '**Shortcut**: ' + shortcut + '  '

    url = 'http://github.com/kirbyt/Xcode4CodeSnippets/blob/master/' + filename
    print '**File**: [' + filename + '](' + url +')  '

    scopeText = '**Scope**: '
    for s in scope:
        scopeText = scopeText + s + ' '
    scopeText = scopeText + ' '
    print scopeText

    print '**Summary**: ' + summary + '  '
    print ''
    for line in snippet.split('\n'):
        print '    ' + line + '  '
    print ''

def printMarkdownHeader():
  print '''# Xcode Code Snippets

This is the collection of my user-defined code snippets for Xcode. Free feel to add them to your own collection.

## Install

* Clone, fork or [download](https://github.com/kirbyt/XcodeCodeSnippets/zipball/master) this collection of code snippets.
* Copy the code snippet files to: `~/Library/Developer/Xcode/UserData/CodeSnippets`

### Hint

To make life easier for me, I clone this repo to my CodeSnippets directory. This makes it easier for me to keep this repo up to date and simplifies sharing my code snippets across multiple machines. You can do the same, but I recommend forking this repo first so you can store your own code snippets along with the ones in this collection.

# Code Snippet Listing <a id="codesnippetlisting"></a>

Each code snippet shortcut is prefixed with **wps** to avoid conflict with other shortcuts. This also groups the code snippets in the Code Completion window.
'''


def printMarkdownFooter():
  print '''# More About Code Snippets

Learn more about using and creating your own Code Snippets from this article, [Be More Productive in Xcode Using Code Snippets](http://www.informit.com/articles/article.aspx?p=1914191).

# lscs.py Script

`lscs.py` is a python script that lists the code snippets for the current user. The listing shows the title, shortcut, and summary for each code snippet file.

    Example: python lscs.py

`lscs.py` is also used to create the list of code snippets shown above. You can do the same by using the `-f markdown` (or `--format=markdown`) command line parameter.

    Example: python lscs.py --f markdown

# Support, Bugs and Feature requests

There is absolutely no support offered for this collection of code snippets. You're on your own! However, free feel to send me a message or even a pull request if you have an interesting and useful code snippet to share.

# License

The MIT License

Copyright (c) 2012-2014 White Peak Software Inc

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.'''


def main():
    format = None
    opts, args = getopt.getopt(sys.argv[1:], 'f:', ['format='])
    for o, a in opts:
        if o in ('-f', '--format'):
            format = a

    if format == 'markdown':
      printMarkdownHeader()

    codeSnippets = [];

    path = os.path.expanduser('~/Library/Developer/Xcode/UserData/CodeSnippets')
    for dirname, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith('codesnippet'):
                from AppKit import NSDictionary
                snippetDict = NSDictionary.dictionaryWithContentsOfFile_(os.path.join(path, filename))
                # objDict = NSDictionary.dictionaryWithObjectsAndKeys_(filename,'filename',snippetDict,'snippet')
                codeSnippets.append({'filename':filename,'snippet':snippetDict});

    sortedCodeSnippets = sorted(codeSnippets, key=lambda k: k['snippet']['IDECodeSnippetTitle'].lower())
    for objDict in sortedCodeSnippets:
      filename = objDict['filename']
      dict = objDict['snippet']
      if format == 'markdown':
          showAsMarkdown(filename, dict)
      else:
          show(filename, dict)

    if format == 'markdown':
      printMarkdownFooter()

if __name__ == '__main__':
  sys.exit(main())
