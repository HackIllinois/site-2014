import MainHandler
import logging
import jinja2
from google.appengine.api import users

# https://webapp-improved.appspot.com/guide/exceptions.html#guide-exceptions

def render(response, template, **kw):
	t = MainHandler.jinja_env.get_template(template)
	page = t.render(**kw)
	response.out.write(page)

def handle_401(request, response, exception):
	# Unauthorized
	logging.exception(exception)
	user = users.get_current_user()
	if not user:
		render( response, "simple_message.html", showSocial=False, header="ACCESS DENIED",
				message="You are not an admin or are not logged in as such.<br>Please log in with a valid @hackillinois.org email address.<br><a class='logout-link' href='%s'>Login</a>" % users.create_login_url('/') )	
	else:
		render( response, "simple_message.html", showSocial=False, header="ACCESS DENIED",
				message="You (%s) are not an admin or are not logged in as such.<br>Please log in with a valid @hackillinois.org email address.<br><a class='logout-link' href='%s'>Logout</a>" % (user.nickname(), users.create_logout_url('/')) )
	response.set_status(401)

def handle_404(request, response, exception):
	# Not Found
	logging.exception(exception)
	render( response, "simple_message.html", showSocial=False, header="PAGE NOT FOUND", message="" )
	response.set_status(404)

def handle_500(request, response, exception):
	# Internal Server Error
	logging.exception(exception)
	render( response, "simple_message.html", showSocial=False, header="A server error occurred!", message="" )
	response.set_status(500)

class Error401Handler(MainHandler.Handler):
	def get(self):
		return self.abort(401)
		
class Error404Handler(MainHandler.Handler):
	def get(self):
		return self.abort(404)
		
class Error500Handler(MainHandler.Handler):
	def get(self):
		return self.abort(500)
