from IPython.core.magic import register_line_magic, register_line_cell_magic
from IPython.core.magic import (Magics, magics_class, line_magic,
                                cell_magic, line_cell_magic)
from IPython.utils.capture import capture_output
from IPython.display import Javascript, display
import json
import time

def _set_tags(tags):
    assert all(map(lambda t: isinstance(t, str), tags))
    display(Javascript(
        """
        define('setTags', function() {
            return function(element, tags) {
                var cell_element = element.parents('.cell');
                var index = Jupyter.notebook.get_cell_elements().index(cell_element);
                var cell = Jupyter.notebook.get_cell(index);
                cell.metadata.tags = tags;
            }
        });

        require(['setTags'], function(setTags) {
            setTags(element, %s);
        });
        """ % json.dumps(tags)
    ))

def _idoml_update_meta(key, value):
    display(Javascript(
        """
        require.undef('updateIdomlMeta');
        define('updateIdomlMeta', function() {
            return function(element, key, value) {
                var cell_element = element.parents('.cell');
                var index = Jupyter.notebook.get_cell_elements().index(cell_element);
                var cell = Jupyter.notebook.get_cell(index);
                if (!cell.metadata.idoml_meta) {
                    cell.metadata.idoml_meta = new Object();
                } 

                cell.metadata.idoml_meta[key] = value;
            }
        });

        require(['updateIdomlMeta'], function(updateIdomlMeta) {
            updateIdomlMeta(element, '%(key)s', '%(value)s');
        });
        """ % {'key': key, 'value': value}
    ))

def _idoml_update_meta_upstrings(upstrings):
    assert all(map(lambda t: isinstance(t, str), upstrings))
    display(Javascript(
        """
        require.undef('updateIdomlMeta');
        define('updateIdomlMeta', function() {
            return function(element, upstrings) {
                var cell_element = element.parents('.cell');
                var index = Jupyter.notebook.get_cell_elements().index(cell_element);
                var cell = Jupyter.notebook.get_cell(index);
                if (!cell.metadata.idoml_meta) {
                    cell.metadata.idoml_meta = new Object();
                } 
                cell.metadata.idoml_meta['upstrings'] = upstrings;
            }
        });

        require(['updateIdomlMeta'], function(updateIdomlMeta) {
            updateIdomlMeta(element, %s);
        });
        """ % json.dumps(upstrings)
    ))

# The class MUST call this class decorator at creation time
@magics_class
class IdomlMagics(Magics):

    @line_magic
    def task_id(self, line):
        _idoml_update_meta('task_id', line)
        time.sleep(0.01)
        # self.shell.run_cell(cell)
    
    @line_magic
    def task_type(self, line):
        _idoml_update_meta('task_type', line)
        time.sleep(0.01)
        # self.shell.run_cell(cell)
    
    @line_magic
    def upstreams(self, line):
        if line:
            time.sleep(0.01)
            _idoml_update_meta_upstrings(line.split())
        # self.shell.run_cell(cell)
    
    @line_cell_magic
    def tag(self, line, cell=None):
        print(line)
        _set_tags(line.split())

def load_ipython_extension(ipython):
    @register_line_magic("reverse")
    def lmagic(line):
        "Line magic that reverses any string that is passed"
        return line[::-1]   

    ipython.register_magics(IdomlMagics)



