@app.route('/files', methods = ['GET'])
def config():
    if 'username' in session :
        path = os.path.expanduser(u'~/path/to/log/')
        return render_template('files.html', tree=make_tree(path))
    else:
        return redirect(url_for('login'))

def make_tree(path):
    tree = dict(name=os.path.basename(path), children=[])
    try: lst = os.listdir(path)
    except OSError:
        pass #ignore errors
    else:
        for name in lst:
            fn = os.path.join(path, name)
            if os.path.isdir(fn):
                tree['children'].append(make_tree(fn))
            else:
                with open(fn) as f:
                    contents = f.read()
                tree['children'].append(dict(name=name, contents=contents))
    return tree
