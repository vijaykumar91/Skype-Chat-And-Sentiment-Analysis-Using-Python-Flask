####
# This script contains functions that demonstrate various
# aspects of the Tableau Server REST API. It also has a __main__
# section that executes when the script is run from the shell.
#
# To run the script, you must have installed Python 2.7.9 or later or
# Python 3.4.2 or later, plus the 'requests' library:
# http://docs.python-requests.org/en/latest/
#
# Note! You must set the variables SERVER, USER, and PASSWORD variables
# to the content URL and credentials for your installation of Tableau Server.
# Set the WORKBOOK_NAME variable to the name (and path) of a workbook to publish.
#     See the __main__ function at the bottom of this file. 
#
# This script works with the REST API version 2.3 that ships with Tableau Server 10.0. 
# The API version is hard-coded into requests.
####

####
# Changes for the 2.2 and 2.3 versions:
# * Updated the version in all requests.

# Changes for the 2.1 version:

# * Changed /2.0/ to /2.1/ in all requests.
# * Changed the namespace from "tableausoftware.com" to "tableau.com"
# * Added int() around math.ceiling when getting page numbers
# * Added ASCII encoding (the _encode_for_display function) around a lot of strings to fix a problem with displaying Unicode characters in the Windows command window.
# * Added an OR test to look for either 'default' or 'Default' as the name of the default project.
####

import math
# Contains methods used to build and parse XML
import xml.etree.ElementTree as ET
import requests  # Contains methods used to make HTTP requests
import sys

# The following packages are used to build a multi-part/mixed request.
# They are contained in the 'requests' library.
from requests.packages.urllib3.fields import RequestField
from requests.packages.urllib3.filepost import encode_multipart_formdata

# The code extracts values from the XML response by using
# ElementTree. This requires using a namespace when searching the XML.
# For details, see:
#      https://docs.python.org/3/library/xml.etree.elementtree.html has more details

# The namespace for the REST API is 'http://tableausoftware.com/api' for Tableau Server 9.0 or 'http://tableau.com/api' for Tableau Server 9.1 or later 
xmlns = {'t': 'http://tableau.com/api'}


####
# Functions for constructing HTTP multi-part requests and dealing with errors
####


def _make_multipart(parts):
    """
    Creates one "chunk" for a multi-part upload.

    'parts' is a dictionary that provides key-value pairs of the format name: (filename, body, content_type).

    Returns the post body and the content type string.

    For more information, see this post:
        http://stackoverflow.com/questions/26299889/how-to-post-multipart-list-of-json-xml-files-using-python-requests
    """

    mime_multipart_parts = []

    for name, (filename, blob, content_type) in parts.items():
        multipart_part = RequestField(name=name, data=blob, filename=filename)
        multipart_part.make_multipart(content_type=content_type)
        mime_multipart_parts.append(multipart_part)

    post_body, content_type = encode_multipart_formdata(mime_multipart_parts)
    content_type = ''.join(('multipart/mixed',) + content_type.partition(';')[1:])
    return post_body, content_type


def _handle_error(server_response):
    """
    Parses an error response for the error subcode and detail message
    and then displays them.

    Returns the error code and error message.
    """
    print("An error occurred")
    xml_response = ET.fromstring(_encode_for_display(server_response.text))
    error_code = xml_response.find('t:error', namespaces=xmlns).attrib.get('code')
    error_detail = xml_response.find('.//t:detail', namespaces=xmlns).text
    print("\tError code: " + str(error_code))
    print("\tError detail: " + str(error_detail))
    return error_code, error_detail


def _encode_for_display(text):
    """
    Encodes strings so they can display as ASCII in a Windows terminal window.
    This function also encodes strings for processing by xml.etree.ElementTree functions. 

    Returns an ASCII-encoded version of the text. Unicode characters are converted to ASCII placeholders (for example, "?").
    """
    return text.encode('ascii', errors="backslashreplace").decode('utf-8')


####
# Functions for authentication (sign in and sign out)
####


def sign_in(name, password, site=""):
    """
    Signs in to the server specified in the global SERVER variable.

    'name'     is the name (not ID) of the user to sign in as.
               Note that most of the functions in this example require that the user
               have server administrator permissions.
    'password' is the password for the user.
    'site'     is the ID (as a string) of the site on the server to sign in to. The
               default is "", which signs in to the default site.

    Returns the authentication token and the site ID.
    """
    url = SERVER + "/api/2.3/auth/signin"
    print(url)
    #sys.exit()
    # Builds the request
    xml_payload_for_request = ET.Element('tsRequest')
    credentials_element = ET.SubElement(xml_payload_for_request, 'credentials', name=name, password=password)
    site_element = ET.SubElement(credentials_element, 'site', contentUrl=site)
    xml_payload_for_request = ET.tostring(xml_payload_for_request)

    # Makes the request to Tableau Server
    server_response = requests.post(url, data=xml_payload_for_request)

    if server_response.status_code != 200:
        print(server_response.text)
        sys.exit(1)
    # Reads and parses the response
    xml_response = ET.fromstring(_encode_for_display(server_response.text))

    # Gets the token and site ID
    token = xml_response.find('t:credentials', namespaces=xmlns).attrib.get('token')
    site_id = xml_response.find('.//t:site', namespaces=xmlns).attrib.get('id')
    user_id = xml_response.find('.//t:user', namespaces=xmlns).attrib.get('id')
    return token, site_id, user_id


def sign_out():
    """
    Destroys the active session
    """
    global TOKEN
    url = SERVER + "/api/2.3/auth/signout"
    server_response = requests.post(url, headers={'x-tableau-auth': TOKEN})
    TOKEN = None
    return


####
# Functions for making queries to get information about content on the server
####

def query_projects():
    """
    Returns a list of projects on the site (a list of <project> elements).

    The function paginates over results (if required) using a page size of 100.
    """
    pageNum, pageSize = 1, 100
    url = SERVER + "/api/2.3/sites/{0}/projects".format(SITE_ID)
    paged_url = url + "?pageSize={}&pageNumber={}".format(pageSize, pageNum)

    server_response = requests.get(paged_url, headers={"x-tableau-auth": TOKEN})
    server_response.encoding = "utf-8";
    if server_response.status_code != 200:
        print(_encode_for_display(server_response.text))
        sys.exit(1)
    xml_response = ET.fromstring(_encode_for_display(server_response.text))

    total_count_of_projects = int(xml_response.find('t:pagination', namespaces=xmlns).attrib.get('totalAvailable'))

    if total_count_of_projects > pageSize:
        projects = []
        projects.extend(xml_response.findall('.//t:project', namespaces=xmlns))
        number_of_pages = int(math.ceil(total_count_of_projects / pageSize))

        # Starts from page 2 because page 1 has already been returned
        for page in range(2, number_of_pages + 1):
            paged_url = url + "?pageSize={}&pageNumber={}".format(pageSize, page)
            server_response = requests.get(paged_url, headers={"x-tableau-auth": TOKEN})
            if server_response.status_code != 200:
                print(_encode_for_display(server_response.text))
                sys.exit(1)
            projects_from_page = ET.fromstring(_encode_for_display(server_response.text)).findall('.//t:project',
                                                                                                  namespaces=xmlns)
            projects.extend(projects_from_page)
    else:
        projects = xml_response.findall('.//t:project', namespaces=xmlns)
    return projects


def query_users():
    """
    Returns a list of users on the site (a list of <user> elements).

    The function paginates over the results (if required) using a page size of 100.
    """
    pageNum, pageSize = 1, 100
    url = SERVER + "/api/2.3/sites/{0}/users".format(SITE_ID)
    paged_url = url + "?pageSize={}&pageNumber={}".format(pageSize, pageNum)
    server_response = requests.get(paged_url, headers={"x-tableau-auth": TOKEN})
    if server_response.status_code != 200:
        print(_encode_for_display(server_response.text))
        sys.exit(1)
    xml_response = ET.fromstring(_encode_for_display(server_response.text))
    total_count_of_users = int(xml_response.find('t:pagination', namespaces=xmlns).attrib.get('totalAvailable'))
    if total_count_of_users > pageSize:
        users = []  # A list to hold the users returned from the server
        users.extend(xml_response.findall('.//t:user', namespaces=xmlns))
        number_of_pages = int(math.ceil(total_count_of_users / pageSize))
        # Starts from page 2 because page 1 has already been returned
        for page in range(2, number_of_pages + 1):
            paged_url = url + "?pageSize={}&pageNumber={}".format(pageSize, page)
            server_response = requests.get(paged_url, headers={"x-tableau-auth": TOKEN})
            if server_response.status_code != 200:
                print(_encode_for_display(server_response.text))
                sys.exit(1)
            users_from_page = ET.fromstring(_encode_for_display(server_response.text)).findall('.//t:user',
                                                                                               namespaces=xmlns)
            # Adds the new page of users to the list
            users.extend(users_from_page)
    else:
        users = xml_response.findall('.//t:user', namespaces=xmlns)
    return users


def query_groups():
    """
    Returns a list of groups on the site (a list of <group> elements).

    The function paginates over the results (if required) using a page size of 100.
    """
    pageNum, pageSize = 1, 100
    url = SERVER + "/api/2.3/sites/{0}/groups".format(SITE_ID)
    paged_url = url + "?pageSize={}&pageNumber={}".format(pageSize, pageNum)
    server_response = requests.get(paged_url, headers={"x-tableau-auth": TOKEN})
    if server_response.status_code != 200:
        print(_encode_for_display(server_response.text))
        sys.exit(1)
    xml_response = ET.fromstring(_encode_for_display(server_response.text))
    total_count_of_groups = int(xml_response.find('t:pagination', namespaces=xmlns).attrib.get('totalAvailable'))
    if total_count_of_groups > pageSize:
        groups = []  # A list to hold the groups returned from the server
        groups.extend(xml_response.findall('.//t:group', namespaces=xmlns))
        number_of_pages = int(math.ceil(total_count_of_groups / pageSize))
        # Starts from page 2 because page 1 has already been returned
        for page in range(2, number_of_pages + 1):
            paged_url = url + "?pageSize={}&pageNumber={}".format(pageSize, page)
            server_response = requests.get(paged_url, headers={"x-tableau-auth": TOKEN})
            if server_response.status_code != 200:
                print(_encode_for_display(server_response.text))
                sys.exit(1)
            groups_from_page = ET.fromstring(_encode_for_display(server_response.text)).findall('.//t:group',
                                                                                                namespaces=xmlns)
            # Adds the new page of groups to the list
            groups.extend(groups_from_page)
    else:
        groups = xml_response.findall('.//t:group', namespaces=xmlns)
    return groups


def query_workbooks(user_id):
    """
    Returns a list of workbooks that the current user has permission to read (a list of <workbook> elements).

    'user_id' is the LUID (as a string) of the user to get workbooks for.

    The function paginates over the results (if required) using a page size of 100.
    """
    pageNum, pageSize = 1, 100
    url = SERVER + "/api/2.3/sites/{0}/users/{1}/workbooks".format(SITE_ID, user_id)
    paged_url = url + "?pageSize={0}&pageNumber={1}".format(pageSize, pageNum)
    server_response = requests.get(paged_url, headers={"x-tableau-auth": TOKEN})
    if server_response.status_code != 200:
        print(_encode_for_display(server_response.text.encode))
        sys.exit(1)
    xml_response = ET.fromstring(_encode_for_display(server_response.text))
    total_count_of_workbooks = int(xml_response.find('t:pagination', namespaces=xmlns).attrib.get('totalAvailable'))
    if total_count_of_workbooks > pageSize:
        workbooks = []  # This list wil hold the users returned from Server
        workbooks.extend(xml_response.findall('.//t:workbook', namespaces=xmlns))
        number_of_pages = int(math.ceil(total_count_of_workbooks / pageSize))
        # Starts from page 2 since page 1 has already been returned
        for page in range(2, number_of_pages + 1):
            paged_url = url + "?pageSize={}&pageNumber={}".format(pageSize, page)
            server_response = requests.get(paged_url, headers={"x-tableau-auth": TOKEN})
            if server_response.status_code != 200:
                print(_encode_for_display(server_response.text))
                sys.exit(1)
            workbooks_from_page = ET.fromstring(_encode_for_display(server_response.text)).findall('.//t:workbook',
                                                                                                   namespaces=xmlns)
            # Adds the new page of workbooks to the list
            workbooks.extend(workbooks_from_page)
    else:
        workbooks = xml_response.findall('.//t:workbook', namespaces=xmlns)
    return workbooks


####
# Functions for publishing a workbook
####

def start_upload_session():
    """
    Creates a POST request that initiates a file upload session.

    Returns a session ID that is used by subsequent functions to identify the upload session.
    """
    url = SERVER + "/api/2.3/sites/{0}/fileUploads".format(SITE_ID)
    server_response = requests.post(url, headers={"x-tableau-auth": TOKEN})
    if server_response.status_code != 201:
        print(_encode_for_display(server_response.text))
        sys.exit(1)
    xml_response = ET.fromstring(_encode_for_display(server_response.text))
    uploadSessionId = xml_response.find('t:fileUpload', namespaces=xmlns).attrib.get('uploadSessionId')
    return uploadSessionId


def _read_in_chunks(file_name, chunk_size=None):
    """
    Reads a file piece by piece.

    'file_name'  is the name of the file to read.
    'chunk_size' is the amount of the file (in bytes) to read at once. If no
                 value is provided, the function reads 4K chunks.
    """
    if chunk_size is None:
        chunk_size = 4096
    with open(file_name, 'rb') as file_object:
        while True:
            data = file_object.read(chunk_size)
            if not data:
                break
            yield data


def put_chunk(chunk, session):
    """
    Makes a PUT request to upload a "chunk" of a file.

    'chunk'    is the portion of the file to publish.
    'session'  is the file upload session (returned from start_upload_session()).

    The request payload is empty in API v2.0, so an empty bytestring is generated in this function.
    """
    url = SERVER + "/api/2.3/sites/{0}/fileUploads/{1}".format(SITE_ID, session)
    payload, content_type = _make_multipart({'request_payload': ('', b'', 'text/xml'),
                                             'tableau_file': ('file', chunk, 'application/octet-stream')})

    print('\tPublishing a chunk ...')
    server_response = requests.put(url, data=payload, headers={"x-tableau-auth": TOKEN, "content-type": content_type})


def publish_with_chunk(fn, name, project_id):
    """
    Publishes a file to Tableau Server in chunks.

    'fn'         is the name of the file to publish.
    'name'       is the workbook name as a string.
    'project_id' is the ID (as a string) of the project to publish to.

    Returns a list of <workbook> elements.
    """
    # Initiates an upload session
    uploadID = start_upload_session()
    # Reads the source file in chunks (default is 100KB)
    chunks = _read_in_chunks(fn, 102400)
    # Loops through the chunks, builds a request payload, and makes a PUT request
    # The information should NOT be encoded (e.g. base-64 or UTF-8)
    for chunk in chunks:
        put_chunk(chunk, uploadID)

    # Builds a request for publishing
    xml_payload_for_request = ET.Element('tsRequest')
    workbook_element = ET.SubElement(xml_payload_for_request, 'workbook', name=name)
    p = ET.SubElement(workbook_element, 'project', id=project_id)
    xml_payload_for_request = ET.tostring(xml_payload_for_request)
    payload, content_type = _make_multipart({'request_payload': ('', xml_payload_for_request, 'text/xml')})

    url = SERVER + "/api/2.3/sites/{0}/workbooks".format(SITE_ID)
    url += "?uploadSessionId={}".format(uploadID)
    url += "&workbookType={}".format(fn.split('.')[1])  # Get extension
    url += "&overwrite=true"

    server_response = requests.post(url, data=payload, headers={'x-tableau-auth': TOKEN, 'content-type': content_type})
    if server_response.status_code != 201:
        print(_encode_for_display(server_response.text))
        sys.exit(1)
    xml_response = ET.fromstring(_encode_for_display(server_response.text))
    return xml_response.find('t:workbook', namespaces=xmlns)


def publish_simple(fn, name, project_id):
    """
    Publishes a file to Tableau Server in a single request.

    'fn'         is the name of the file to publish.
    'name'       is the workbook name as a string.
    'project_id' is the ID (as a string) of the project to publish to.

    Returns a list of <workbook> elements.
    """
    with open(fn, 'rb') as f:
        workbook_bytes = f.read()

    # Builds the publish request
    xml_payload_for_request = ET.Element('tsRequest')
    workbook_element = ET.SubElement(xml_payload_for_request, 'workbook', name=name)
    p = ET.SubElement(workbook_element, 'project', id=project_id)
    xml_payload_for_request = ET.tostring(xml_payload_for_request)

    payload, content_type = _make_multipart(
        {'request_payload': ('', xml_payload_for_request, 'text/xml'),
         'tableau_workbook': (fn, workbook_bytes, 'application/octet-stream')})

    url = SERVER + "/api/2.3/sites/{0}/workbooks".format(SITE_ID)
    url += "?workbookType={}".format(fn.split('.')[1])  # Get extension
    url += "&overwrite=true"
    server_response = requests.post(url, data=payload, headers={'x-tableau-auth': TOKEN, 'content-type': content_type})
    if server_response.status_code != 201:
        print(_encode_for_displayserver_response.text)
        sys.exit(1)
    xml_response = ET.fromstring(_encode_for_display(server_response.text))
    return xml_response.find('t:workbook', namespaces=xmlns)


####
# Functions for setting permissions
####


def create_group(name):
    """
    Creates a group on Tableau Server (local, not Active Directory).
    If the group already exists, the function finds the ID of the
    specified group.

    Note: This function illustrates how to check for error codes
    in the response. The pattern shown here can be used in other
    functions.

    'name'  is the name of the group tp create.

    Returns a <group> element with information about the specified group.
    """
    url = SERVER + "/api/2.3/sites/{0}/groups".format(SITE_ID)
    xml_payload_for_request = ET.Element('tsRequest')
    group = ET.SubElement(xml_payload_for_request, 'group', name=name)
    xml_payload_for_request = ET.tostring(xml_payload_for_request)
    server_response = requests.post(url, data=xml_payload_for_request, headers={'x-tableau-auth': TOKEN})

    # Checks HTTP status code. If the code is anything _except_ success (here, 201),
    # the code reads the <error> block from the response. The error code
    # in the block indicates the specific issue. The documentation for each method
    # provides a list of error codes that might be returned for that method.
    if server_response.status_code != 201:
        error, detail = _handle_error(server_response)
        # 409009 is the error code when the group already exists.
        if error == "409009":
            # A group with the specified name already exists. Therefore, gets a list
            # of existing groups and finds the ID of the group with the specified name.
            groups = query_groups()
            for group in groups:
                if group.get('name') == name:
                    return group
            else:
                print(detail)
                sys.exit(1)  # Exit the program altogether
    xml_response = ET.fromstring(_encode_for_display(server_response.text))
    return xml_response.find('t:group', namespaces=xmlns)


def set_group_permissions_for_workbook(workbook_id, group_id, permissions_map):
    """
    Adds a set of permissions for a single group on a single workbook

    'workbook_id'      is the ID (as a string) of the workbook to set permissions on.
    'group_id'         is the ID (as a string) of the group to give permissions to.
    'permissions_map'  is a dictionary that provides key-value pairs of the
                       format "permissionName: Allow/Deny ".

    Returns the <granteeCapabilities> element from the response.
    """
    url = SERVER + "/api/2.3/sites/{0}/workbooks/{1}/permissions".format(SITE_ID, workbook_id)
    xml_payload_for_request = ET.Element('tsRequest')
    permissions = ET.SubElement(xml_payload_for_request, 'permissions')
    granteeCapabilities = ET.SubElement(permissions, 'granteeCapabilities')
    user_xml = ET.SubElement(granteeCapabilities, 'group', id=group_id)
    capabilities = ET.SubElement(granteeCapabilities, 'capabilities')
    for perm, mode in permissions_map.items():
        capabilities.append(ET.Element('capability', name=perm, mode=mode))
    xml_payload_for_request = ET.tostring(xml_payload_for_request)
    server_response = requests.put(url, data=xml_payload_for_request, headers={'x-tableau-auth': TOKEN})
    if server_response.status_code != 200:
        print(_encode_for_displayserver_response.text)
        sys.exit(1)
    xml_response = ET.fromstring(_encode_for_display(server_response.text))
    return xml_response.findall('.//t:granteeCapabilities', namespaces=xmlns)


####
# Main function. This executes when the script is run from a shell
####


if __name__ == '__main__':
    ####
    # Global variables -- SET THESE BEFORE RUNNING
    ####
    SERVER = "https://us-east-1.online.tableau.com/#/site/loginworks/workbooks"  # Set to the server URL without a trailing slash (/).
    USER = 'vijay.kumar@loginworks.com'  # Set to your Tableau Server username. The user must be a server administrator.
    PASSWORD = 'Vijayloginworks3'  # Set to your Tableau Server password.
    WORKBOOK_NAME = 'test_bookhook.twbx'  # Set to the name of the workbook to publish. Include a path if necessary.
    CHUNKED = True  # Set to False to publish the workbook in one request. (The workbook must be less than 64MB.)

    ####
    # These calls will perform the following tasks:
    # 1. Sign in to Tableau Server
    # 2. Get a list of all projects on the server
    # 3. Loop through the results and find the project named 'Default'
    # 4. Get a list of all users on the server
    # 5. Create a group
    # 6. Publish a workbook
    # 7. Get a list of all workbooks on the server for the current user
    # 8. Loop through the list of workbooks and display their names
    # 9. Set permissions on the published workbook
    ####

    # Signs in to get an authentication token and site ID to use later
    print("Signing in")
    TOKEN, SITE_ID, MY_USER_ID = sign_in(USER, PASSWORD)

    # Lists all projects on the server
    print("Getting a list of all projects on the server for the Default site:")
    for project in query_projects():
        print('\t{} (id: {})'.format(project.get('name'), project.get('id')))

    # Gets a list of projects
    list_of_projects = list(query_projects())
    # Loops through the list of projects and looks for the project named 'default', then
    # gets its ID. The ID is used later when publishing.
    print("\nFinding the 'default' project")
    for project in list_of_projects:
        if project.get('name') == 'default' or project.get('name') == 'Default':
            default_project_id = project.get('id')

    # Creates a group
    print('\nCreating a group')
    new_group = create_group('TableauExample')
    new_group_id = new_group.get('id')
    print('\tID of the new or existing group: {} '.format(new_group_id))

    # Publishes the workbook. The boolean value of the global variable CHUNKED
    # determines whether the publish process is simple (one request) or chunked
    if CHUNKED:
        # Publishes a workbook in chunks
        # The publish_with_chunk method returns a <workbook> element that can
        # be used in later calls
        print(
            "\nPublishing the workbook '{0}' to the server as 'PublishedWithRestAPIWorkBook' using the chunked method ...".format(
                WORKBOOK_NAME))
        new_workbook = publish_with_chunk(WORKBOOK_NAME, 'PublishedWithRestAPIWorkBook', default_project_id)
    else:
        # Publishes a workbook in one request
        print(
            "Publishing the workbook '{0}' to the server as 'PublishedWithRestAPIWorkBook' using the all-in-one method ...".format(
                WORKBOOK_NAME))
        new_workbook = publish_simple(WORKBOOK_NAME, 'PublishedWithRestAPIWorkBook', default_project_id)

    # Gets the ID of the published workbook
    new_workbook_id = new_workbook.get('id')

    # Gets all workbooks for the current user
    print("\nGetting all workbooks on the server for the current user:")
    for workbook in query_workbooks(MY_USER_ID):
        # Includes decoding to handle Unicode characters in workbook names
        print('\t' + _encode_for_display(workbook.get('name')))

    # Sets explicit permissions on the published workbook for the group created earlier
    # Creates a dictionary (mapping) of permissions to set
    permissions = {
        "Write": "Deny",
        "Read": "Deny",
        "ViewUnderlyingData": "Deny",
    }
    # Calls a function that uses the map to set the workbook permissions for the group
    print("\nSetting permissions on the workbook '{0}'".format(WORKBOOK_NAME))
    set_group_permissions_for_workbook(new_workbook_id, new_group_id, permissions)

    # Signs out (destroys the current session)
    sign_out()
    print("\nSigned out, and the authentication token has been invalidated")
