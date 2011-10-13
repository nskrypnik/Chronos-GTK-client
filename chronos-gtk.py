import gtk 
import webkit
import os

from settings import LOGIN, PASSWORD

try:
    from settings import CHRONOS_URL
except ImportError:
    CHRONOS_URL = "https://achille.proxistep.com/index.php?go=chronos_auth"

def set_app_icon(win):
    path_to_icon = os.path.abspath(os.path.dirname(__file__))
    win.set_icon_from_file(os.path.join(path_to_icon, "icon.png"))

def handle_console_message(view, message, line):
    print message

def on_chronos_page(view, frame):
    js = '''
            $(function(){
                
                    $('a').click(function(){
                    //console.log('Hello world!');
                    alert('Hello');
                });
            })
            '''
    view.execute_script(js)
    view.disconnect(view.load_connect_id)
    view.connect('console-message', handle_console_message)

def on_html_get(view, frame):
    js = '''
        $('input[name="login_name"]').val('%s');
        $('input[name="login_password"]').val('%s')
        $('form[name="my_form"]').submit();
    ''' % (LOGIN, PASSWORD)
    view.execute_script(js)
    view.load_connect_id = view.connect('load_finished', on_chronos_page)
    #

if __name__ == '__main__':
    view = webkit.WebView() 
    sw = gtk.ScrolledWindow() 
    sw.add(view) 

    win = gtk.Window(gtk.WINDOW_TOPLEVEL) 
    win.add(sw)
    win.set_default_size(600, 800)
    win.show_all()
    win.connect('destroy', gtk.main_quit)

    set_app_icon(win)

    view.open(CHRONOS_URL)
    view.connect('load-finished', on_html_get)
    
    gtk.main()
