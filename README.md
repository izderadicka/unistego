unistego is python library which helps to hide secret message in text using special unicode characters. 

Usage
-----
Library is written in python 3 , but it's backward compatible with python 2.7 (using six library).

For python 2 it's important to use io package  to get streams that alraeady supports unicode reading/writing.

Unistego provides stream like objects, that can be used to hide and unhide data into unicode text.

*quick sample*
to hide message:
```python
#python 3 example
import unistego
secret_message="Nobody will see me"
carrier_text=open('innocent-text.txt', 'rt')
hider=unistego.get_hider(open('text-with-hidden-msg.txt', 'wt'), secret_message, 'joiners')
with carrier_text, hider:
	hider.write(carrier_text.read())
```

to read hidden message:
```python
import unistego
unhider=unistego.get_uhider(open('text-with-hidden-msg.txt', 'rt'), 'joiners')
with unhider:
	unhider.read()
print(unhider.get_message().decode('utf-8')
```

Unistego also supports html (where html is parsed and message in hidden in text not in markup) - 
usage is same as above, just use `unistego.get_hider_html` and `unistego.get_unhider_html`.

Package also contains a command line tool unistego-tool:
```shell
unistego-tool --hide -o text-with-hidden-msg.txt -m "Nobody will see me" --preset joiners innocent-text.txt
unistego-tool --unhide --preset joiners text-with-hidden-msg.txt
```

More information on [unistego page on my web](http://zderadicka.eu).

Install
-------

pip install [-e] git+https://github.com/izderadicka/unistego#egg=unistego



License
-------
[GPL v3](http://www.gnu.org/licenses/gpl.html) 


Versions:
---------
0.1.0 -  Initial version - supports two strategies (joiners, spaces) with optional zlib compression, html support and commnand line tool unistego-tool.
