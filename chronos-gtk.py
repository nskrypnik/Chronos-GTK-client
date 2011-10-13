import gtk 
import webkit
import os
import webbrowser

from settings import LOGIN, PASSWORD

try:
    from settings import CHRONOS_URL
except ImportError:
    CHRONOS_URL = "https://achille.proxistep.com/index.php?go=chronos_auth"

LAST_HOVERED_URI = None

def set_app_icon(win):
    path_to_icon = os.path.abspath(os.path.dirname(__file__))
    win.set_icon_from_file(os.path.join(path_to_icon, "icon.png"))

def hovering_over_link(view, title, uri):
    view.last_hovered_link = uri

def on_view_click(view, event):
    if event.button == 1 and view.last_hovered_link:
        webbrowser.open(view.last_hovered_link)

def on_chronos_page(view, frame):
    js = '''
            $(function(){
                    console.log('Hello world');
                    $('a').click(function(){
                    //console.log('Hello world!');
                    alert('Hello');
                });
            })
            '''
    view.execute_script(js)
    view.disconnect(view.load_connect_id)
    view.connect('hovering_over_link', hovering_over_link)
    view.connect('button-press-event', on_view_click);

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
