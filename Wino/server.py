from werkzeug.wrappers import Request, Response
import os

@Request.application
def application(request):

    path = request.url
    print(path)

    html_file = open("index.html", "rb")
    html_content = html_file.read()

    css_file = open("static/style.css", "rb")
    css_content = css_file.read()

    image_file = open("static/wina.jpg", "rb")
    image_content = image_file.read()

    login_file = open("login.html", "rb")
    login_content = login_file.read()

    js_file = open("app.js", "rb")
    js_content = js_file.read()

    if "wino.jpg" in path:
        return Response(image_content, content_type="image/jpeg", status='200 OK')

    if "plain" in path:
        return Response(html_content, content_type="text/plain", status='200 OK')

    if "/login.html" in path:
        return Response(login_content, content_type="text/html", status='200 OK')

    if "/app.js" in path:
        return Response(js_content, content_type="application/javascript", status='200 OK')

    return Response(html_content, content_type="text/html", status='200 OK')

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    app = run_simple('0.0.0.0', 4444, application, static_files={'/static':'static'}).wsgi_app()
