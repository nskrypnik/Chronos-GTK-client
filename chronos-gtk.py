import gtk 
import webkit

from settings import LOGIN, PASSWORD

view = webkit.WebView() 
sw = gtk.ScrolledWindow() 
sw.add(view) 

win = gtk.Window(gtk.WINDOW_TOPLEVEL) 
win.add(sw)
win.set_default_size(600, 800)
win.show_all()
win.connect('destroy', gtk.main_quit)

view.open("https://achille.proxistep.com/index.php?go=chronos_auth")

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
    print 'Iam on chronos page'
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
view.connect('load-finished', on_html_get)

gtk.main()

