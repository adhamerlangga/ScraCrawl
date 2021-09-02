import os
from urllib.parse import urlparse

from scrapy.pipelines.files import FilesPipeline

class MyFilesPipeline(FilesPipeline):

    # def file_path(self, request, response=None, info=None):
    #     url = request.url
    #     url_array = url.split('/')
    #     file_name = url_array[len(url_array)-1]
    #     return 'full/'+file_name

    def file_path(self, request, response=None, info=None):
        return 'files/' + os.path.basename(urlparse(request.url).path)

    # # error karena banyak library yang g ada.
    # def file_path(self, request, response=None, info=None):
    #     media_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
    #     media_ext = os.path.splitext(request.url)[1]
    #     # Handles empty and wild extensions by trying to guess the
    #     # mime type then extension or default to empty string otherwise
    #     if media_ext not in mimetypes.types_map:
    #         media_ext = ''
    #         media_type = mimetypes.guess_type(request.url)[0]
    #         if media_type:
    #             media_ext = mimetypes.guess_extension(media_type)
    #     return 'full/%s%s' % (media_guid, media_ext)