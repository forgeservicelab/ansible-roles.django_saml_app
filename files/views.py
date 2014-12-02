from django.http import HttpResponse
import datetime

_response = """
<html>
<body>
<p>
This is a testing SAML Django App. It was set up with the Ansible role at <a href=https://git.forgeservicelab.fi/groups/ansible-roles/django_saml_app>https://git.forgeservicelab.fi/groups/ansible-roles/django_saml_app</a>

<p>
To see local metadata, visit <a href=/saml2/metadata>/saml2/metadata</a>.
</p>


<p>
To test SAML login, visit <a href=/test>/test</a>.
</p>

</body>
</html>

"""


def index(request):
    return HttpResponse(_response)
