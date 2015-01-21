#coding: utf-8

# pep333 application middleware server

from wsgiref.simple_server import make_server
from cgi import parse_qs, escape

html = """
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>%s</title>
</head>
<body>
    <form method="post" action="main.py">
    <!-- if can't find newmain.py ,the server will use the orignal script to handle the get, ie main.py . There are still something strange: the url
    no strange things , it just need to rerun the main.py script, we need a tool to auto-rerun scripts.
    
    -->

    <p>Age: <input type="text" name="age"></p>
    <p>
    Languages:<br>
    <input type="checkbox" name="language" value="scheme">Scheme
    <br/>
    <input type="checkbox" name="language" value="ruby">Ruby
    </p>
    <p>
    <input type="submit" value="Submit">
    </p>
    
    </form>
    <p>Age: %s<br>Languages: %s</p>
	
</body>
</html>
"""
# environ points to a dictionary containing CGI like environment which is filled by The SERVER for each received request from client
# start_response is a callback function supplied by the server
# which will be used to send the HTTP status and headers to the server

# application level
def application(environ, start_response):

# GET method
    query_string = parse_qs(environ['QUERY_STRING'])
    print query_string, "GET method"
# age=10&hobbies=software&hobbies=tunning

# It is possible to write code to parse the query string and retrieve those values but it is easier to use the CGI module's parse_qs function which returns a dictionary with the values as lists.
    age = query_string.get('age',[''])[0]
    languages = query_string.get('language',[])

    age = escape(age)
    languages =  [escape(language) for language in languages]

# POST method
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH',0))
    except (ValueError):
        request_body_size = 0

    request_body = environ['wsgi.input'].read(request_body_size)
    query_string = parse_qs(request_body)
    print query_string, "POST method"

    age = escape(query_string.get('age', [''])[0])
    languages = query_string.get('language',[])
    language = [escape(language) for language in languages]

    
    #response_body = "The request method was %s" % environ['REQUEST_METHOD']
# generate webpage
    response_body = html % ("Make out a new title", age or 'Empty',', '.join(languages or ['No Languages']))

    #response_body = ['%s: %s' % (key, value) for key, value in sorted(environ.items())]
    response_body = ''.join(response_body)
# response_body is a string

    #response_body = ['The Beggining\n', '*'*30+'\n',response_body, '\n'+ '*'*30,'\nThe End']
# response_body is a list. list is fastter than string

    content_length = 0
    for s in response_body:
        content_length += len(s)

    status = '200 OK'

# HTTP headers [(Headers name, Header value)]
#    response_headers = [('Content-Type', 'text/plain'), ('Content-Length', str(len(response_body)))]
    response_headers = [('Content-Type', 'text/html'), ('Content-Length', str(content_length))]

    start_response(status, response_headers)

    # return [response_body]
    return response_body # a list


# server level
httpd = make_server('localhost',
        8090,
        application
        )
print('running on localhost:8090')
#httpd.handle_request() # run once
httpd.serve_forever()

# sources
# http://webpython.codepoint.net/wsgi_request_parsing_get
# http://anandology.com/blog/how-to-write-a-web-framework-in-python/
# https://www.python.org/dev/peps/pep-0333/
# https://www.python.org/dev/peps/pep-3333/ for Python3
