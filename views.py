import os
import stat

from elementtree import ElementTree

from django.http import HttpResponse

BASE_PATH = '/var/www/django-media'
BASE_URL = '/django-media'

def actual_path(base_path, file_type, path):

    if path == '/':
        path = ''
        
    actual = os.path.normpath('%s/%s/%s' % (base_path, file_type, path))

    # make sure we start and end with a slash
    if actual[0] != '/':
        actual = '/' + actual

    if actual[-1] != '/':
        actual = actual + '/'

    return actual
    
def browser(request):

    global BASE_PATH
    
    # extract the command, type and folder path
    command_name = request.REQUEST.get('Command', None)
    resource_type = request.REQUEST.get('Type', None)
    folder_path = request.REQUEST.get('CurrentFolder', None)

    #if None in (command_name, resource_type, folder_path):
    #    return 

    err_no = 0
    err_txt = 'Successful'
    
    xml_response = ElementTree.ElementTree(
        ElementTree.Element("Connector", {'command':command_name,
                                          'resourceType':resource_type})
        )
    
    if None in (command_name, resource_type, folder_path):
        err_no = 1
        err_txt = 'Incomplete command.'
    else:
        # construct the response
        # append current folder information
        abs_path =  actual_path(BASE_PATH, resource_type, folder_path)
        abs_url  =  actual_path(BASE_URL,  resource_type, folder_path)

        xml_response.getroot().append(
            ElementTree.Element("CurrentFolder",
                                {'path':folder_path,
                                 'url': abs_url,
                                 })
            )

        if (command_name == 'GetFolders'):
            # append Folder list
            folders = ElementTree.Element("Folders")

            for f in os.listdir(abs_path):
                if os.path.isdir(f):
                    folders.append(ElementTree.Element("Folder",
                                                       {'name' : f}))

            xml_response.getroot().append(folders)

        elif (command_name == 'GetFoldersAndFiles'):
            # append Folder and list
            folders = ElementTree.Element("Folders")
            files = ElementTree.Element("Files")
            
            for f in os.listdir(abs_path):
                if os.path.isdir(os.path.join(abs_path, f)):
                    folders.append(ElementTree.Element("Folder",
                                                       {'name' : f}))
                else:
                    size = os.lstat(os.path.join(abs_path, f))[stat.ST_SIZE]
                    size = str(size / 1024)
                    
                    files.append(ElementTree.Element("File",
                                                     {'name' : f,
                                                      'size': size}
                                                     )
                                 )

            xml_response.getroot().append(folders)
            xml_response.getroot().append(files)

        elif (command_name == 'CreateFolder'):
            new_folder_name = request.REQUEST.get('NewFolderName', None)

            if new_folder_name is None:
                err_no = 102
                err_txt = 'Invalid folder name.'
            else:

                try:
                    os.mkdir(os.path.join(abs_path, new_folder_name))
                except Exception, e:
                    err_no = 110
                    err_txt = str(e)
            
        elif (command_name == 'FileUpload'):

            new_file = request.FILES.get('NewFile', None)
            if new_file is None:
                status = "202"
            else:
                # determine the destination file name
                file_name = new_file['filename']
                base, ext = os.path.splitext(new_file['filename'])
                count = 1
                
                while (os.path.exists(os.path.join(abs_path, file_name))):
                    file_name = '%s(%s)%s' % (base, count, ext)
                    count += 1
                    
                # write the file
                target = file(os.path.join(abs_path, file_name), 'wb')
                target.write(new_file['content'])
                target.close()

                # set the status
                if file_name == new_file['filename']:
                    status = "0"
                else:
                    status = "201, '%s'" % file_name
            
            return HttpResponse(
                """<script type="text/javascript">
                window.parent.frames['frmUpload'].OnUploadCompleted(%s)
                </script>""" % status)

        else:
            # unknown command
            xml_response.getroot().append(
                ElementTree.Element("Error", {'number':1, 'text':'blarf'})
                )
            
    xml_response.getroot().append(
        ElementTree.Element("Error", {'number':str(err_no), 'text':err_txt})
        )

    response = HttpResponse(ElementTree.tostring(xml_response.getroot(),
                                                 'utf-8'),
                            mimetype='text/xml')
    response['Cache-Control'] = 'no-cache'
    
    return response

def uploader(request):
    pass
