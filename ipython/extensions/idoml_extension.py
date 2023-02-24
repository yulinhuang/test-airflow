from IPython.display import Javascript, display
from idoml_magic import IdomlMagics

def _set_counts():
    display(Javascript(
        """
        require.undef('setCounts');
        define('setCounts', function() {
            return function(element) {
                var cell_element = element.parents('.cell');
                var index = Jupyter.notebook.get_cell_elements().index(cell_element);
                var cell = Jupyter.notebook.get_cell(index);
                if (cell.metadata.idoml_meta && cell.metadata.idoml_meta['task_id']) {                
                    var inputElement = cell_element[0].firstChild.firstChild.firstChild;
                    inputElement.innerHTML += '<br />[' + cell.metadata.idoml_meta['task_id'] + '] <br /> [' + cell.metadata.idoml_meta['task_type'] + ']<br />';
                }
            }
        });

        require(['setCounts'], function(setCounts) {
            setCounts(element);
        });
        """ 
    ))

class CountModifier(object):
    """
    A class that modifies the count of a cell in the notebook.
    """

    def __init__(self, ip):
        self.shell = ip
    
    def pre_execute(self):
        """
        Called before any code is run.
        """
        pass

    def pre_run_cell(self):
        """
        Called before each cell is run.
        """
        pass

    def post_execute(self):
        """
        Called after any code is run.
        """
        _set_counts()

    def post_run_cell(self, result):
        """
        Called when a cell is run.
        """
        _set_counts()

def load_ipython_extension(ipython):
    """
    Called when the extension is loaded.
    """
    cm = CountModifier(ipython)
    ipython.events.register('post_execute', cm.post_execute)
    ipython.register_magics(IdomlMagics)